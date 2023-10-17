import { gql } from 'apollo-boost';
export const BulkUpdateGrievancePriority = gql`
  mutation BulkUpdateGrievancePriority(
    $grievanceTicketIds: [ID]!
    $priority: Int!
    $businessAreaSlug: String!
  ) {
    bulkUpdateGrievancePriority(
      grievanceTicketIds: $grievanceTicketIds
      priority: $priority
      businessAreaSlug: $businessAreaSlug
    ) {
      grievanceTickets {
        id
        priority
      }
    }
  }
`;