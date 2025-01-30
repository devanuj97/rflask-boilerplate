import React, { ReactNode } from 'react';

const ParagraphMedium: React.FC<{ children: ReactNode }> = ({ children }) => (
  <p className="text-xl font-medium">{children}</p>
);

export default ParagraphMedium;
