import { useFormik } from 'formik';
import * as Yup from 'yup';

import constant from '../../../constants';
import { useAccountContext, useAuthContext } from '../../../contexts';
import { AsyncError } from '../../../types';

interface PasswordValidationFormProps {
  handleAccount: () => void;
  onValidationError: (error: AsyncError) => void;
}

const usePasswordValidationForm = ({
  handleAccount,
  onValidationError,
}: PasswordValidationFormProps) => {
  const { isLoginLoading, login, loginError, loginResult } = useAuthContext();
  const { accountDetails } = useAccountContext();

  const formik = useFormik({
    initialValues: {
      password: '',
    },
    validationSchema: Yup.object({
      password: Yup.string()
        .min(constant.PASSWORD_MIN_LENGTH, constant.PASSWORD_VALIDATION_ERROR)
        .required(constant.PASSWORD_VALIDATION_ERROR),
    }),
    onSubmit: (values) => {
      login(accountDetails.username, values.password)
        .then(() => {
          handleAccount();
        })
        .catch((error) => {
          onValidationError(error as AsyncError);
        });
    },
  });

  return {
    isLoginLoading,
    loginError,
    loginResult,
    formik,
  };
};

export default usePasswordValidationForm;
