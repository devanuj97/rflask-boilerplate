import React, { ReactNode } from 'react';

const AuthenticationPageLayout: React.FC<{ children: ReactNode }> = ({
  children,
}) => (
  <div className="rounded-sm border border-stroke shadow-default dark:border-strokedark dark:bg-boxdark">
    {children}
  </div>
);

export default AuthenticationPageLayout;
