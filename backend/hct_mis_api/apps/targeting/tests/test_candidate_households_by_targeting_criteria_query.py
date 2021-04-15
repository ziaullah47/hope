from django.core.management import call_command
from parameterized import parameterized

from hct_mis_api.apps.targeting.models import (
    HouseholdSelection,
    TargetingCriteria,
    TargetingCriteriaRule,
    TargetingCriteriaRuleFilter,
    TargetPopulation,
)

from hct_mis_api.apps.account.fixtures import UserFactory
from hct_mis_api.apps.core.base_test_case import APITestCase
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.household.fixtures import create_household
from hct_mis_api.apps.account.permissions import Permissions


class CandidateListTargetingCriteriaQueryTestCase(APITestCase):
    QUERY = """
    query CandidateListByTargetingCriteria($targetPopulation: ID!, $businessArea: String) {
      candidateHouseholdsListByTargetingCriteria (targetPopulation:$targetPopulation, businessArea: $businessArea){
        totalCount
        edges {
          node {
            size
            residenceStatus
          }
        }
      }
    }
    """
    QUERY_FIRST_10 = """
        query CandidateListByTargetingCriteria($targetPopulation: ID!, $businessArea: String) {
          candidateHouseholdsListByTargetingCriteria (targetPopulation:$targetPopulation, first: 10, businessArea: $businessArea){
            totalCount
            edges {
              node {
                size
                residenceStatus
              }
            }
          }
        }
        """

    @classmethod
    def setUpTestData(cls):
        call_command("loadbusinessareas")
        cls.business_area = BusinessArea.objects.first()
        _ = create_household(
            {"size": 1, "residence_status": "HOST", "business_area": cls.business_area},
        )
        (household, individuals) = create_household(
            {"size": 1, "residence_status": "HOST", "business_area": cls.business_area},
        )
        cls.household_size_1 = household
        cls.household_residence_status_citizen = household

        (household, individuals) = create_household(
            {"size": 2, "residence_status": "REFUGEE", "business_area": cls.business_area},
        )
        cls.household_residence_status_refugee = household
        cls.household_size_2 = household
        cls.user = UserFactory.create()
        targeting_criteria = cls.get_targeting_criteria_for_rule(
            {"field_name": "size", "arguments": [2], "comparision_method": "EQUALS"}
        )
        cls.target_population_size_2 = TargetPopulation(
            name="target_population_size_2",
            created_by=cls.user,
            candidate_list_targeting_criteria=targeting_criteria,
        )
        cls.target_population_size_2.save()
        targeting_criteria = cls.get_targeting_criteria_for_rule(
            {"field_name": "residence_status", "arguments": ["REFUGEE"], "comparision_method": "EQUALS"}
        )
        cls.target_population_residence_status = TargetPopulation(
            name="target_population_residence_status",
            created_by=cls.user,
            candidate_list_targeting_criteria=targeting_criteria,
        )
        cls.target_population_residence_status.save()

        targeting_criteria = cls.get_targeting_criteria_for_rule(
            {"field_name": "size", "arguments": [1], "comparision_method": "EQUALS"}
        )
        cls.target_population_size_1_approved = TargetPopulation(
            name="target_population_size_1_approved",
            created_by=cls.user,
            candidate_list_targeting_criteria=targeting_criteria,
            status="APPROVED",
        )
        cls.target_population_size_1_approved.save()
        HouseholdSelection.objects.create(
            household=cls.household_size_1,
            target_population=cls.target_population_size_1_approved,
        )
        cls.variables = {"businessArea": cls.business_area.slug}

    @staticmethod
    def get_targeting_criteria_for_rule(rule_filter):
        targeting_criteria = TargetingCriteria()
        targeting_criteria.save()
        rule = TargetingCriteriaRule(targeting_criteria=targeting_criteria)
        rule.save()
        rule_filter = TargetingCriteriaRuleFilter(**rule_filter, targeting_criteria_rule=rule)
        rule_filter.save()
        return targeting_criteria

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.TARGETING_VIEW_DETAILS],
            ),
            ("without_permission", []),
        ]
    )
    def test_candidate_households_list_by_targeting_criteria_size(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        self.snapshot_graphql_request(
            request_string=CandidateListTargetingCriteriaQueryTestCase.QUERY,
            context={"user": self.user},
            variables={
                "targetPopulation": self.id_to_base64(self.target_population_size_2.id, "TargetPopulationNode"),
                **self.variables,
            },
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.TARGETING_VIEW_DETAILS],
            ),
            ("without_permission", []),
        ]
    )
    def test_candidate_households_list_by_targeting_criteria_residence_status(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        self.snapshot_graphql_request(
            request_string=CandidateListTargetingCriteriaQueryTestCase.QUERY,
            context={"user": self.user},
            variables={
                "targetPopulation": self.id_to_base64(
                    self.target_population_residence_status.id,
                    "TargetPopulationNode",
                ),
                **self.variables,
            },
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.TARGETING_VIEW_DETAILS],
            ),
            ("without_permission", []),
        ]
    )
    def test_candidate_households_list_by_targeting_criteria_approved(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        self.snapshot_graphql_request(
            request_string=CandidateListTargetingCriteriaQueryTestCase.QUERY,
            context={"user": self.user},
            variables={
                "targetPopulation": self.id_to_base64(
                    self.target_population_size_1_approved.id,
                    "TargetPopulationNode",
                ),
                **self.variables,
            },
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.TARGETING_VIEW_DETAILS],
            ),
            ("without_permission", []),
        ]
    )
    def test_candidate_households_list_by_targeting_criteria_first_10(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        self.snapshot_graphql_request(
            request_string=CandidateListTargetingCriteriaQueryTestCase.QUERY_FIRST_10,
            context={"user": self.user},
            variables={
                "targetPopulation": self.id_to_base64(self.target_population_size_2.id, "TargetPopulationNode"),
                **self.variables,
            },
        )