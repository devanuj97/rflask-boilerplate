import React, { ReactNode } from 'react';

const AuthenticationFormLayout: React.FC<{ children: ReactNode }> = ({
  children,
}) => (
  <div className="flex min-h-screen flex-wrap items-center justify-center p-4 md:p-6 2xl:p-10">
    <div className="w-full rounded-sm border border-stroke bg-white p-4 shadow-default dark:border-strokedark dark:bg-boxdark sm:p-12.5 md:w-4/5 xl:w-2/5">
      {children}
    </div>
  </div>
);

export default AuthenticationFormLayout;
