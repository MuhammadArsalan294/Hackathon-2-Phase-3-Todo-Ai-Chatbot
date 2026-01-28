'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { Button } from '@/components/ui/Button';

export const Navbar: React.FC = () => {
  const pathname = usePathname();
  const { isAuthenticated, user, signout } = useAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const handleSignOut = async () => {
    try {
      await signout();
      setDropdownOpen(false);
      // The auth context will handle the redirect after clearing auth state
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Don't show navbar on auth pages
  if (pathname?.startsWith('/signin') || pathname?.startsWith('/signup') || pathname?.startsWith('/forgot-password') || pathname?.startsWith('/reset-password')) {
    return null;
  }

  return (
    <nav className="bg-gradient-primary text-white shadow-medium">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <div className="flex items-center">
                <div className="bg-white text-indigo-600 w-8 h-8 rounded-lg flex items-center justify-center font-bold mr-2">
                  TP
                </div>
                <span className="text-xl font-bold tracking-tight">TodoPro</span>
              </div>
            </Link>
            <div className="hidden md:ml-6 md:flex md:space-x-8">
              {isAuthenticated ? (
                <>
                  <Link
                    href="/dashboard"
                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-all duration-200 ${
                      pathname === '/dashboard'
                        ? 'border-white text-white'
                        : 'border-transparent text-indigo-100 hover:border-indigo-200 hover:text-white'
                    }`}
                  >
                    <span className="relative">
                      <span className="absolute inset-x-0 -bottom-6 h-0.5 bg-white opacity-0 group-hover:opacity-100 transition-opacity duration-200"></span>
                      Dashboard
                    </span>
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    href="/signin"
                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-all duration-200 ${
                      pathname === '/signin'
                        ? 'border-white text-white'
                        : 'border-transparent text-indigo-100 hover:border-indigo-200 hover:text-white'
                    }`}
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/signup"
                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-all duration-200 ${
                      pathname === '/signup'
                        ? 'border-white text-white'
                        : 'border-transparent text-indigo-100 hover:border-indigo-200 hover:text-white'
                    }`}
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
          <div className="flex items-center">
            {isAuthenticated && user && (
              <div className="ml-3 relative" ref={dropdownRef}>
                <div>
                  <button
                    type="button"
                    className="max-w-xs flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-white"
                    id="user-menu-button"
                    aria-expanded={dropdownOpen}
                    onClick={() => setDropdownOpen(!dropdownOpen)}
                  >
                    <span className="sr-only">Open user menu</span>
                    <div className="h-8 w-8 rounded-full bg-white text-indigo-600 flex items-center justify-center font-medium uppercase">
                      {user.name ? user.name.charAt(0) : user.email?.charAt(0) || 'U'}
                    </div>
                  </button>
                </div>

                {dropdownOpen && (
                  <div
                    className="origin-top-right absolute right-0 mt-2 w-48 rounded-lg shadow-card bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50 overflow-hidden"
                    role="menu"
                    aria-orientation="vertical"
                    aria-labelledby="user-menu-button"
                  >
                    <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
                      <p className="text-sm font-medium text-gray-900 truncate">{user.name || user.email}</p>
                      <p className="text-xs text-gray-500 truncate">{user.email}</p>
                    </div>
                    <button
                      onClick={handleSignOut}
                      className="block w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 transition-colors duration-200 border-t border-gray-100"
                      role="menuitem"
                    >
                      Sign out
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};