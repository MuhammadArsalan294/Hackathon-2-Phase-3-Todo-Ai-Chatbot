'use client';

import React from 'react';
import { Input } from './Input';

interface PasswordFieldProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  fullWidth?: boolean;
  showVisibilityToggle?: boolean;
}

export const PasswordField: React.FC<PasswordFieldProps> = ({
  label = 'Password',
  error,
  helperText,
  fullWidth = false,
  showVisibilityToggle = true,
  className = '',
  ...props
}) => {
  return (
    <div>
      <Input
        label={label}
        type="password"
        error={error}
        helperText={helperText}
        fullWidth={fullWidth}
        className={className}
        placeholder={props.placeholder || '••••••••'}
        {...props}
        autoComplete={props.autoComplete || 'current-password'}
      />
    </div>
  );
};