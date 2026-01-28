'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import LandingPage from './landing/page'; // Import the landing page component
import DashboardPage from './dashboard/page'; // Import the dashboard page component

const HomePage: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();

  // Show loading state while checking auth status
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full text-center">
          <div className="animate-pulse">
            <div className="mx-auto h-16 w-16 rounded-full bg-indigo-500 flex items-center justify-center mb-6">
              <svg className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">TodoPro</h1>
            <p className="text-gray-600">Loading your workspace...</p>
          </div>
        </div>
      </div>
    );
  }

  // Render the appropriate page based on authentication status
  if (isAuthenticated) {
    return <DashboardPage />;
  } else {
    return <LandingPage />;
  }
};

export default HomePage;