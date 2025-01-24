import React, { useState } from 'react';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

import { H2, Spinner, VerticalStackLayout } from '../../../components';
import routes from '../../../constants/routes';
import { useAccountContext, useAuthContext } from '../../../contexts';
import { AsyncError } from '../../../types';

import AccountActionsSection from './account-actions-section';
import AccountDeletionModal from './account-deletion-modal';
import PersonalInfoSection from './personal-info-section';

const ProfileSettings = () => {
  const {
    accountDetails,
    isAccountLoading,
    deleteAccount,
    isDeleteAccountLoading,
  } = useAccountContext();
  const { logout } = useAuthContext();
  const navigate = useNavigate();

  const [isDeleteAccountModalOpen, setIsDeleteAccountModalOpen] =
    useState(false);

  const handleLogout = () => {
    logout();
    navigate(routes.LOGIN);
  };

  const onAccountDeletionError = (err: AsyncError) => {
    toast.error(err.message);
  };

  const handleDeleteAccount = () => {
    deleteAccount()
      .then(() => {
        toast.success('Account deleted successfully');
        handleLogout();
      })
      .catch((err) => {
        onAccountDeletionError(err as AsyncError);
      });
  };

  const handleResetPasswordClick = () => {
    navigate(routes.FORGOT_PASSWORD);
  };

  return isAccountLoading ? (
    <Spinner />
  ) : (
    <div className="container mx-auto p-7">
      <VerticalStackLayout gap={7}>
        <H2>Settings</H2>
        <div className="grid grid-cols-5 gap-8">
          <PersonalInfoSection accountDetails={accountDetails} />
          <AccountActionsSection
            accountDetails={accountDetails}
            setIsDeleteAccountModalOpen={setIsDeleteAccountModalOpen}
            handleLogout={handleLogout}
            handleResetPassword={handleResetPasswordClick}
          />
        </div>
        <AccountDeletionModal
          handleDeleteAccount={handleDeleteAccount}
          isModalOpen={isDeleteAccountModalOpen}
          setIsModalOpen={setIsDeleteAccountModalOpen}
          isDeleteAccountLoading={isDeleteAccountLoading}
        />
      </VerticalStackLayout>
    </div>
  );
};

export default ProfileSettings;
