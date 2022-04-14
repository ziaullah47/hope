import { Box, Paper, Typography } from '@material-ui/core';
import React from 'react';
import { useTranslation } from 'react-i18next';
import styled from 'styled-components';
import { useBusinessArea } from '../../hooks/useBusinessArea';
import { GrievanceTicketQuery } from '../../__generated__/graphql';
import { ContentLink } from '../core/ContentLink';
import { Title } from '../core/Title';

const StyledBox = styled(Paper)`
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 26px 22px;
`;

export const PaymentIds = ({
  verifications,
}: {
  verifications: GrievanceTicketQuery['grievanceTicket']['paymentVerificationTicketDetails']['paymentVerifications']['edges'];
}): React.ReactElement => {
  const { t } = useTranslation();
  const businessArea = useBusinessArea();

  const mappedIds = verifications.map(
    (verification): React.ReactElement => (
      <Box mb={1}>
        <ContentLink
          href={`/${businessArea}/verification-records/${verification.node.id}`}
        >
          {verification.node.paymentRecord.caId}
        </ContentLink>
      </Box>
    ),
  );
  return (
    <StyledBox>
      <Title>
        <Typography variant='h6'>{t('Payment Ids')}</Typography>
      </Title>
      <Box display='flex' flexDirection='column'>
        {mappedIds}
      </Box>
    </StyledBox>
  );
};