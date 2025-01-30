import clsx from 'clsx';
import React, { PropsWithChildren } from 'react';

import { ButtonKind, ButtonSize, ButtonType } from '../../types/button';
import HorizontalStackLayout from '../layouts/horizontal-stack-layout';
import Spinner from '../spinner/spinner';

import styles from './button.styles';

interface ButtonProps {
  disabled?: boolean;
  endEnhancer?: React.ReactElement | string;
  isLoading?: boolean;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
  size?: ButtonSize;
  startEnhancer?: React.ReactElement | string;
  type?: ButtonType;
  kind?: ButtonKind;
}

const Button: React.FC<PropsWithChildren<ButtonProps>> = ({
  children,
  disabled,
  endEnhancer,
  isLoading,
  onClick,
  size,
  startEnhancer,
  type = ButtonType.BUTTON,
  kind = ButtonKind.PRIMARY,
}) => {
  const content =
    isLoading && kind === ButtonKind.PRIMARY ? <Spinner /> : children;

  return (
    <button
      className={clsx([
        styles.kind[kind].base,
        disabled || isLoading
          ? styles.kind[kind].disableState
          : styles.kind[kind].enableState,
        size && styles.size[size],
      ])}
      disabled={disabled || isLoading}
      type={type}
      onClick={onClick}
    >
      <HorizontalStackLayout gap={2}>
        {startEnhancer && (
          <span className="flex h-full min-w-6 items-center justify-center">
            {startEnhancer}
          </span>
        )}
        {content}
        {endEnhancer && (
          <span className="flex h-full min-w-6 items-center justify-center">
            {endEnhancer}
          </span>
        )}
      </HorizontalStackLayout>
    </button>
  );
};

export default Button;
