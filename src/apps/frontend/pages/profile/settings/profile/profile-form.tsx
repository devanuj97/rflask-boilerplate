import React from 'react';

import { FormControl, Input } from '../../../../components';
import { Account } from '../../../../types';

interface ProfileFormProps {
  accountDetails: Account;
}

const ProfileForm: React.FC<ProfileFormProps> = ({ accountDetails }) => (
  <form action="#">
    {accountDetails.firstName && (
      <div className="mb-5.5 flex flex-col gap-5.5 sm:flex-row">
        <div className="w-full sm:w-1/2">
          <FormControl label="First Name" error="">
            <Input
              defaultValue={accountDetails.firstName}
              disabled={true}
              error={''}
            />
          </FormControl>
        </div>
        <div className="w-full sm:w-1/2">
          <FormControl label="Last Name" error="">
            <Input
              defaultValue={accountDetails.lastName}
              disabled={true}
              error={''}
            />
          </FormControl>
        </div>
      </div>
    )}
    <div className="mb-5.5">
      {accountDetails.username && (
        <FormControl label="Email" error="">
          <Input
            defaultValue={accountDetails.username}
            disabled={true}
            error={''}
          />
        </FormControl>
      )}
      {accountDetails.phoneNumber && (
        <FormControl label="Phone Number" error="">
          <Input
            defaultValue={accountDetails.phoneNumber.displayPhoneNumber()}
            disabled={true}
            error={''}
          />
        </FormControl>
      )}
    </div>
  </form>
);

export default ProfileForm;
