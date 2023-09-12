import { Box, FormControlLabel, Radio, RadioGroup } from '@material-ui/core';
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useLocation } from 'react-router-dom';
import styled from 'styled-components';
import {
  ProgramNode,
  RegistrationDataImportStatus,
  useAllProgramsForChoicesQuery,
  useHouseholdChoiceDataQuery,
} from '../../../../__generated__/graphql';
import { CommunicationTabsValues } from '../../../../utils/constants';
import { getFilterFromQueryParams } from '../../../../utils/utils';
import { LookUpHouseholdFiltersCommunication } from './LookUpHouseholdFiltersCommunication';
import { LookUpRegistrationFiltersCommunication } from './LookUpRegistrationFiltersCommunication';
import { LookUpSelectionTablesCommunication } from './LookUpSelectionTablesCommunication';
import { LookUpTargetPopulationFiltersCommunication } from './LookUpTargetPopulationFiltersCommunication';

const communicationTabs = ['Household', 'Target Population', 'RDI'];

const BoxWithBorderBottom = styled(Box)`
  border-bottom: 1px solid ${({ theme }) => theme.hctPalette.lighterGray};
  padding: 15px 0;
`;

export const LookUpSelectionCommunication = ({
  businessArea,
  onValueChange,
  setValues,
  values,
  selectedTab,
  setSelectedTab,
}: {
  businessArea: string;
  onValueChange;
  setValues;
  values;
  selectedTab;
  setSelectedTab;
}): React.ReactElement => {
  const location = useLocation();

  const initialFilterRDI = {
    search: '',
    importedBy: '',
    status: RegistrationDataImportStatus.Merged,
    sizeMin: '',
    sizeMax: '',
    importDateRangeMin: undefined,
    importDateRangeMax: undefined,
  };

  const [filterRDI, setFilterRDI] = useState(
    getFilterFromQueryParams(location, initialFilterRDI),
  );
  const [appliedFilterRDI, setAppliedFilterRDI] = useState(
    getFilterFromQueryParams(location, initialFilterRDI),
  );

  const initialFilterTP = {
    name: '',
    status: '',
    program: '',
    numIndividualsMin: null,
    numIndividualsMax: null,
    totalHouseholdsCountWithValidPhoneNoMin: null,
    totalHouseholdsCountWithValidPhoneNoMax: null,
  };

  const [filterTP, setFilterTP] = useState(
    getFilterFromQueryParams(location, initialFilterTP),
  );
  const [appliedFilterTP, setAppliedFilterTP] = useState(
    getFilterFromQueryParams(location, initialFilterTP),
  );

  const initialFilterHH = {
    search: '',
    searchType: 'household_id',
    program: '',
    residenceStatus: '',
    admin2: '',
    householdSizeMin: '',
    householdSizeMax: '',
    orderBy: 'unicef_id',
    withdrawn: null,
  };

  const [filterHH, setFilterHH] = useState(
    getFilterFromQueryParams(location, initialFilterHH),
  );
  const [appliedFilterHH, setAppliedFilterHH] = useState(
    getFilterFromQueryParams(location, initialFilterHH),
  );

  const { t } = useTranslation();

  const {
    data: choicesData,
    loading: choicesLoading,
  } = useHouseholdChoiceDataQuery({
    variables: { businessArea },
  });

  const { data, loading: programsLoading } = useAllProgramsForChoicesQuery({
    variables: { businessArea },
    fetchPolicy: 'cache-and-network',
  });

  const allPrograms = data?.allPrograms?.edges || [];
  const programs = allPrograms.map((edge) => edge.node);

  const handleChange = (type: number, value: string[] | string): void => {
    setValues({
      ...values,
      households:
        type === CommunicationTabsValues.HOUSEHOLD && typeof value !== 'string'
          ? value
          : [],
      targetPopulation:
        type === CommunicationTabsValues.TARGET_POPULATION &&
        typeof value === 'string'
          ? value
          : '',
      registrationDataImport:
        type === CommunicationTabsValues.RDI && typeof value === 'string'
          ? value
          : '',
    });
  };

  if (programsLoading || choicesLoading) return null;

  return (
    <Box>
      <BoxWithBorderBottom
        p={4}
        m={4}
        display='flex'
        alignItems='center'
        bgcolor='#F5F5F5'
      >
        <Box pr={5} fontWeight='500' fontSize='medium'>
          {t('Look up for')}
        </Box>
        <RadioGroup
          aria-labelledby='selection-radio-buttons-group'
          value={selectedTab}
          row
          name='radio-buttons-group'
        >
          {communicationTabs.map((tab, index) => (
            <FormControlLabel
              value={index}
              onChange={() => {
                setSelectedTab(index);
              }}
              control={<Radio color='primary' />}
              label={tab}
              key={tab}
            />
          ))}
        </RadioGroup>
      </BoxWithBorderBottom>
      <Box p={4} mt={4}>
        {selectedTab === CommunicationTabsValues.HOUSEHOLD && (
          <LookUpHouseholdFiltersCommunication
            programs={programs as ProgramNode[]}
            filter={filterHH}
            choicesData={choicesData}
            setFilter={setFilterHH}
            initialFilter={initialFilterHH}
            appliedFilter={appliedFilterHH}
            setAppliedFilter={setAppliedFilterHH}
          />
        )}
        {selectedTab === CommunicationTabsValues.TARGET_POPULATION && (
          <LookUpTargetPopulationFiltersCommunication
            filter={filterTP}
            programs={programs as ProgramNode[]}
            setFilter={setFilterTP}
            initialFilter={initialFilterTP}
            appliedFilter={appliedFilterTP}
            setAppliedFilter={setAppliedFilterTP}
            addBorder={false}
          />
        )}
        {selectedTab === CommunicationTabsValues.RDI && (
          <LookUpRegistrationFiltersCommunication
            filter={filterRDI}
            setFilter={setFilterRDI}
            initialFilter={initialFilterRDI}
            appliedFilter={appliedFilterRDI}
            setAppliedFilter={setAppliedFilterRDI}
            addBorder={false}
          />
        )}
      </Box>
      <LookUpSelectionTablesCommunication
        selectedTab={selectedTab}
        choicesData={choicesData}
        filtersHouseholdApplied={appliedFilterHH}
        filtersTargetPopulationApplied={appliedFilterTP}
        filtersRDIApplied={appliedFilterRDI}
        businessArea={businessArea}
        onValueChange={onValueChange}
        values={values}
        handleChange={handleChange}
      />
    </Box>
  );
};