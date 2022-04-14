import React, { Fragment, useState } from 'react';
import styled from 'styled-components';
import { useTranslation } from 'react-i18next';
import { Button, Paper, Typography } from '@material-ui/core';
import { AddCircleOutline } from '@material-ui/icons';
import { TargetCriteriaForm } from '../../../containers/forms/TargetCriteriaForm';
import { TargetPopulationQuery } from '../../../__generated__/graphql';
import { Criteria } from './Criteria';
import {
  ContentWrapper,
  VulnerabilityScoreComponent,
} from './VulnerabilityScoreComponent';

const PaperContainer = styled(Paper)`
  margin: ${({ theme }) => theme.spacing(5)}px;
  border-bottom: 1px solid rgba(224, 224, 224, 1);
`;

const Title = styled.div`
  padding: ${({ theme }) => theme.spacing(3)}px
    ${({ theme }) => theme.spacing(4)}px;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Divider = styled.div`
  border-left: 1px solid #b1b1b5;
  margin: 0 ${({ theme }) => theme.spacing(10)}px;
  position: relative;
  transform: scale(0.9);
`;

const DividerLabel = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 500;
  color: #253b46;
  text-transform: uppercase;
  padding: 5px;
  border: 1px solid #b1b1b5;
  border-radius: 50%;
  background-color: #fff;
`;

const AddCriteria = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  color: #003c8f;
  border: 2px solid #033f91;
  border-radius: 3px;
  font-size: 16px;
  padding: ${({ theme }) => theme.spacing(6)}px
    ${({ theme }) => theme.spacing(28)}px;
  cursor: pointer;
  p {
    font-weight: 500;
    margin: 0 0 0 ${({ theme }) => theme.spacing(2)}px;
  }
`;

interface TargetingCriteriaProps {
  candidateListRules?;
  isEdit?: boolean;
  helpers?;
  targetPopulation?: TargetPopulationQuery['targetPopulation'];
  selectedProgram?;
}

export function TargetingCriteria({
  candidateListRules,
  isEdit = false,
  helpers,
  targetPopulation,
  selectedProgram,
}: TargetingCriteriaProps): React.ReactElement {
  const { t } = useTranslation();
  const [isOpen, setOpen] = useState(false);
  const [criteriaIndex, setIndex] = useState(null);
  const [criteriaObject, setCriteria] = useState({});
  const openModal = (criteria): void => {
    setCriteria(criteria);
    setOpen(true);
  };
  const closeModal = (): void => {
    setCriteria({});
    setIndex(null);
    return setOpen(false);
  };
  const editCriteria = (criteria, index): void => {
    setIndex(index);
    return openModal(criteria);
  };

  const addCriteria = (values): void => {
    const criteria = {
      filters: [...values.filters],
      individualsFiltersBlocks: [...values.individualsFiltersBlocks],
    };
    if (criteriaIndex !== null) {
      helpers.replace(criteriaIndex, criteria);
    } else {
      helpers.push(criteria);
    }
    return closeModal();
  };
  return (
    <div>
      <PaperContainer>
        <Title>
          <Typography variant='h6'>{t('Targeting Criteria')}</Typography>
          {isEdit && (
            <>
              {!!candidateListRules.length && (
                <Button
                  variant='outlined'
                  color='primary'
                  onClick={() => setOpen(true)}
                >
                  {t('Add')} &apos;Or&apos; {t('Filter')}
                </Button>
              )}
              <TargetCriteriaForm
                criteria={criteriaObject}
                title={t('Add Filter')}
                open={isOpen}
                onClose={() => closeModal()}
                addCriteria={addCriteria}
                shouldShowWarningForIndividualFilter={
                  selectedProgram && !selectedProgram.individualDataNeeded
                }
              />
            </>
          )}
        </Title>
        <ContentWrapper>
          {candidateListRules.length ? (
            candidateListRules.map((criteria, index) => {
              return (
                //eslint-disable-next-line
                <Fragment key={criteria.id || index}>
                  <Criteria
                    isEdit={isEdit}
                    canRemove={candidateListRules.length > 1}
                    rules={criteria.filters}
                    individualsFiltersBlocks={
                      criteria.individualsFiltersBlocks || []
                    }
                    editFunction={() => editCriteria(criteria, index)}
                    removeFunction={() => helpers.remove(index)}
                  />

                  {index === candidateListRules.length - 1 ||
                  (candidateListRules.length === 1 && index === 0) ? null : (
                    <Divider>
                      <DividerLabel>Or</DividerLabel>
                    </Divider>
                  )}
                </Fragment>
              );
            })
          ) : (
            <AddCriteria
              onClick={() => setOpen(true)}
              data-cy='button-target-population-add-criteria'
            >
              <AddCircleOutline />
              <p>{t('Add Filter')}</p>
            </AddCriteria>
          )}
        </ContentWrapper>
        {targetPopulation && (
          <VulnerabilityScoreComponent targetPopulation={targetPopulation} />
        )}
      </PaperContainer>
    </div>
  );
}