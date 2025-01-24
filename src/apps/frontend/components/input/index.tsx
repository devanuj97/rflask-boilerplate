import clsx from 'clsx';
import * as React from 'react';

import { Nullable } from '../../types/common-types';
import HorizontalStackLayout from '../layouts/horizontal-stack-layout';

import styles from './input.styles';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  endEnhancer?: React.ReactElement | string;
  error?: string;
  handleInputRef?: (ref: Nullable<HTMLInputElement>) => void;
  index?: number;
  startEnhancer?: React.ReactElement | string;
  testId?: string;
  textAlign?: 'left' | 'center' | 'right';
  type?: string;
}

const Input: React.FC<InputProps> = ({
  disabled,
  endEnhancer,
  error,
  handleInputRef,
  index,
  startEnhancer,
  testId,
  textAlign = 'left',
  type,
  ...props
}) => (
  <div
    className={clsx([
      styles.inputContainer,
      error ? styles.border.errorState : styles.border.normalState,
    ])}
  >
    <HorizontalStackLayout gap={2}>
      {startEnhancer && (
        <span className="flex h-full min-w-6 items-center justify-center">
          {startEnhancer}
        </span>
      )}
      <input
        {...props}
        autoComplete="off"
        disabled={disabled}
        className={clsx([
          styles.input,
          textAlign ? styles.textAlign[textAlign] : '',
        ])}
        data-testid={testId}
        type={type || 'text'}
        ref={handleInputRef ? (ref) => handleInputRef(ref) : null}
      />
      {endEnhancer && (
        <span className="flex h-full min-w-6 items-center justify-center">
          {endEnhancer}
        </span>
      )}
    </HorizontalStackLayout>
  </div>
);

export default Input;
