'use client';

import React from 'react';
import { TaskList } from '@/components/todo/TaskList';

const DashboardPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8 animate-slideInUp">
        <div className="text-center mb-6">
          <h1 className="text-display text-gray-900 mb-3">Your Tasks</h1>
          <p className="text-subheading max-w-md mx-auto">Manage your daily work efficiently with our productivity suite</p>
        </div>

        <div className="relative overflow-hidden rounded-2xl bg-gradient-card shadow-card border border-[rgb(var(--border-rgb))]">
          <div className="absolute inset-0 bg-gradient-to-r from-[rgb(var(--primary-rgb))] to-[rgb(var(--secondary-rgb))] opacity-5"></div>
          <div className="relative bg-white bg-opacity-95 backdrop-blur-sm">
            <div className="px-6 py-5 border-b border-gray-200 bg-gradient-to-r from-white to-gray-50">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Task Management</h2>
                  <p className="text-sm text-gray-500 mt-1">Stay organized and productive</p>
                </div>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gradient-primary text-white shadow-light">
                  <svg className="-ml-0.5 mr-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Productivity Suite
                </span>
              </div>
            </div>

            <div className="p-6">
              <TaskList />
            </div>
          </div>
        </div>
      </div>

      {/* Floating Add Task Button for Mobile */}
      <div className="fixed bottom-6 right-6 md:hidden z-40 animate-scaleIn">
        <button
          onClick={() => {
            // This would trigger the add task form, but we'll let the TaskList component handle it
            const addTaskBtn = document.querySelector('[aria-label="Add Task"]');
            if (addTaskBtn) {
              (addTaskBtn as HTMLElement).click();
            }
          }}
          className="bg-gradient-primary text-white p-4 rounded-full shadow-card hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[rgb(var(--primary-rgb))] transition-all duration-200 transform hover:scale-105"
          aria-label="Add Task"
        >
          <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default DashboardPage;