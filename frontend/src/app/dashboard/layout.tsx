'use client';

import React from 'react';
import { ProtectedRoute } from '@/components/auth/ProtectedRoute';

const DashboardLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        {/* Main content */}
        <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </div>
    </ProtectedRoute>
  );
};

export default DashboardLayout;