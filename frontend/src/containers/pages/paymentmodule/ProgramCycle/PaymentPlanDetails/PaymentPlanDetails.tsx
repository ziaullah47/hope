import { Grid, Typography } from '@mui/material';
import * as React from 'react';
import { useTranslation } from 'react-i18next';
import { renderUserName } from '@utils/utils';
import { PaymentPlanQuery } from '@generated/graphql';
import { ContainerColumnWithBorder } from '@core/ContainerColumnWithBorder';
import { LabelizedField } from '@core/LabelizedField';
import { OverviewContainer } from '@core/OverviewContainer';
import { Title } from '@core/Title';
import { UniversalMoment } from '@core/UniversalMoment';
import { FieldBorder } from '@core/FieldBorder';
import { RelatedFollowUpPaymentPlans } from '@components/paymentmodule/PaymentPlanDetails/PaymentPlanDetails/RelatedFollowUpPaymentPlans';

interface PaymentPlanDetailsProps {
  baseUrl: string;
  paymentPlan: PaymentPlanQuery['paymentPlan'];
}

export const PaymentPlanDetails = ({
  baseUrl,
  paymentPlan,
}: PaymentPlanDetailsProps): React.ReactElement => {
  const { t } = useTranslation();
  const {
    createdBy,
    currency,
    startDate,
    endDate,
    dispersionStartDate,
    dispersionEndDate,
    followUps,
  } = paymentPlan;

  return (
    <Grid item xs={12}>
      <ContainerColumnWithBorder>
        <Title>
          <Typography variant="h6">{t('Details')}</Typography>
        </Title>
        <OverviewContainer>
          <Grid container>
            <Grid container item xs={9} spacing={6}>
              <Grid item xs={3}>
                <LabelizedField label={t('Created By')}>
                  {renderUserName(createdBy)}
                </LabelizedField>
              </Grid>
              <Grid item xs={3}>
                <LabelizedField label={t('Start Date')}>
                  <UniversalMoment>{startDate}</UniversalMoment>
                </LabelizedField>
              </Grid>
              <Grid item xs={3}>
                <LabelizedField label={t('End Date')}>
                  <UniversalMoment>{endDate}</UniversalMoment>
                </LabelizedField>
              </Grid>
              <Grid item xs={3}>
                <LabelizedField label={t('Currency')}>
                  {currency}
                </LabelizedField>
              </Grid>
              <Grid item xs={3}>
                <LabelizedField label={t('Dispersion Start Date')}>
                  <UniversalMoment>{dispersionStartDate}</UniversalMoment>
                </LabelizedField>
              </Grid>
              <Grid item xs={3}>
                <LabelizedField label={t('Dispersion End Date')}>
                  <UniversalMoment>{dispersionEndDate}</UniversalMoment>
                </LabelizedField>
              </Grid>
            </Grid>
            <Grid container direction="column" item xs={3} spacing={6}>
              <Grid item xs={12}>
                <FieldBorder color="#84A1CA">
                  <RelatedFollowUpPaymentPlans
                    followUps={followUps}
                    baseUrl={baseUrl}
                  />
                </FieldBorder>
              </Grid>
            </Grid>
          </Grid>
        </OverviewContainer>
      </ContainerColumnWithBorder>
    </Grid>
  );
};
