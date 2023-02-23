import { Box, Button } from '@material-ui/core';
import { GetApp } from '@material-ui/icons';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { useSnackbar } from '../../../../../hooks/useSnackBar';
import {
  PaymentPlanQuery,
  useExportXlsxPpListPerFspMutation,
} from '../../../../../__generated__/graphql';
import { LoadingButton } from '../../../../core/LoadingButton';

export interface AcceptedPaymentPlanHeaderButtonsProps {
  canDownloadXlsx: boolean;
  canSendToFsp: boolean;
  paymentPlan: PaymentPlanQuery['paymentPlan'];
}

export const AcceptedPaymentPlanHeaderButtons = ({
  canDownloadXlsx,
  canSendToFsp,
  paymentPlan,
}: AcceptedPaymentPlanHeaderButtonsProps): React.ReactElement => {
  const { t } = useTranslation();
  const { showMessage } = useSnackbar();
  const [
    mutateExport,
    { loading: loadingExport },
  ] = useExportXlsxPpListPerFspMutation();

  return (
    <Box display='flex' alignItems='center'>
      {canDownloadXlsx && (
        <>
          {!paymentPlan.hasPaymentListExportFile ? (
            <Box p={2}>
              <LoadingButton
                loading={loadingExport}
                disabled={loadingExport || !paymentPlan.hasFspDeliveryMechanismXlsxTemplate}
                color='primary'
                variant='contained'
                startIcon={<GetApp />}
                data-cy='button-export-xlsx'
                onClick={async () => {
                  try {
                    await mutateExport({
                      variables: {
                        paymentPlanId: paymentPlan.id,
                      },
                    });
                    showMessage(t('Exporting XLSX started'));
                  } catch (e) {
                    e.graphQLErrors.map((x) => showMessage(x.message));
                  }
                }}
              >
                {t('Export Xlsx')}
              </LoadingButton>
            </Box>
          ) : (
            <Box m={2}>
              <Button
                color='primary'
                component='a'
                variant='contained'
                data-cy='button-download-xlsx'
                download
                href={`/api/download-payment-plan-payment-list/${paymentPlan.id}`}
                disabled={!paymentPlan.hasFspDeliveryMechanismXlsxTemplate}
              >
                {t('Download XLSX')}
              </Button>
            </Box>
          )}
        </>
      )}
      {canSendToFsp && (
        <Box m={2}>
          {/*TODO: connect this button*/}
          <Button color='primary' variant='contained'>
            {t('Send to FSP')}
          </Button>
        </Box>
      )}
    </Box>
  );
};