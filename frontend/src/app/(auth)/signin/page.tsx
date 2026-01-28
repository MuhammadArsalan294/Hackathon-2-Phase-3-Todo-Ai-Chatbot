'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { LoginForm } from '@/components/auth/LoginForm';

const SigninPage: React.FC = () => {
  const [rememberMe, setRememberMe] = useState(false);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-gray-900 mb-2">Welcome Back</h1>
          <p className="text-gray-600">Sign in to your Todo Pro account</p>
        </div>

        <Card className="shadow-lg">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Sign In</h2>
            <p className="mt-2 text-sm text-gray-600">
              Access your tasks and productivity tools
            </p>
          </div>

          <LoginForm mode="signin" />

          <div className="mt-4 flex items-center justify-between">
            <div className="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                Remember me
              </label>
            </div>

            <div className="text-sm">
              <Link href="/forgot-password" className="font-medium text-indigo-600 hover:text-indigo-500">
                Forgot password?
              </Link>
            </div>
          </div>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Don't have an account?{' '}
              <Link href="/signup" className="font-medium text-indigo-600 hover:text-indigo-500">
                Sign up
              </Link>
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default SigninPage;