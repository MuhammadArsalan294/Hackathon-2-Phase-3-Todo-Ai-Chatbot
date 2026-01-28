'use client';

import { useRouter } from 'next/navigation';
import React, { useEffect } from 'react';

const ForgotPasswordPage: React.FC = () => {
  const router = useRouter();

  // Automatically redirect to the reset password page
  useEffect(() => {
    router.replace('/reset-password');
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full text-center">
        <div className="animate-pulse">
          <h1 className="text-3xl font-extrabold text-gray-900 mb-2">Redirecting...</h1>
          <p className="text-gray-600">You are being redirected to the password reset page</p>
        </div>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;