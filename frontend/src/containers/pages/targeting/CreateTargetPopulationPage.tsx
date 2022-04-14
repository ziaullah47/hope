import { FieldArray, Form, Formik } from 'formik';
import React from 'react';
import { useTranslation } from 'react-i18next';
import * as Yup from 'yup';
import { LoadingComponent } from '../../../components/core/LoadingComponent';
import { PermissionDenied } from '../../../components/core/PermissionDenied';
import { CreateTargetPopulationHeader } from '../../../components/targeting/CreateTargetPopulation/CreateTargetPopulationHeader';
import { EmptyTargetingCriteria } from '../../../components/targeting/CreateTargetPopulation/EmptyTargetingCriteria';
import { Exclusions } from '../../../components/targeting/CreateTargetPopulation/Exclusions';
import { Results } from '../../../components/targeting/Results';
import { TargetingCriteria } from '../../../components/targeting/TargetingCriteria';
import { TargetingCriteriaDisabled } from '../../../components/targeting/TargetingCriteria/TargetingCriteriaDisabled';
import { TargetPopulationProgramme } from '../../../components/targeting/TargetPopulationProgramme';
import { hasPermissions, PERMISSIONS } from '../../../config/permissions';
import { useBusinessArea } from '../../../hooks/useBusinessArea';
import { usePermissions } from '../../../hooks/usePermissions';
import { useSnackbar } from '../../../hooks/useSnackBar';
import { getTargetingCriteriaVariables } from '../../../utils/targetingUtils';
import {
  getFullNodeFromEdgesById,
  handleValidationErrors,
} from '../../../utils/utils';
import {
  useAllProgramsQuery,
  useCreateTpMutation,
} from '../../../__generated__/graphql';
import { CreateTable } from '../../tables/targeting/TargetPopulation/Create';

export function CreateTargetPopulationPage(): React.ReactElement {
  const { t } = useTranslation();
  const initialValues = {
    name: '',
    criterias: [],
    program: null,
    excludedIds: '',
    exclusionReason: '',
  };
  const [mutate] = useCreateTpMutation();
  const { showMessage } = useSnackbar();
  const businessArea = useBusinessArea();
  const permissions = usePermissions();

  const {
    data: allProgramsData,
    loading: loadingPrograms,
  } = useAllProgramsQuery({
    variables: { businessArea, status: ['ACTIVE'] },
  });

  if (loadingPrograms) return <LoadingComponent />;
  if (permissions === null) return null;
  if (!hasPermissions(PERMISSIONS.TARGETING_CREATE, permissions))
    return <PermissionDenied />;

  const validationSchema = Yup.object().shape({
    name: Yup.string()
      .min(2, t('Too short'))
      .max(255, t('Too long')),
    excludedIds: Yup.string().test(
      'testName',
      'ID is not in the correct format',
      (ids) => {
        if (!ids?.length) {
          return true;
        }
        const idsArr = ids.split(',');
        return idsArr.every((el) =>
          /^\s*(IND|HH)-\d{2}-\d{4}\.\d{4}\s*$/.test(el),
        );
      },
    ),
    exclusionReason: Yup.string().max(500, t('Too long')),
  });

  const handleSubmit = async (values, { setFieldError }): Promise<void> => {
    try {
      const res = await mutate({
        variables: {
          input: {
            programId: values.program,
            name: values.name,
            excludedIds: values.excludedIds,
            exclusionReason: values.exclusionReason,
            businessAreaSlug: businessArea,
            ...getTargetingCriteriaVariables(values),
          },
        },
      });
      showMessage(t('Target Population Created'), {
        pathname: `/${businessArea}/target-population/${res.data.createTargetPopulation.targetPopulation.id}`,
        historyMethod: 'push',
      });
    } catch (e) {
      const { nonValidationErrors } = handleValidationErrors(
        'createTargetPopulation',
        e,
        setFieldError,
        showMessage,
      );
      if (nonValidationErrors.length > 0) {
        showMessage(t('Unexpected problem while creating Target Population'));
      }
    }
  };

  return (
    <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={handleSubmit}
    >
      {({ submitForm, values }) => (
        <Form>
          <CreateTargetPopulationHeader
            handleSubmit={submitForm}
            values={values}
            businessArea={businessArea}
            permissions={permissions}
          />
          <TargetPopulationProgramme
            allPrograms={allProgramsData}
            loading={loadingPrograms}
            program={values.program}
          />
          {values.program ? (
            <FieldArray
              name='criterias'
              render={(arrayHelpers) => (
                <TargetingCriteria
                  helpers={arrayHelpers}
                  candidateListRules={values.criterias}
                  isEdit
                  selectedProgram={getFullNodeFromEdgesById(
                    allProgramsData?.allPrograms?.edges,
                    values.program,
                  )}
                />
              )}
            />
          ) : (
            <TargetingCriteriaDisabled />
          )}
          <Exclusions />
          <Results />
          {values.criterias.length ? (
            <CreateTable
              variables={{
                ...getTargetingCriteriaVariables(values),
                excludedIds: values.excludedIds,
              }}
              program={values.program}
              businessArea={businessArea}
            />
          ) : (
            <EmptyTargetingCriteria />
          )}
        </Form>
      )}
    </Formik>
  );
}