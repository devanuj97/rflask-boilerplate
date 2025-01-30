import React from 'react';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

import { Button, H2, VerticalStackLayout } from '../../../components';
import constant from '../../../constants';
import routes from '../../../constants/routes';
import { AsyncError } from '../../../types';
import { ButtonKind } from '../../../types/button';
import useTimer from '../../../utils/use-timer.hook';
import AuthenticationFormLayout from '../authentication-form-layout';
import AuthenticationPageLayout from '../authentication-page-layout';

import OTPForm from './otp-form';

export const OTPPage: React.FC = () => {
  const { startTimer, remainingSecondsStr, isResendEnabled } = useTimer({
    delayInMilliseconds: constant.SEND_OTP_DELAY_IN_MS,
  });

  const navigate = useNavigate();

  const onVerifyOTPSuccess = () => {
    navigate(routes.DASHBOARD);
  };

  const onResendOTPSuccess = () => {
    startTimer();
    toast.success(
      'OTP has been successfully re-sent. Please check your messages.',
    );
  };

  const onError = (error: AsyncError) => {
    toast.error(error.message);
  };

  const handleBackButtonClick = () => {
    navigate(routes.PHONE_LOGIN);
  };

  return (
    <AuthenticationPageLayout>
      <AuthenticationFormLayout>
        <VerticalStackLayout gap={8}>
          <Button kind={ButtonKind.SECONDARY} onClick={handleBackButtonClick}>
            Back
          </Button>
          <H2>Verify Your Account</H2>
          <OTPForm
            isResendEnabled={isResendEnabled}
            onError={onError}
            onResendOTPSuccess={onResendOTPSuccess}
            onVerifyOTPSuccess={onVerifyOTPSuccess}
            timerRemainingSeconds={remainingSecondsStr}
          />
        </VerticalStackLayout>
      </AuthenticationFormLayout>
    </AuthenticationPageLayout>
  );
};

export default OTPPage;
