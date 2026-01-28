'use client';

import React, { useState } from 'react';
import { Input } from '@/components/ui/Input';
import { PasswordField } from '@/components/ui/PasswordField';
import { Button } from '@/components/ui/Button';
import { apiClient } from '@/lib/api/client';
import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';

interface SignupFormProps {
  onSuccess?: () => void;
}

export const SignupForm: React.FC<SignupFormProps> = ({ onSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { signup } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Directly call the signup method which handles API call and state update
      await signup(email, password, name);

      // Call success callback if provided
      if (onSuccess) {
        onSuccess();
      } else {
        // Redirect to dashboard
        router.push('/dashboard');
        router.refresh(); // Refresh to update the UI after state change
      }
    } catch (err: any) {
      setError(err.message || 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Input
        label="Full Name"
        type="text"
        id="name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="John Doe"
        required
      />

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
        autoComplete="new-password"
      />

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
          {loading ? 'Creating Account...' : 'Sign Up'}
        </Button>
      </div>
    </form>
  );
};