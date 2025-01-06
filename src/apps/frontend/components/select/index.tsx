import React from 'react';
import ErrorBoundary from '../../error/ErrorBoundary';

type OPTION = {
  label: string;
  value: string | number;
};

interface SelectProps {
  handleChange: (event: React.ChangeEvent<HTMLSelectElement>) => void;
  isLoading: boolean;
  multiple?: boolean;
  options: OPTION[];
  value: string | number;
}

const Select: React.FC<SelectProps> = ({
  handleChange,
  isLoading,
  multiple,
  options,
  value,
}) => (
  <ErrorBoundary>
    <select
      className="
      items-center
      justify-center
      rounded-lg
      border
      border-stroke
      bg-transparent
      px-2
      py-4
      text-lg
      outline-none
      focus:border-primary
      focus-visible:shadow-none
    "
      disabled={isLoading}
      multiple={multiple}
      onChange={handleChange}
      value={value}
    >
      {options.map((option, index) => (
        <ErrorBoundary>
          <option key={index} value={option.value}>
            {option.label}
          </option>
        </ErrorBoundary>
      ))}
    </select>
  </ErrorBoundary>
);

export default Select;
