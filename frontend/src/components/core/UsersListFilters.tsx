import { FormControl, Grid, InputAdornment, MenuItem } from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import React from 'react';
import { useTranslation } from 'react-i18next';
import styled from 'styled-components';
import InputLabel from '../../shared/InputLabel';
import Select from '../../shared/Select';
import TextField from '../../shared/TextField';
import { useUserChoiceDataQuery } from '../../__generated__/graphql';
import { ContainerWithBorder } from './ContainerWithBorder';

const StyledFormControl = styled(FormControl)`
  width: 232px;
  color: #5f6368;
  border-bottom: 0;
`;

const SearchTextField = styled(TextField)`
  flex: 1;
  && {
    min-width: 150px;
  }
`;

interface UsersListFiltersProps {
  onFilterChange;
  filter;
}
export function UsersListFilters({
  onFilterChange,
  filter,
}: UsersListFiltersProps): React.ReactElement {
  const { t } = useTranslation();
  const handleFilterChange = (e, name): void =>
    onFilterChange({ ...filter, [name]: e.target.value });
  const { data: choices } = useUserChoiceDataQuery();
  if (!choices) {
    return null;
  }

  return (
    <ContainerWithBorder>
      <Grid container spacing={3}>
        <Grid item>
          <SearchTextField
            label={t('Search')}
            variant='outlined'
            margin='dense'
            onChange={(e) => handleFilterChange(e, 'search')}
            InputProps={{
              startAdornment: (
                <InputAdornment position='start'>
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
        </Grid>
        <Grid item>
          <StyledFormControl variant='outlined' margin='dense'>
            <InputLabel>{t('Partner')}</InputLabel>
            <Select
              /* eslint-disable-next-line @typescript-eslint/ban-ts-ignore */
              // @ts-ignore
              onChange={(e) => handleFilterChange(e, 'partner')}
              variant='outlined'
              label={t('Partner')}
              value={filter.partner || ''}
            >
              <MenuItem value=''>
                <em>{t('None')}</em>
              </MenuItem>
              {choices.userPartnerChoices.map((item) => {
                return (
                  <MenuItem key={item.value} value={item.value}>
                    {item.name}
                  </MenuItem>
                );
              })}
            </Select>
          </StyledFormControl>
        </Grid>
        <Grid item>
          <StyledFormControl variant='outlined' margin='dense'>
            <InputLabel>{t('Role')}</InputLabel>
            <Select
              /* eslint-disable-next-line @typescript-eslint/ban-ts-ignore */
              // @ts-ignore
              onChange={(e) => handleFilterChange(e, 'roles')}
              variant='outlined'
              label={t('Role')}
              value={filter.roles || ''}
            >
              <MenuItem value=''>
                <em>{t('None')}</em>
              </MenuItem>
              {choices.userRolesChoices.map((item) => {
                return (
                  <MenuItem key={item.value} value={item.value}>
                    {item.name}
                  </MenuItem>
                );
              })}
            </Select>
          </StyledFormControl>
        </Grid>
        <Grid item>
          <StyledFormControl variant='outlined' margin='dense'>
            <InputLabel>{t('Status')}</InputLabel>
            <Select
              /* eslint-disable-next-line @typescript-eslint/ban-ts-ignore */
              // @ts-ignore
              onChange={(e) => handleFilterChange(e, 'status')}
              variant='outlined'
              label={t('Status')}
              value={filter.status || ''}
            >
              <MenuItem value=''>
                <em>{t('None')}</em>
              </MenuItem>
              {choices.userStatusChoices.map((item) => {
                return (
                  <MenuItem key={item.value} value={item.value}>
                    {item.name}
                  </MenuItem>
                );
              })}
            </Select>
          </StyledFormControl>
        </Grid>
      </Grid>
    </ContainerWithBorder>
  );
}