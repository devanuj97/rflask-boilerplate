import React from 'react';

import {
  Button,
  H2,
  ParagraphSmall,
  VerticalStackLayout,
} from '../../../components';
import Modal from '../../../components/modal';
import { ButtonKind, ButtonSize } from '../../../types/button';

interface AccountDeletionModalProps {
  handleDeleteAccount: () => void;
  isDeleteAccountLoading: boolean;
  isModalOpen: boolean;
  setIsModalOpen: (isOpen: boolean) => void;
}

const AccountDeletionModal: React.FC<AccountDeletionModalProps> = ({
  handleDeleteAccount,
  isDeleteAccountLoading,
  isModalOpen,
  setIsModalOpen,
}) => (
  <Modal isModalOpen={isModalOpen}>
    <div className="absolute right-1 top-1 sm:right-5 sm:top-5">
      <Button
        kind={ButtonKind.TERTIARY}
        onClick={() => setIsModalOpen(false)}
        startEnhancer={
          <img src="assets/img/icon/close-icon.svg" alt="close-icon" />
        }
      />
    </div>
    <VerticalStackLayout gap={5}>
      <H2>Delete Account</H2>
      <ParagraphSmall>
        Are you sure you want to delete your account? This action cannot be
        undone!
      </ParagraphSmall>
      <div className="mt-6 flex items-center justify-end gap-4">
        <div>
          <Button
            onClick={() => setIsModalOpen(false)}
            kind={ButtonKind.SECONDARY}
          >
            Cancel
          </Button>
        </div>
        <div>
          <Button
            isLoading={isDeleteAccountLoading}
            onClick={() => handleDeleteAccount()}
            size={ButtonSize.DEFAULT}
            kind={ButtonKind.DANGER}
          >
            Delete Account
          </Button>
        </div>
      </div>
    </VerticalStackLayout>
  </Modal>
);

export default AccountDeletionModal;
