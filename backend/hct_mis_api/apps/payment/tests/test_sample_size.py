from hct_mis_api.apps.payment.fixtures import PaymentRecordFactory
from hct_mis_api.apps.program.fixtures import CashPlanFactory
from hct_mis_api.apps.account.fixtures import UserFactory
from hct_mis_api.apps.core.base_test_case import APITestCase
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.payment.models import PaymentRecord
from hct_mis_api.apps.core.fixtures import (
    create_afghanistan,
)
from hct_mis_api.apps.household.fixtures import create_household
from hct_mis_api.apps.core.utils import encode_id_base64


def create_query_variables(cash_plan, verification_channel):
    return {
        "input": {
            "cashPlanId": encode_id_base64(cash_plan.pk, "CashPlan"),
            "sampling": "FULL_LIST",
            "fullListArguments": {"excludedAdminAreas": []},
            "verificationChannel": verification_channel,
            "rapidProArguments": None,
            "randomSamplingArguments": None,
            "businessAreaSlug": "afghanistan",
        }
    }


class TestSampleSize(APITestCase):
    SAMPLE_SIZE_QUERY = """
query SampleSize($input: GetCashplanVerificationSampleSizeInput!) {
  sampleSize(input: $input) {
    paymentRecordCount
    sampleSize
    __typename
  }
}
    """

    @classmethod
    def setUpTestData(cls):
        create_afghanistan()
        cls.user = UserFactory.create()
        cls.business_area = BusinessArea.objects.get(slug="afghanistan")
        cls.household, cls.individuals = create_household(household_args={"size": 1})

        cls.individuals[0].phone_no = "invalid-phone-no"
        cls.individuals[0].phone_no_alternative = "invalid-phone-no"
        cls.individuals[0].save()

    def test_sample_size_in_manual_verification_plan(self):
        cash_plan = CashPlanFactory()
        PaymentRecordFactory(
            cash_plan=cash_plan,
            business_area=self.business_area,
            household=self.household,
            head_of_household_id=self.individuals[0].id,
            status=PaymentRecord.STATUS_SUCCESS,
        )
        manual_sample_query_variables = create_query_variables(cash_plan, "MANUAL")
        manual_response = self.graphql_request(
            request_string=self.SAMPLE_SIZE_QUERY,
            variables=manual_sample_query_variables,
            context={"user": self.user},
        )
        self.assertTrue(manual_response["data"]["sampleSize"]["paymentRecordCount"] == 1)

        rapid_pro_sample_query_variables = create_query_variables(cash_plan, "RAPIDPRO")
        rapid_pro_response = self.graphql_request(
            request_string=self.SAMPLE_SIZE_QUERY,
            variables=rapid_pro_sample_query_variables,
            context={"user": self.user},
        )
        self.assertTrue(rapid_pro_response["data"]["sampleSize"]["paymentRecordCount"] == 0)