import graphene

from hct_mis_api.apps.grievance.mutations_extras.data_change import (
    AddIndividualIssueTypeExtras,
    HouseholdDataUpdateIssueTypeExtras,
    IndividualDataUpdateIssueTypeExtras,
    IndividualDeleteIssueTypeExtras,
    UpdateAddIndividualIssueTypeExtras,
    UpdateHouseholdDataUpdateIssueTypeExtras,
    UpdateIndividualDataUpdateIssueTypeExtras,
)
from hct_mis_api.apps.grievance.mutations_extras.feedback import (
    NegativeFeedbackTicketExtras,
    PositiveFeedbackTicketExtras,
)
from hct_mis_api.apps.grievance.mutations_extras.grievance_complaint import (
    GrievanceComplaintTicketExtras,
)
from hct_mis_api.apps.grievance.mutations_extras.referral import ReferralTicketExtras
from hct_mis_api.apps.grievance.mutations_extras.sensitive_grievance import (
    SensitiveGrievanceTicketExtras,
)


class IssueTypeExtrasInput(graphene.InputObjectType):
    household_data_update_issue_type_extras = HouseholdDataUpdateIssueTypeExtras()
    individual_data_update_issue_type_extras = IndividualDataUpdateIssueTypeExtras()
    individual_delete_issue_type_extras = IndividualDeleteIssueTypeExtras()
    add_individual_issue_type_extras = AddIndividualIssueTypeExtras()


class CategoryExtrasInput(graphene.InputObjectType):
    sensitive_grievance_ticket_extras = SensitiveGrievanceTicketExtras()
    grievance_complaint_ticket_extras = GrievanceComplaintTicketExtras()
    positive_feedback_ticket_extras = PositiveFeedbackTicketExtras()
    negative_feedback_ticket_extras = NegativeFeedbackTicketExtras()
    referral_ticket_extras = ReferralTicketExtras()


class CreateGrievanceTicketExtrasInput(graphene.InputObjectType):
    category = CategoryExtrasInput()
    issue_type = IssueTypeExtrasInput()


class UpdateGrievanceTicketExtrasInput(graphene.InputObjectType):
    household_data_update_issue_type_extras = UpdateHouseholdDataUpdateIssueTypeExtras()
    individual_data_update_issue_type_extras = UpdateIndividualDataUpdateIssueTypeExtras()
    add_individual_issue_type_extras = UpdateAddIndividualIssueTypeExtras()
    category = CategoryExtrasInput()


def _no_operation_close_method(*args, **kwargs):
    pass