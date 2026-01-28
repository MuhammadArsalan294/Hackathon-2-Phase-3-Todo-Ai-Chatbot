'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api/client';

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  signin: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name?: string) => Promise<void>;
  signout: () => void;
  initializeAuth: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    initializeAuth();
  }, []);

  const initializeAuth = () => {
    try {
      const storedToken = localStorage.getItem('token');
      const storedUser = localStorage.getItem('user');

      if (storedToken && storedUser) {
        const parsedUser = JSON.parse(storedUser);
        setToken(storedToken);
        setUser(parsedUser);
        apiClient.setToken(storedToken); // Set token in API client
      }
    } catch (error) {
      console.error('Error initializing auth:', error);
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    } finally {
      setIsLoading(false);
    }
  };

  const signin = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await apiClient.signin(email, password);

      if (response.success && response.data) {
        const { token, user } = response.data;

        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));

        setToken(token);
        setUser(user);
        apiClient.setToken(token);

        // Redirect to dashboard after successful login
        router.replace('/dashboard');
      } else {
        // Check if there's an error message in the response
        if (response.error) {
          const errorMessage = typeof response.error === 'string'
            ? response.error
            : response.error.message || 'Sign in failed';

          // Provide clearer validation messages as per requirements
          if (errorMessage.toLowerCase().includes('invalid credentials')) {
            throw new Error('Invalid credentials');
          } else if (errorMessage.toLowerCase().includes('please sign up first')) {
            throw new Error('Please sign up first');
          } else if (errorMessage.toLowerCase().includes('does not exist') || errorMessage.toLowerCase().includes('user not found')) {
            throw new Error('Please sign up first');
          }

          throw new Error(errorMessage);
        } else {
          throw new Error('Sign in failed');
        }
      }
    } catch (error) {
      // Re-throw the error with its original message
      if (error instanceof Error) {
        throw error;
      } else {
        throw new Error('An unexpected error occurred during sign in');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (email: string, password: string, name?: string) => {
    setIsLoading(true);
    try {
      const response = await apiClient.signup(email, password, name);

      if (response.success && response.data) {
        const { token, user } = response.data;

        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));

        setToken(token);
        setUser(user);
        apiClient.setToken(token);

        // After successful signup, redirect to sign in page (as per strict requirements)
        alert('Account created successfully. Please sign in.');
        router.replace('/signin');
      } else {
        // Check if there's an error message in the response
        if (response.error) {
          const errorMessage = typeof response.error === 'string'
            ? response.error
            : response.error.message || 'Sign up failed';

          // Provide clearer validation messages
          if (errorMessage.toLowerCase().includes('already exists')) {
            throw new Error('User already exists');
          }

          throw new Error(errorMessage);
        } else {
          throw new Error('Sign up failed');
        }
      }
    } catch (error) {
      // Re-throw the error with its original message
      if (error instanceof Error) {
        throw error;
      } else {
        throw new Error('An unexpected error occurred during sign up');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const signout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');

    setToken(null);
    setUser(null);
    apiClient.clearToken();

    // Redirect to landing page after signout
    router.replace('/');
  };

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!token && !!user,
    isLoading,
    signin,
    signup,
    signout,
    initializeAuth
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};