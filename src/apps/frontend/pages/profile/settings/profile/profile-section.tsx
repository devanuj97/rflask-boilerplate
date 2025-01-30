import React from 'react';

import { H3 } from '../../../../components';
import { Account } from '../../../../types';

import ProfileForm from './profile-form';

interface ProfileSectionProps {
  accountDetails: Account;
}

const ProfileSection: React.FC<ProfileSectionProps> = ({ accountDetails }) => (
  <div className="col-span-5 xl:col-span-3">
    <div className="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
      <div className="border-b border-stroke px-7 py-4 dark:border-strokedark">
        <H3>Personal Information</H3>
      </div>
      <div className="p-7">
        <ProfileForm accountDetails={accountDetails} />
      </div>
    </div>
  </div>
);

export default ProfileSection;
