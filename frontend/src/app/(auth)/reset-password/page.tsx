'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { PasswordField } from '@/components/ui/PasswordField';
import { Button } from '@/components/ui/Button';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { apiClient } from '@/lib/api/client';

const ResetPasswordPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Validate email format
    if (!email || !/\S+@\S+\.\S+/.test(email)) {
      setError('Please enter a valid email address');
      setLoading(false);
      return;
    }

    // Validate passwords match
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    // Validate password strength
    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      setLoading(false);
      return;
    }

    try {
      // Call the backend API to reset password using email
      await apiClient.resetPassword(email, password);

      // Show success message
      setSuccess(true);

      // Redirect to sign in after a short delay to show success message
      setTimeout(() => {
        router.replace('/signin');
      }, 2000);
    } catch (err: any) {
      setError(err.message || 'Failed to reset password');
    } finally {
      setLoading(false);
    }
  };

  // Password strength validation
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

  const passwordValidation = validatePasswordStrength(password);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-gray-900 mb-2">Reset Your Password</h1>
          <p className="text-gray-600">Create a new secure password for your account</p>
        </div>

        <Card className="shadow-lg">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Set New Password</h2>
            <p className="mt-2 text-sm text-gray-600">
              Choose a strong password to protect your account
            </p>
          </div>

          {success ? (
            <div className="rounded-md bg-green-50 p-4 mb-6">
              <div>
                <h3 className="text-sm font-medium text-green-800">Password reset successfully</h3>
                <div className="mt-2 text-sm text-green-700">
                  <p>You can now sign in with your new password.</p>
                </div>
              </div>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              <Input
                label="Registered Email"
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                required
              />

              <PasswordField
                label="New Password"
                id="password"
                value={password}
                onChange={(e) => setPassword((e.target as HTMLInputElement).value)}
                required
                autoComplete="new-password"
              />

              <PasswordField
                label="Confirm New Password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword((e.target as HTMLInputElement).value)}
                required
                autoComplete="new-password"
              />

              {/* Password strength indicator */}
              <div className="space-y-2">
                <h3 className="text-sm font-medium text-gray-700">Password requirements:</h3>
                <ul className="space-y-1">
                  <li className={`text-sm ${passwordValidation.checks.length ? 'text-green-600' : 'text-gray-400'}`}>
                    At least 8 characters
                  </li>
                  <li className={`text-sm ${passwordValidation.checks.uppercase ? 'text-green-600' : 'text-gray-400'}`}>
                    Contains uppercase letter
                  </li>
                  <li className={`text-sm ${passwordValidation.checks.lowercase ? 'text-green-600' : 'text-gray-400'}`}>
                    Contains lowercase letter
                  </li>
                  <li className={`text-sm ${passwordValidation.checks.number ? 'text-green-600' : 'text-gray-400'}`}>
                    Contains a number
                  </li>
                  <li className={`text-sm ${passwordValidation.checks.special ? 'text-green-600' : 'text-gray-400'}`}>
                    Contains a special character
                  </li>
                </ul>
              </div>

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
                  variant="primary"
                >
                  {loading ? <LoadingSpinner size="sm" /> : 'Reset Password'}
                </Button>
              </div>
            </form>
          )}

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Remember your password?{' '}
              <Link href="/signin" className="font-medium text-indigo-600 hover:text-indigo-500">
                Sign in
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default ResetPasswordPage;