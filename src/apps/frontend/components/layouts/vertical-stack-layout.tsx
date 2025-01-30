import React, { PropsWithChildren } from 'react';

interface VerticalStackLayoutProps {
  gap?: number;
}

const VerticalStackLayout: React.FC<
  PropsWithChildren<VerticalStackLayoutProps>
> = ({ children, gap = 0 }) => (
  // eslint-disable-next-line tailwindcss/no-custom-classname
  <div className={`gap-${gap} flex flex-col justify-center`}>{children}</div>
);

export default VerticalStackLayout;
