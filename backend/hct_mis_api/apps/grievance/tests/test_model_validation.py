from django.core.exceptions import ValidationError
from django.test import TestCase

from hct_mis_api.apps.account.fixtures import UserFactory
from hct_mis_api.apps.core.fixtures import create_afghanistan
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.grievance.models import GrievanceTicket
from hct_mis_api.apps.payment.fixtures import (
    FinancialServiceProviderFactory,
    FinancialServiceProviderXlsxTemplateFactory,
    FspXlsxTemplatePerDeliveryMechanismFactory,
    generate_delivery_mechanisms,
)
from hct_mis_api.apps.payment.models import DeliveryMechanism


class TestGrievanceModelValidation(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        create_afghanistan()
        cls.user = UserFactory.create()
        cls.base_model_data = {
            "status": GrievanceTicket.STATUS_NEW,
            "description": "test description",
            "area": "test area",
            "language": "english",
            "consent": True,
            "business_area": BusinessArea.objects.first(),
            "assigned_to": cls.user,
            "created_by": cls.user,
        }

        cls.valid_model_data = {
            "category": GrievanceTicket.CATEGORY_DATA_CHANGE,
            "issue_type": GrievanceTicket.ISSUE_TYPE_INDIVIDUAL_DATA_CHANGE_DATA_UPDATE,
        }

        cls.valid_model_2_data = {
            "category": GrievanceTicket.CATEGORY_POSITIVE_FEEDBACK,
            "issue_type": None,
        }

        cls.invalid_model_data = {
            "category": GrievanceTicket.CATEGORY_DATA_CHANGE,
            "issue_type": None,
        }

        cls.invalid_model_2_data = {
            "category": GrievanceTicket.CATEGORY_POSITIVE_FEEDBACK,
            "issue_type": GrievanceTicket.ISSUE_TYPE_INDIVIDUAL_DATA_CHANGE_DATA_UPDATE,
        }

    def test_valid_issue_types(self) -> None:
        grievance_ticket_1 = GrievanceTicket(**self.base_model_data, **self.valid_model_data)
        grievance_ticket_2 = GrievanceTicket(**self.base_model_data, **self.valid_model_2_data)

        grievance_ticket_1.save()
        grievance_ticket_2.save()

        self.assertEqual(self.valid_model_data["issue_type"], grievance_ticket_1.issue_type)
        self.assertEqual(self.valid_model_2_data["issue_type"], grievance_ticket_2.issue_type)

    def test_invalid_issue_types(self) -> None:
        grievance_ticket_1 = GrievanceTicket(**self.base_model_data, **self.invalid_model_data)
        grievance_ticket_2 = GrievanceTicket(**self.base_model_data, **self.invalid_model_2_data)

        self.assertRaisesMessage(
            ValidationError,
            "{'issue_type': ['Invalid issue type for selected category']}",
            grievance_ticket_1.save,
        )
        self.assertRaisesMessage(
            ValidationError,
            "{'issue_type': ['Invalid issue type for selected category']}",
            grievance_ticket_2.save,
        )


class TestFspXlsxTemplatePerDeliveryMechanismValidation(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        create_afghanistan()
        cls.user = UserFactory.create()
        generate_delivery_mechanisms()

    def test_clean(self) -> None:
        dm_cash = DeliveryMechanism.objects.get(code="cash")
        dm_atm_card = DeliveryMechanism.objects.get(code="atm_card")
        fsp = FinancialServiceProviderFactory()
        fsp.delivery_mechanisms.set([dm_atm_card])
        template = FinancialServiceProviderXlsxTemplateFactory()
        template_per_dm_cash = FspXlsxTemplatePerDeliveryMechanismFactory(
            financial_service_provider=fsp,
            delivery_mechanism=dm_cash,
            xlsx_template=template,
        )

        with self.assertRaisesMessage(
            ValidationError,
            f"Delivery Mechanism {template_per_dm_cash.delivery_mechanism} is not supported by Financial Service Provider {fsp}",
        ):
            template_per_dm_cash.clean()

        template_per_dm_atm_card = FspXlsxTemplatePerDeliveryMechanismFactory(
            financial_service_provider=fsp,
            delivery_mechanism=dm_atm_card,
            xlsx_template=template,
        )

        with self.assertRaisesMessage(
            ValidationError,
            f"['card_number__atm_card', 'card_expiry_date__atm_card', 'name_of_cardholder__atm_card'] fields are required by delivery mechanism "
            f"{template_per_dm_atm_card.delivery_mechanism} and must be present in the template core fields",
        ):
            template_per_dm_atm_card.clean()

        template.core_fields = ["card_number__atm_card", "card_expiry_date__atm_card", "name_of_cardholder__atm_card"]
        template.save()
        template_per_dm_atm_card.clean()
