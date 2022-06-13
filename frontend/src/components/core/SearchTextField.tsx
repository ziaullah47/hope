import { InputAdornment } from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';
import styled from 'styled-components';
import React from 'react';
import TextField from '../../shared/TextField';

const StyledTextField = styled(TextField)`
  flex: 1;
  && {
    min-width: 150px;
  }
`;
export const SearchTextField = ({ ...props }): React.ReactElement => {
  return (
    <StyledTextField
      {...props}
      variant='outlined'
      margin='dense'
      InputProps={{
        startAdornment: (
          <InputAdornment position='start'>
            <SearchIcon />
          </InputAdornment>
        ),
      }}
    />
  );
};