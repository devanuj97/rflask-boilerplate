import React, { ReactNode } from 'react';

const ParagraphSmall: React.FC<{ children: ReactNode }> = ({ children }) => (
  <p className="text-base font-medium">{children}</p>
);

export default ParagraphSmall;
