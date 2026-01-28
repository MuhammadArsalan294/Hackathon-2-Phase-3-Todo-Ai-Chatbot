'use client';

import React from 'react';
import { useAuth } from '@/lib/auth';

export const UserDisplay: React.FC = () => {
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  return (
    <div className="flex items-center">
      <div className="mr-3 text-sm text-gray-700">
        Welcome, <span className="font-medium">{user.name || user.email}</span>
      </div>
    </div>
  );
};