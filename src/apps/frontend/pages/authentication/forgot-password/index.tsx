import React, { useState } from 'react';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

import { Button, H2, VerticalStackLayout } from '../../../components';
import routes from '../../../constants/routes';
import { AsyncError } from '../../../types';
import { ButtonKind } from '../../../types/button';
import useTimer from '../../../utils/use-timer.hook';
import AuthenticationFormLayout from '../authentication-form-layout';
import AuthenticationPageLayout from '../authentication-page-layout';

import ForgotPasswordForm from './forgot-password-form';
import ForgotPasswordResendEmail from './forgot-password-resend-email';

export const ForgotPassword: React.FC = () => {
  const passwordResendDelayInSeconds = 60_000;

  const navigate = useNavigate();

  const [isResendEmailPage, setIsResendEmailPage] = useState(false);
  const [username, setUsername] = useState('');

  const { startTimer, remainingSecondsStr, isResendEnabled } = useTimer({
    delayInMilliseconds: passwordResendDelayInSeconds,
  });

  const onSendEmailSuccess = (newUsername: string) => {
    startTimer();
    setUsername(newUsername);
    setIsResendEmailPage(true);
  };

  const onResendEmailSuccess = () => {
    startTimer();
    toast.success(
      'A password reset link has been re-sent. Please check your inbox',
    );
  };

  const onError = (error: AsyncError) => {
    toast.error(error.message);
  };

  const handleBackButtonClick = () => {
    if (isResendEmailPage) {
      setIsResendEmailPage(false);
    } else {
      navigate(routes.LOGIN);
    }
  };

  return (
    <AuthenticationPageLayout>
      <AuthenticationFormLayout>
        <VerticalStackLayout gap={6}>
          <Button kind={ButtonKind.SECONDARY} onClick={handleBackButtonClick}>
            Back
          </Button>
          <H2>Forgot Password?</H2>
          {isResendEmailPage ? (
            <ForgotPasswordResendEmail
              isResendEnabled={isResendEnabled}
              onSuccess={onResendEmailSuccess}
              onError={onError}
              username={username}
              timerRemainingSeconds={remainingSecondsStr}
            />
          ) : (
            <ForgotPasswordForm
              onSuccess={onSendEmailSuccess}
              onError={onError}
            />
          )}
        </VerticalStackLayout>
      </AuthenticationFormLayout>
    </AuthenticationPageLayout>
  );
};

export default ForgotPassword;
