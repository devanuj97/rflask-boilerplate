import React from 'react';

import { Button, H3 } from '../../../components';
import { Account } from '../../../types';
import { ButtonKind, ButtonSize } from '../../../types/button';

interface AccountActionsSectionProps {
  accountDetails: Account;
  handleLogout: () => void;
  handleResetPassword: () => void;
  setIsDeleteAccountModalOpen: (isOpen: boolean) => void;
}

const AccountActionsSection: React.FC<AccountActionsSectionProps> = ({
  accountDetails,
  handleLogout,
  handleResetPassword,
  setIsDeleteAccountModalOpen,
}) => (
  <div className="col-span-5 xl:col-span-2">
    <div className="flex flex-col rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
      <div className="border-b border-stroke px-7 py-4 dark:border-strokedark">
        <H3>Account Actions</H3>
      </div>

      <div className="flex flex-col gap-4 p-7">
        <Button onClick={handleLogout} size={ButtonSize.LARGE}>
          Log Out
        </Button>
        {accountDetails.username && (
          <Button onClick={handleResetPassword} size={ButtonSize.LARGE}>
            Reset Password
          </Button>
        )}
        <Button
          onClick={() => setIsDeleteAccountModalOpen(true)}
          size={ButtonSize.LARGE}
          kind={ButtonKind.DANGER}
        >
          Delete Account
        </Button>
      </div>
    </div>
  </div>
);

export default AccountActionsSection;
