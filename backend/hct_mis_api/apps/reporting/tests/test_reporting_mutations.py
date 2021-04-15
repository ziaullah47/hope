from parameterized import parameterized
from django.core.management import call_command

from hct_mis_api.apps.account.fixtures import UserFactory
from hct_mis_api.apps.account.permissions import Permissions
from hct_mis_api.apps.core.base_test_case import APITestCase
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.household.fixtures import create_household_and_individuals
from hct_mis_api.apps.reporting.validators import ReportValidator
from hct_mis_api.apps.reporting.models import Report
from hct_mis_api.apps.core.fixtures import AdminAreaLevelFactory, AdminAreaFactory
from hct_mis_api.apps.core.utils import encode_id_base64
from hct_mis_api.apps.program.fixtures import ProgramFactory


class TestReportingMutation(APITestCase):

    CREATE_REPORT = """
    mutation CreateReport($reportData: CreateReportInput!) {
        createReport(reportData: $reportData) {
            report {
                reportType
                dateFrom
                dateTo
                status
            }
        }
    }
    """

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        call_command("loadbusinessareas")
        self.business_area_slug = "afghanistan"
        self.business_area = BusinessArea.objects.get(slug=self.business_area_slug)
        family_sizes_list = (2, 4, 5, 1, 3, 11, 14)
        last_registration_dates = ("2020-01-01", "2021-01-01")
        area_type = AdminAreaLevelFactory(
            name="Admin type one",
            admin_level=2,
            business_area=self.business_area,
        )
        self.admin_area_1 = AdminAreaFactory(title="Adminarea Test", admin_area_level=area_type)
        self.program_1 = ProgramFactory(business_area=self.business_area, end_date="2020-01-01")

        self.households = []
        for index, family_size in enumerate(family_sizes_list):
            (household, individuals) = create_household_and_individuals(
                {
                    "size": family_size,
                    "address": "Lorem Ipsum",
                    "country_origin": "PL",
                    "business_area": self.business_area,
                    "last_registration_date": last_registration_dates[0] if index % 2 else last_registration_dates[1],
                },
                [{"last_registration_date": last_registration_dates[0] if index % 2 else last_registration_dates[1]}],
            )

    @parameterized.expand(
        [
            (
                "with_permission_individuals_report_with_earlier_dateTo",
                [Permissions.REPORTING_EXPORT],
                Report.INDIVIDUALS,
                "2020-01-02",
            ),
            (
                "with_permission_individuals_report_with_later_dateTo",
                [Permissions.REPORTING_EXPORT],
                Report.INDIVIDUALS,
                "2022-01-02",
            ),
            (
                "with_permission_households_report_with_earlier_dateTo",
                [Permissions.REPORTING_EXPORT],
                Report.HOUSEHOLD_DEMOGRAPHICS,
                "2020-01-02",
            ),
            (
                "with_permission_households_report_with_later_dateTo",
                [Permissions.REPORTING_EXPORT],
                Report.HOUSEHOLD_DEMOGRAPHICS,
                "2022-01-02",
            ),
            ("without_permission_individuals_report", [], Report.INDIVIDUALS, "2022-01-02"),
        ]
    )
    def test_create_report_with_no_extra_filters(self, _, permissions, report_type, date_to):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)
        self.snapshot_graphql_request(
            request_string=self.CREATE_REPORT,
            context={"user": self.user},
            variables={
                "reportData": {
                    "businessAreaSlug": self.business_area_slug,
                    "reportType": report_type,
                    "dateFrom": "2019-01-01",
                    "dateTo": date_to,
                }
            },
        )

    @parameterized.expand(
        [
            ("individuals", Report.INDIVIDUALS, "admin_area", "program"),
            ("households", Report.HOUSEHOLD_DEMOGRAPHICS, "admin_area", "program"),
            ("cash_plan_verifications", Report.CASH_PLAN_VERIFICATION, "program", "admin_area"),
            ("payments", Report.PAYMENTS, "admin_area", "program"),
            ("payment_verifications", Report.PAYMENT_VERIFICATION, "program", "admin_area"),
            ("cash_plans", Report.CASH_PLAN, "program", "admin_area"),
            ("programs", Report.PROGRAM, None, "admin_area"),
            ("programs", Report.PROGRAM, None, "program"),
            ("individuals_payments", Report.INDIVIDUALS_AND_PAYMENT, "admin_area", None),
            ("individuals_payments", Report.INDIVIDUALS_AND_PAYMENT, "program", None),
        ]
    )
    def test_create_report_validator(self, _, report_type, should_exist_field, should_not_exist_field):

        report_data = {
            "report_type": report_type,
            "business_area_slug": self.business_area_slug,
            "date_from": "2019-01-01",
            "date_to": "2021-01-01",
            "admin_area": [encode_id_base64(self.admin_area_1, "AdminArea")],
            "program": encode_id_base64(self.program_1, "Program"),
        }
        ReportValidator.validate_report_type_filters(report_data=report_data)

        if should_exist_field:
            self.assertTrue(should_exist_field in report_data)
        if should_not_exist_field:
            self.assertFalse(should_not_exist_field in report_data)