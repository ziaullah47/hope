from django.core.management import call_command
from parameterized import parameterized

from hct_mis_api.apps.account.fixtures import UserFactory
from hct_mis_api.apps.account.permissions import Permissions
from hct_mis_api.apps.core.base_test_case import APITestCase
from hct_mis_api.apps.core.fixtures import AdminAreaLevelFactory, AdminAreaFactory
from hct_mis_api.apps.core.models import BusinessArea
from hct_mis_api.apps.grievance.models import GrievanceTicket
from hct_mis_api.apps.household.fixtures import create_household
from hct_mis_api.apps.payment.fixtures import PaymentRecordFactory
from hct_mis_api.apps.program.fixtures import ProgramFactory, CashPlanFactory


class TestGrievanceCreateSensitiveTicketQuery(APITestCase):
    CREATE_GRIEVANCE_MUTATION = """
    mutation CreateGrievanceTicket($input: CreateGrievanceTicketInput!) {
      createGrievanceTicket(input: $input) {
        grievanceTickets{
          category
          issueType
          admin
          language
          description
          consent
          sensitiveTicketDetails {
            household {
              size
            }
            individual {
              fullName
            }
            paymentRecord {
              fullName
            }
          }
        }
      }
    }
    """

    def setUp(self):
        super().setUp()
        call_command("loadbusinessareas")
        self.user = UserFactory.create()
        self.business_area = BusinessArea.objects.get(slug="afghanistan")
        area_type = AdminAreaLevelFactory(
            name="Admin type one",
            admin_level=2,
            business_area=self.business_area,
        )
        self.admin_area = AdminAreaFactory(title="City Test", admin_area_level=area_type, p_code="asfdsfg")
        self.household, self.individuals = create_household(
            {"size": 1, "business_area": self.business_area},
            {"given_name": "John", "family_name": "Doe", "middle_name": "", "full_name": "John Doe"},
        )
        program = ProgramFactory(business_area=self.business_area)
        cash_plan = CashPlanFactory(program=program, business_area=self.business_area)
        self.payment_record = PaymentRecordFactory(
            household=self.household,
            full_name=self.individuals[0].full_name,
            business_area=self.business_area,
            cash_plan=cash_plan,
        )
        self.second_payment_record = PaymentRecordFactory(
            household=self.household,
            full_name=f"{self.individuals[0].full_name} second Individual",
            business_area=self.business_area,
            cash_plan=cash_plan,
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.GRIEVANCES_CREATE],
            ),
            ("without_permission", []),
        ]
    )
    def test_create_sensitive_ticket(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        input_data = {
            "input": {
                "description": "Test Feedback",
                "assignedTo": self.id_to_base64(self.user.id, "UserNode"),
                "category": GrievanceTicket.CATEGORY_SENSITIVE_GRIEVANCE,
                "issueType": GrievanceTicket.ISSUE_TYPE_MISCELLANEOUS,
                "admin": self.admin_area.p_code,
                "language": "Polish, English",
                "consent": True,
                "businessArea": "afghanistan",
                "extras": {
                    "category": {
                        "sensitiveGrievanceTicketExtras": {
                            "household": self.id_to_base64(self.household.id, "HouseholdNode"),
                            "individual": self.id_to_base64(self.individuals[0].id, "IndividualNode"),
                            "paymentRecord": [self.id_to_base64(self.payment_record.id, "PaymentRecordNode")],
                        }
                    }
                },
            }
        }

        self.snapshot_graphql_request(
            request_string=self.CREATE_GRIEVANCE_MUTATION,
            context={"user": self.user},
            variables=input_data,
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.GRIEVANCES_CREATE],
            ),
            ("without_permission", []),
        ]
    )
    def test_create_sensitive_ticket_wrong_extras(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        input_data = {
            "input": {
                "description": "Test Feedback",
                "assignedTo": self.id_to_base64(self.user.id, "UserNode"),
                "category": GrievanceTicket.CATEGORY_SENSITIVE_GRIEVANCE,
                "issueType": GrievanceTicket.ISSUE_TYPE_MISCELLANEOUS,
                "admin": self.admin_area.p_code,
                "language": "Polish, English",
                "consent": True,
                "businessArea": "afghanistan",
                "extras": {
                    "category": {
                        "grievanceComplaintTicketExtras": {
                            "household": self.id_to_base64(self.household.id, "HouseholdNode"),
                            "individual": self.id_to_base64(self.individuals[0].id, "IndividualNode"),
                            "paymentRecord": [self.id_to_base64(self.payment_record.id, "PaymentRecordNode")],
                        }
                    }
                },
            }
        }

        self.snapshot_graphql_request(
            request_string=self.CREATE_GRIEVANCE_MUTATION,
            context={"user": self.user},
            variables=input_data,
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.GRIEVANCES_CREATE],
            ),
            ("without_permission", []),
        ]
    )
    def test_create_sensitive_ticket_without_issue_type(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        input_data = {
            "input": {
                "description": "Test Feedback",
                "assignedTo": self.id_to_base64(self.user.id, "UserNode"),
                "category": GrievanceTicket.CATEGORY_SENSITIVE_GRIEVANCE,
                "admin": self.admin_area.p_code,
                "language": "Polish, English",
                "consent": True,
                "businessArea": "afghanistan",
                "extras": {
                    "category": {
                        "sensitiveGrievanceTicketExtras": {
                            "household": self.id_to_base64(self.household.id, "HouseholdNode"),
                            "individual": self.id_to_base64(self.individuals[0].id, "IndividualNode"),
                            "paymentRecord": [self.id_to_base64(self.payment_record.id, "PaymentRecordNode")],
                        }
                    }
                },
            }
        }

        self.snapshot_graphql_request(
            request_string=self.CREATE_GRIEVANCE_MUTATION,
            context={"user": self.user},
            variables=input_data,
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.GRIEVANCES_CREATE],
            ),
            ("without_permission", []),
        ]
    )
    def test_create_sensitive_ticket_with_two_payment_records(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        input_data = {
            "input": {
                "description": "Test Feedback",
                "assignedTo": self.id_to_base64(self.user.id, "UserNode"),
                "category": GrievanceTicket.CATEGORY_SENSITIVE_GRIEVANCE,
                "issueType": GrievanceTicket.ISSUE_TYPE_MISCELLANEOUS,
                "admin": self.admin_area.p_code,
                "language": "Polish, English",
                "consent": True,
                "businessArea": "afghanistan",
                "extras": {
                    "category": {
                        "sensitiveGrievanceTicketExtras": {
                            "household": self.id_to_base64(self.household.id, "HouseholdNode"),
                            "individual": self.id_to_base64(self.individuals[0].id, "IndividualNode"),
                            "paymentRecord": [
                                self.id_to_base64(self.payment_record.id, "PaymentRecordNode"),
                                self.id_to_base64(self.second_payment_record.id, "PaymentRecordNode"),
                            ],
                        }
                    }
                },
            }
        }

        self.snapshot_graphql_request(
            request_string=self.CREATE_GRIEVANCE_MUTATION,
            context={"user": self.user},
            variables=input_data,
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.GRIEVANCES_CREATE],
            ),
            ("without_permission", []),
        ]
    )
    def test_create_sensitive_ticket_without_payment_record(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        input_data = {
            "input": {
                "description": "Test Feedback",
                "assignedTo": self.id_to_base64(self.user.id, "UserNode"),
                "category": GrievanceTicket.CATEGORY_SENSITIVE_GRIEVANCE,
                "issueType": GrievanceTicket.ISSUE_TYPE_MISCELLANEOUS,
                "admin": self.admin_area.p_code,
                "language": "Polish, English",
                "consent": True,
                "businessArea": "afghanistan",
                "extras": {
                    "category": {
                        "sensitiveGrievanceTicketExtras": {
                            "household": self.id_to_base64(self.household.id, "HouseholdNode"),
                            "individual": self.id_to_base64(self.individuals[0].id, "IndividualNode"),
                        }
                    }
                },
            }
        }

        self.snapshot_graphql_request(
            request_string=self.CREATE_GRIEVANCE_MUTATION,
            context={"user": self.user},
            variables=input_data,
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.GRIEVANCES_CREATE],
            ),
            ("without_permission", []),
        ]
    )
    def test_create_sensitive_ticket_without_household(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        input_data = {
            "input": {
                "description": "Test Feedback",
                "assignedTo": self.id_to_base64(self.user.id, "UserNode"),
                "category": GrievanceTicket.CATEGORY_SENSITIVE_GRIEVANCE,
                "issueType": GrievanceTicket.ISSUE_TYPE_MISCELLANEOUS,
                "admin": self.admin_area.p_code,
                "language": "Polish, English",
                "consent": True,
                "businessArea": "afghanistan",
                "extras": {
                    "category": {
                        "sensitiveGrievanceTicketExtras": {
                            "individual": self.id_to_base64(self.individuals[0].id, "IndividualNode"),
                            "paymentRecord": [self.id_to_base64(self.payment_record.id, "PaymentRecordNode")],
                        }
                    }
                },
            }
        }

        self.snapshot_graphql_request(
            request_string=self.CREATE_GRIEVANCE_MUTATION,
            context={"user": self.user},
            variables=input_data,
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.GRIEVANCES_CREATE],
            ),
            ("without_permission", []),
        ]
    )
    def test_create_sensitive_ticket_without_individual(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        input_data = {
            "input": {
                "description": "Test Feedback",
                "assignedTo": self.id_to_base64(self.user.id, "UserNode"),
                "category": GrievanceTicket.CATEGORY_SENSITIVE_GRIEVANCE,
                "issueType": GrievanceTicket.ISSUE_TYPE_MISCELLANEOUS,
                "admin": self.admin_area.p_code,
                "language": "Polish, English",
                "consent": True,
                "businessArea": "afghanistan",
                "extras": {
                    "category": {
                        "sensitiveGrievanceTicketExtras": {
                            "household": self.id_to_base64(self.household.id, "HouseholdNode"),
                            "paymentRecord": [self.id_to_base64(self.payment_record.id, "PaymentRecordNode")],
                        }
                    }
                },
            }
        }

        self.snapshot_graphql_request(
            request_string=self.CREATE_GRIEVANCE_MUTATION,
            context={"user": self.user},
            variables=input_data,
        )

    @parameterized.expand(
        [
            (
                "with_permission",
                [Permissions.GRIEVANCES_CREATE],
            ),
            ("without_permission", []),
        ]
    )
    def test_create_sensitive_ticket_without_extras(self, _, permissions):
        self.create_user_role_with_permissions(self.user, permissions, self.business_area)

        input_data = {
            "input": {
                "description": "Test Feedback",
                "assignedTo": self.id_to_base64(self.user.id, "UserNode"),
                "category": GrievanceTicket.CATEGORY_SENSITIVE_GRIEVANCE,
                "issueType": GrievanceTicket.ISSUE_TYPE_MISCELLANEOUS,
                "admin": self.admin_area.p_code,
                "language": "Polish, English",
                "consent": True,
                "businessArea": "afghanistan",
            }
        }

        self.snapshot_graphql_request(
            request_string=self.CREATE_GRIEVANCE_MUTATION,
            context={"user": self.user},
            variables=input_data,
        )