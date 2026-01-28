import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'outline' | 'ghost' | 'link';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  fullWidth?: boolean;
  icon?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  fullWidth = false,
  icon = false,
  className = '',
  disabled,
  ...props
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-200 focus-ring';

  const variantClasses = {
    primary: 'bg-[rgb(var(--primary-rgb))] hover:bg-[rgb(var(--primary-hover-rgb))] focus:ring-[rgb(var(--primary-rgb))] text-white shadow-light hover:shadow-medium',
    secondary: 'bg-[rgb(var(--secondary-rgb))] hover:bg-[rgb(var(--secondary-hover-rgb))] focus:ring-[rgb(var(--secondary-rgb))] text-white shadow-light hover:shadow-medium',
    danger: 'bg-[rgb(var(--danger-rgb))] hover:bg-[rgb(var(--danger-hover-rgb))] focus:ring-[rgb(var(--danger-rgb))] text-white shadow-light hover:shadow-medium',
    outline: 'border border-[rgb(var(--border-rgb))] bg-white hover:bg-gray-50 focus:ring-[rgb(var(--primary-rgb))] text-[rgb(var(--text-primary-rgb))] shadow-light hover:shadow-medium',
    ghost: 'bg-transparent hover:bg-gray-100 focus:ring-[rgb(var(--primary-rgb))] text-[rgb(var(--text-primary-rgb))] hover:text-[rgb(var(--primary-rgb))]',
    link: 'bg-transparent hover:underline focus:ring-[rgb(var(--primary-rgb))] text-[rgb(var(--primary-rgb))] underline-offset-4 hover:no-underline',
  };

  const sizeClasses = {
    sm: icon ? 'p-1.5' : 'text-sm px-3 py-1.5',
    md: icon ? 'p-2' : 'text-sm px-4 py-2',
    lg: icon ? 'p-2.5' : 'text-base px-6 py-3',
  };

  const widthClass = fullWidth ? 'w-full' : '';

  const disabledClasses = disabled || loading
    ? '!bg-gray-300 !hover:bg-gray-300 !cursor-not-allowed opacity-70'
    : '';

  const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${widthClass} ${disabledClasses} ${className}`;

  return (
    <button
      className={classes}
      disabled={disabled || loading}
      aria-disabled={disabled || loading}
      role="button"
      {...props}
    >
      {loading ? (
        <span className="flex items-center justify-center">
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" aria-hidden="true">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>Loading...</span>
        </span>
      ) : (
        children
      )}
    </button>
  );
};