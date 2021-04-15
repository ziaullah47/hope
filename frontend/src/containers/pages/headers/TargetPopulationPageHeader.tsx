import React from 'react';
import styled from 'styled-components';
import { useTranslation } from 'react-i18next';
import { TargetPopulationNode } from '../../../__generated__/graphql';
import { PageHeader } from '../../../components/PageHeader';
import { BreadCrumbsItem } from '../../../components/BreadCrumbs';
import { useBusinessArea } from '../../../hooks/useBusinessArea';
import { StatusBox } from '../../../components/StatusBox';
import {
  targetPopulationStatusToColor,
  targetPopulationStatusMapping,
} from '../../../utils/utils';
import { InProgressTargetPopulationHeaderButtons } from './InProgressTargetPopulationHeaderButtons';
import { FinalizedTargetPopulationHeaderButtons } from './FinalizedTargetPopulationHeaderButtons';
import { ApprovedTargetPopulationHeaderButtons } from './ApprovedTargetPopulationHeaderButtons';

const HeaderWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  div {
    margin: 0 0 0 ${({ theme }) => theme.spacing(3)}px;
  }
`;
const StatusWrapper = styled.div`
  width: 140px;
`;

export interface ProgramDetailsPageHeaderPropTypes {
  setEditState: Function;
  targetPopulation: TargetPopulationNode;
  canEdit: boolean;
  canRemove: boolean;
  canDuplicate: boolean;
  canLock: boolean;
  canUnlock: boolean;
  canSend: boolean;
}

export function TargetPopulationPageHeader({
  targetPopulation,
  setEditState,
  canEdit,
  canRemove,
  canDuplicate,
  canLock,
  canUnlock,
  canSend,
}: ProgramDetailsPageHeaderPropTypes): React.ReactElement {
  const { t } = useTranslation();
  const businessArea = useBusinessArea();
  const breadCrumbsItems: BreadCrumbsItem[] = [
    {
      title: 'Targeting',
      to: `/${businessArea}/target-population/`,
    },
  ];
  //TODO: Use statuses from node - not in backend yet
  let buttons;
  switch (targetPopulation.status) {
    case 'DRAFT':
      buttons = (
        <InProgressTargetPopulationHeaderButtons
          targetPopulation={targetPopulation}
          setEditState={setEditState}
          canDuplicate={canDuplicate}
          canRemove={canRemove}
          canEdit={canEdit}
          canLock={canLock}
        />
      );
      break;
    case 'APPROVED':
      buttons = (
        <ApprovedTargetPopulationHeaderButtons
          targetPopulation={targetPopulation}
          canDuplicate={canDuplicate}
          canUnlock={canUnlock}
          canSend={canSend}
        />
      );
      break;
    default:
      //FINALIZED
      buttons = (
        <FinalizedTargetPopulationHeaderButtons
          targetPopulation={targetPopulation}
          canDuplicate={canDuplicate}
        />
      );
      break;
  }
  return (
    <>
      <PageHeader
        title={
          <HeaderWrapper>
            {t(`${targetPopulation.name}`)}
            <StatusWrapper>
              <StatusBox
                status={targetPopulation.status}
                statusToColor={targetPopulationStatusToColor}
                statusNameMapping={targetPopulationStatusMapping}
              />
            </StatusWrapper>
          </HeaderWrapper>
        }
        breadCrumbs={breadCrumbsItems}
      >
        {buttons}
      </PageHeader>
    </>
  );
}