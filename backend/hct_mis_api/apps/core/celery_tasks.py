import csv
import logging
import os
import tempfile
from datetime import datetime
from functools import wraps
from typing import Any, Callable

from django.db import transaction
from django.utils import timezone

from hct_mis_api.apps.core.celery import app
from hct_mis_api.apps.core.models import StorageFile, XLSXKoboTemplate
from hct_mis_api.apps.core.tasks.upload_new_template_and_update_flex_fields import (
    KoboRetriableError,
)
from hct_mis_api.apps.core.utils import IDENTIFICATION_TYPE_TO_KEY_MAPPING
from hct_mis_api.apps.household.models import (
    COLLECT_TYPE_SIZE_ONLY,
    HEAD,
    IDENTIFICATION_TYPE_NATIONAL_PASSPORT,
    IDENTIFICATION_TYPE_TAX_ID,
    MALE,
    ROLE_PRIMARY,
    BankAccountInfo,
    Document,
    DocumentType,
    Household,
    Individual,
    IndividualRoleInHousehold,
)
from hct_mis_api.apps.periodic_data_update.utils import populate_pdu_with_null_values
from hct_mis_api.apps.program.models import Program
from hct_mis_api.apps.registration_data.models import RegistrationDataImport
from hct_mis_api.apps.targeting.models import TargetPopulation
from hct_mis_api.apps.targeting.services.targeting_stats_refresher import refresh_stats
from hct_mis_api.apps.utils.logs import log_start_and_end
from hct_mis_api.apps.utils.models import MergeStatusModel
from hct_mis_api.apps.utils.sentry import sentry_tags, set_sentry_business_area_tag

logger = logging.getLogger(__name__)


class transaction_celery_task:  # used as decorator
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.task_args = args
        self.task_kwargs = kwargs

    def __call__(self, func: Callable) -> Any:
        @wraps(func)
        def wrapper_func(*args: Any, **kwargs: Any) -> None:
            try:
                with transaction.atomic():
                    return func(*args, **kwargs)
            except Exception as e:
                logger.error(e)

        task_func = app.task(*self.task_args, **self.task_kwargs)(wrapper_func)
        return task_func


@app.task(bind=True, default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def upload_new_kobo_template_and_update_flex_fields_task_with_retry(self: Any, xlsx_kobo_template_id: str) -> None:
    try:
        from hct_mis_api.apps.core.tasks.upload_new_template_and_update_flex_fields import (
            UploadNewKoboTemplateAndUpdateFlexFieldsTask,
        )

        UploadNewKoboTemplateAndUpdateFlexFieldsTask().execute(xlsx_kobo_template_id=xlsx_kobo_template_id)
    except KoboRetriableError as exc:
        from datetime import timedelta

        from django.utils import timezone

        one_day_earlier_time = timezone.now() - timedelta(days=1)
        if exc.xlsx_kobo_template_object.first_connection_failed_time > one_day_earlier_time:
            logger.exception(exc)
            raise self.retry(exc=exc)
        else:
            exc.xlsx_kobo_template_object.status = XLSXKoboTemplate.UNSUCCESSFUL
    except Exception as e:
        logger.exception(e)
        raise


@app.task(bind=True, default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def upload_new_kobo_template_and_update_flex_fields_task(self: Any, xlsx_kobo_template_id: str) -> None:
    try:
        from hct_mis_api.apps.core.tasks.upload_new_template_and_update_flex_fields import (
            UploadNewKoboTemplateAndUpdateFlexFieldsTask,
        )

        UploadNewKoboTemplateAndUpdateFlexFieldsTask().execute(xlsx_kobo_template_id=xlsx_kobo_template_id)
    except KoboRetriableError:
        upload_new_kobo_template_and_update_flex_fields_task_with_retry.delay(xlsx_kobo_template_id)
    except Exception as e:
        logger.exception(e)
        raise self.retry(exc=e)


@app.task(bind=True, default_retry_delay=60, max_retries=3)
@log_start_and_end
@sentry_tags
def create_target_population_task(self: Any, storage_id: str, program_id: str, tp_name: str) -> None:
    storage_obj = StorageFile.objects.get(id=storage_id)
    file_path = None
    program = Program.objects.get(id=program_id)
    set_sentry_business_area_tag(program.business_area.name)

    try:
        with transaction.atomic():
            registration_data_import = RegistrationDataImport.objects.create(
                name=f"{storage_obj.file.name}_{program.name}",
                number_of_individuals=0,
                number_of_households=0,
                business_area=program.business_area,
                data_source=RegistrationDataImport.EDOPOMOGA,
                program=program,
            )
            if program.biometric_deduplication_enabled:
                registration_data_import.deduplication_engine_status = RegistrationDataImport.DEDUP_ENGINE_PENDING

            business_area = storage_obj.business_area
            country = business_area.countries.first()

            passport_type = DocumentType.objects.get(
                key=IDENTIFICATION_TYPE_TO_KEY_MAPPING[IDENTIFICATION_TYPE_NATIONAL_PASSPORT]
            )
            tax_type = DocumentType.objects.get(key=IDENTIFICATION_TYPE_TO_KEY_MAPPING[IDENTIFICATION_TYPE_TAX_ID])

            first_registration_date = timezone.now()
            last_registration_date = first_registration_date

            families = {}
            individuals, documents, bank_infos = [], [], []

            storage_obj.status = StorageFile.STATUS_PROCESSING
            storage_obj.save(update_fields=["status"])
            rows_count = 0

            # TODO fix to use Azure storage override AzureStorageFile open method
            with storage_obj.file.open("rb") as original_file, tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(original_file.read())
                file_path = tmp.name

            with open(file_path, encoding="cp1251") as file:
                reader = csv.DictReader(file, delimiter=";")
                for row in reader:
                    rows_count += 1
                    family_id = row["ID_FAM"]
                    iban = row["IBAN"]
                    tax_id = row["N_ID"]
                    passport_id = row["PASSPORT"]
                    size = row["FAM_NUM"]

                    individual_data = {
                        "given_name": row.get("NAME", ""),
                        "middle_name": row.get("PATRONYMIC", ""),
                        "family_name": row.get("SURNAME", ""),
                        "full_name": f'{row.get("NAME", "")} {row.get("PATRONYMIC", "")} {row.get("SURNAME", "")}',
                        "birth_date": datetime.strptime(row["BDATE"], "%d.%m.%Y").date(),
                        "phone_no": row.get("PHONЕ", ""),
                        "business_area": business_area,
                        "first_registration_date": first_registration_date,
                        "last_registration_date": last_registration_date,
                        "sex": MALE,
                        "relationship": HEAD,
                        "rdi_merge_status": MergeStatusModel.MERGED,
                        "flex_fields": populate_pdu_with_null_values(program),
                        "registration_data_import": registration_data_import,
                    }
                    if family_id in families:
                        individual = Individual(**individual_data, household_id=families.get(family_id))
                        individuals.append(individual)
                    else:
                        individual = Individual.objects.create(**individual_data)
                        individual.refresh_from_db()

                        household = Household.objects.create(
                            head_of_household=individual,
                            business_area=business_area,
                            first_registration_date=first_registration_date,
                            last_registration_date=last_registration_date,
                            registration_data_import=registration_data_import,
                            size=size,
                            family_id=family_id,
                            storage_obj=storage_obj,
                            collect_individual_data=COLLECT_TYPE_SIZE_ONLY,
                            country=country,
                            rdi_merge_status=MergeStatusModel.MERGED,
                        )

                        individual.household = household
                        individual.save(update_fields=("household",))

                        IndividualRoleInHousehold.objects.create(
                            role=ROLE_PRIMARY,
                            individual=individual,
                            household=household,
                            rdi_merge_status=MergeStatusModel.MERGED,
                        )

                        families[family_id] = household.id

                    passport = Document(
                        document_number=passport_id,
                        type=passport_type,
                        individual=individual,
                        status=Document.STATUS_INVALID,
                        country=country,
                        rdi_merge_status=MergeStatusModel.MERGED,
                    )

                    tax = Document(
                        document_number=tax_id,
                        type=tax_type,
                        individual=individual,
                        status=Document.STATUS_INVALID,
                        country=country,
                        rdi_merge_status=MergeStatusModel.MERGED,
                    )

                    bank_account_info = BankAccountInfo(
                        bank_account_number=iban, individual=individual, rdi_merge_status=MergeStatusModel.MERGED
                    )

                    documents.append(passport)
                    documents.append(tax)
                    bank_infos.append(bank_account_info)

                    if rows_count % 1000 == 0:
                        Individual.objects.bulk_create(individuals)
                        Document.objects.bulk_create(documents)
                        BankAccountInfo.objects.bulk_create(bank_infos)
                        individuals = []
                        documents = []
                        bank_infos = []

            Individual.objects.bulk_create(individuals)
            Document.objects.bulk_create(documents)
            BankAccountInfo.objects.bulk_create(bank_infos)

            households = Household.objects.filter(family_id__in=list(families.keys()))
            households.update(withdrawn=True, withdrawn_date=timezone.now())
            Individual.objects.filter(household__in=households).update(withdrawn=True, withdrawn_date=timezone.now())

            target_population = TargetPopulation.objects.create(
                name=tp_name,
                created_by=storage_obj.created_by,
                program=program,
                status=TargetPopulation.STATUS_LOCKED,
                build_status=TargetPopulation.BUILD_STATUS_OK,
                business_area=business_area,
                storage_file=storage_obj,
            )
            target_population.households.set(households)
            refresh_stats(target_population)
            target_population.save()

            storage_obj.status = StorageFile.STATUS_FINISHED
            storage_obj.save(update_fields=["status"])
    except Exception as e:
        storage_obj.status = StorageFile.STATUS_FAILED
        storage_obj.save(update_fields=["status"])
        raise self.retry(exc=e)
    finally:
        if file_path:
            os.remove(file_path)
