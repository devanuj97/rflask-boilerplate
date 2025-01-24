import React, { ReactNode } from 'react';

const H3: React.FC<{ children: ReactNode }> = ({ children }) => (
  <h3 className="text-lg font-medium text-black">{children}</h3>
);

export default H3;
