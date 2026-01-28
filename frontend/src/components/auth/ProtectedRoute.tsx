'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, isLoading, signout } = useAuth();
  const router = useRouter();
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      // Check for expired session or invalid token
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        try {
          // Decode JWT to check expiration (simplified check)
          const tokenParts = storedToken.split('.');
          if (tokenParts.length === 3) {
            const payload = JSON.parse(atob(tokenParts[1]));
            const currentTime = Math.floor(Date.now() / 1000);

            if (payload.exp && payload.exp < currentTime) {
              // Token is expired
              signout();
              router.replace('/signin');
              setChecked(true);
              return;
            }
          }
        } catch (error) {
          // If we can't decode the token, clear it and redirect
          console.error('Error decoding token:', error);
          signout();
          router.replace('/signin');
          setChecked(true);
          return;
        }
      }

      // If not authenticated, redirect to sign in
      if (!isLoading && !isAuthenticated) {
        router.replace('/signin');
        setChecked(true);
        return;
      }

      setChecked(true);
    };

    if (!checked) {
      checkAuth();
    }
  }, [isAuthenticated, isLoading, router, signout, checked]);

  // Show loading while checking authentication status
  if (!checked || isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <p>Loading...</p>
      </div>
    );
  }

  // If authenticated, render the children
  if (isAuthenticated) {
    return <>{children}</>;
  }

  // If not authenticated, we've already redirected
  return null;
};