import { gql } from 'apollo-boost';

export const AllTargetPopulations = gql`
  query AllTargetPopulations(
    $after: String
    $before: String
    $first: Int
    $last: Int
    $orderBy: String
    $name: String
    $status: String
    $candidateListTotalHouseholdsMin: Int
    $candidateListTotalHouseholdsMax: Int
    $businessArea: String
    $program: [ID]
  ) {
    allTargetPopulation(
      after: $after
      before: $before
      first: $first
      last: $last
      orderBy: $orderBy
      name: $name
      status: $status
      candidateListTotalHouseholdsMin: $candidateListTotalHouseholdsMin
      candidateListTotalHouseholdsMax: $candidateListTotalHouseholdsMax
      businessArea: $businessArea
      program: $program
    ) {
      edges {
        node {
          ...targetPopulationMinimal
        }
        cursor
      }
      totalCount
      edgeCount
    }
  }
`;