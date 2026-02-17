import React from 'react';

interface BaseInputProps {
  label?: string;
  error?: string;
  helperText?: string;
  fullWidth?: boolean;
}

interface TextInputProps extends BaseInputProps, Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  type?: 'text' | 'email' | 'password' | 'number' | 'search' | 'tel' | 'url';
}

interface TextareaInputProps extends BaseInputProps, React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  type: 'textarea';
}

type InputProps = TextInputProps | TextareaInputProps;

export const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  fullWidth = false,
  className = '',
  type = 'text',
  ...props
}) => {
  const containerClasses = `mb-4 ${fullWidth ? 'w-full' : 'w-full max-w-md'}`;
  const baseClasses = 'block w-full rounded-lg border-[rgb(var(--border-rgb))] shadow-sm focus:ring-2 focus:ring-[rgb(var(--primary-rgb))] focus:border-[rgb(var(--primary-rgb))] sm:text-sm transition-colors duration-200';
  const errorClasses = error ? 'border-red-300 focus:ring-red-500 focus:border-red-500' : 'focus:ring-[rgb(var(--primary-rgb))] focus:border-[rgb(var(--primary-rgb))]';
  const elementClasses = `${baseClasses} ${errorClasses} ${className} py-3 px-4 bg-white`;

  const uniqueId = (props as any).id || `input-${Math.random().toString(36).substr(2, 9)}`;

  return (
    <div className={containerClasses}>
      {label && (
        <label htmlFor={uniqueId} className="block text-sm font-medium text-gray-700 mb-2">
          {label}
          {(props as any).required && <span className="text-red-500 ml-1" aria-label="required">*</span>}
        </label>
      )}
      {type === 'textarea' ? (
        <textarea
          id={uniqueId}
          className={elementClasses}
          aria-invalid={!!error}
          aria-describedby={error || helperText ? `${uniqueId}-feedback` : undefined}
          {...props as React.TextareaHTMLAttributes<HTMLTextAreaElement>}
        />
      ) : (
        <input
          id={uniqueId}
          className={elementClasses}
          aria-invalid={!!error}
          aria-describedby={error || helperText ? `${uniqueId}-feedback` : undefined}
          type={type}
          {...props as React.InputHTMLAttributes<HTMLInputElement>}
        />
      )}
      {(error || helperText) && (
        <p
          id={`${uniqueId}-feedback`}
          className={`mt-2 text-sm ${error ? 'text-red-600' : 'text-gray-500'}`}
          role={error ? 'alert' : undefined}
        >
          {error || helperText}
        </p>
      )}
    </div>
  );
};