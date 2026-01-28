'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Input } from '@/components/ui/Input';
import { PasswordField } from '@/components/ui/PasswordField';
import { Button } from '@/components/ui/Button';
import { apiClient } from '@/lib/api/client';
import { useAuth } from '@/lib/auth';

interface LoginFormProps {
  mode: 'signup' | 'signin';
}

export const LoginForm: React.FC<LoginFormProps> = ({ mode }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { signin, signup } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (mode === 'signup') {
        await signup(email, password, name);
      } else {
        await signin(email, password);
      }
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  // Password strength validation (for signup mode)
  const validatePasswordStrength = (password: string) => {
    const checks = {
      length: password.length >= 8,
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
      number: /\d/.test(password),
      special: /[!@#$%^&*(),.?":{}|<>]/.test(password),
    };

    const passedChecks = Object.values(checks).filter(Boolean).length;
    return { checks, passed: passedChecks };
  };

  const passwordValidation = mode === 'signup' ? validatePasswordStrength(password) : null;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {mode === 'signup' && (
        <Input
          label="Full Name"
          type="text"
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="John Doe"
          required
        />
      )}

      <Input
        label="Email address"
        type="email"
        id="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="name@example.com"
        required
      />

      <PasswordField
        label="Password"
        id="password"
        value={password}
        onChange={(e) => setPassword((e.target as HTMLInputElement).value)}
        required
        autoComplete={mode === 'signup' ? 'new-password' : 'current-password'}
      />

      {mode === 'signup' && passwordValidation && (
        <div className="space-y-2">
          <h3 className="text-sm font-medium text-gray-700">Password requirements:</h3>
          <ul className="space-y-1">
            <li className={`text-sm flex items-center ${passwordValidation.checks.length ? 'text-green-600' : 'text-gray-400'}`}>
              <svg className={`h-4 w-4 mr-2 ${passwordValidation.checks.length ? 'text-green-500' : 'text-gray-300'}`} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              At least 8 characters
            </li>
            <li className={`text-sm flex items-center ${passwordValidation.checks.uppercase ? 'text-green-600' : 'text-gray-400'}`}>
              <svg className={`h-4 w-4 mr-2 ${passwordValidation.checks.uppercase ? 'text-green-500' : 'text-gray-300'}`} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Contains uppercase letter
            </li>
            <li className={`text-sm flex items-center ${passwordValidation.checks.lowercase ? 'text-green-600' : 'text-gray-400'}`}>
              <svg className={`h-4 w-4 mr-2 ${passwordValidation.checks.lowercase ? 'text-green-500' : 'text-gray-300'}`} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Contains lowercase letter
            </li>
            <li className={`text-sm flex items-center ${passwordValidation.checks.number ? 'text-green-600' : 'text-gray-400'}`}>
              <svg className={`h-4 w-4 mr-2 ${passwordValidation.checks.number ? 'text-green-500' : 'text-gray-300'}`} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Contains a number
            </li>
            <li className={`text-sm flex items-center ${passwordValidation.checks.special ? 'text-green-600' : 'text-gray-400'}`}>
              <svg className={`h-4 w-4 mr-2 ${passwordValidation.checks.special ? 'text-green-500' : 'text-gray-300'}`} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Contains a special character
            </li>
          </ul>
        </div>
      )}

      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="text-sm text-red-700">{error}</div>
        </div>
      )}

      <div>
        <Button
          type="submit"
          fullWidth
          loading={loading}
          variant={mode === 'signup' ? 'primary' : 'secondary'}
        >
          {loading ? 'Processing...' : mode === 'signup' ? 'Sign Up' : 'Sign In'}
        </Button>
      </div>
    </form>
  );
};