'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { apiClient } from '@/lib/api/client';
import { useAuth } from '@/lib/auth';

export const LogoutButton: React.FC = () => {
  const router = useRouter();
  const { signout } = useAuth();

  const handleLogout = async () => {
    try {
      // Call the logout API endpoint
      await apiClient.logout();
    } catch (error) {
      // Even if the API call fails, we should still clear the local session
      console.error('Logout API call failed:', error);
    } finally {
      // Clear the authentication state
      signout();

      // Redirect to signin page
      router.push('/signin');
      router.refresh(); // Refresh to update the UI after state change
    }
  };

  return (
    <Button
      onClick={handleLogout}
      variant="secondary"
      size="sm"
    >
      Logout
    </Button>
  );
};