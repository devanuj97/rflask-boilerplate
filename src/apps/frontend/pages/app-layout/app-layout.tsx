import React, { PropsWithChildren, ReactNode } from 'react';

import { Header } from '../../components';
import Sidebar from '../../components/sidebar';

export const AppLayout: React.FC<PropsWithChildren<ReactNode>> = ({
  children,
}) => {
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(false);

  return (
    <div className="dark:bg-boxdark-2 dark:text-bodydark">
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          isSidebarOpen={isSidebarOpen}
          setIsSidebarOpen={setIsSidebarOpen}
        />

        <div className="relative flex flex-1 flex-col">
          {/* Header */}
          <Header
            isSidebarOpen={isSidebarOpen}
            setIsSidebarOpen={setIsSidebarOpen}
          />

          {/* Main Content */}
          <main className="overflow-y-auto">{children}</main>
        </div>
      </div>
    </div>
  );
};

export default AppLayout;
