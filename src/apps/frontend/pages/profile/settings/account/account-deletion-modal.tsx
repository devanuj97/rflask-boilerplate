import React from 'react';

import {
  Button,
  H2,
  ParagraphSmall,
  VerticalStackLayout,
} from '../../../../components';
import Modal from '../../../../components/modal';
import { AsyncError } from '../../../../types';
import { ButtonKind } from '../../../../types/button';
import PasswordValidationForm from '../password-validation-form';

interface AccountDeletionModalProps {
  handleDeleteAccount: () => void;
  isDeleteAccountLoading: boolean;
  onValidationError: (error: AsyncError) => void;
  isModalOpen: boolean;
  setIsModalOpen: (isOpen: boolean) => void;
}

const AccountDeletionModal: React.FC<AccountDeletionModalProps> = ({
  handleDeleteAccount,
  isDeleteAccountLoading,
  onValidationError,
  isModalOpen,
  setIsModalOpen,
}) => (
  <Modal isModalOpen={isModalOpen}>
    <div className="absolute right-1 top-1 sm:right-5 sm:top-5">
      <Button
        kind={ButtonKind.TERTIARY}
        onClick={() => setIsModalOpen(false)}
        startEnhancer={
          <img
            src="../../../../../../assets/img/icon/close-icon.svg"
            alt="close-icon"
          />
        }
      />
    </div>
    <VerticalStackLayout gap={5}>
      <H2>Delete Account</H2>
      <ParagraphSmall>
        Please enter your password to delete your account.
      </ParagraphSmall>
      <PasswordValidationForm
        handleAccount={handleDeleteAccount}
        isDeleteAccountLoading={isDeleteAccountLoading}
        onValidationError={onValidationError}
      />
    </VerticalStackLayout>
  </Modal>
);

export default AccountDeletionModal;
