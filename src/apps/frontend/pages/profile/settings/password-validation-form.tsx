import React from 'react';

import {
  VerticalStackLayout,
  FormControl,
  PasswordInput,
  Button,
} from '../../../components';
import { AsyncError } from '../../../types';
import { ButtonType, ButtonKind, ButtonSize } from '../../../types/button';

import usePasswordValidationForm from './password-validation-form.hook';

interface PasswordValidationFormProps {
  handleAccount: () => void;
  isDeleteAccountLoading: boolean;
  onValidationError: (error: AsyncError) => void;
}

const PasswordValidationForm: React.FC<PasswordValidationFormProps> = ({
  handleAccount,
  isDeleteAccountLoading,
  onValidationError,
}) => {
  const { formik } = usePasswordValidationForm({
    handleAccount,
    onValidationError,
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <VerticalStackLayout gap={5}>
        <FormControl
          label={'Password'}
          error={formik.touched.password ? formik.errors.password : ''}
        >
          <PasswordInput
            error={formik.touched.password ? formik.errors.password : ''}
            name="password"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            placeholder="Enter your password"
            value={formik.values.password}
          />
        </FormControl>

        <Button
          type={ButtonType.SUBMIT}
          size={ButtonSize.LARGE}
          kind={ButtonKind.DANGER}
          isLoading={isDeleteAccountLoading}
        >
          Delete Account
        </Button>
      </VerticalStackLayout>
    </form>
  );
};

export default PasswordValidationForm;
