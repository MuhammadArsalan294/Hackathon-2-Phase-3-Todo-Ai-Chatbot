import React from 'react';
import './globals.css';
import type { Metadata } from 'next';
import { AuthProvider } from '@/lib/auth';
import { Navbar } from '@/components/ui/Navbar';

export const metadata: Metadata = {
  title: 'Todo Pro - Productivity Suite',
  description: 'A professional todo application with advanced productivity features',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-gray-50">
        <AuthProvider>
          <Navbar />
          <main>
            {children}
          </main>
        </AuthProvider>
      </body>
    </html>
  );
}