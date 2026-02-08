'use client';

import React, { useState, useEffect } from 'react';
import { TaskCard } from '@/components/todo/TaskCard';
import { TaskForm } from '@/components/todo/TaskForm';
import { apiClient } from '@/lib/api/client';
import { useAuth } from '@/lib/auth';
import { useTaskUpdate } from '@/contexts/TaskUpdateContext';
import { Button } from '@/components/ui/Button';
import { Toast } from '@/components/ui/Toast';

interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState<boolean>(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);
  const { isAuthenticated, isLoading: authLoading, token } = useAuth();
  const { taskUpdateTrigger } = useTaskUpdate();

  useEffect(() => {
    // Ensure token is set in API client from localStorage
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      apiClient.setToken(storedToken);
    }
  }, []);

  useEffect(() => {
    // Wait for auth to be ready and user to be authenticated
    if (!authLoading && isAuthenticated && token) {
      fetchTasks();
    } else if (!authLoading && !isAuthenticated) {
      setLoading(false);
      setError('Please sign in to view your tasks');
    }
  }, [isAuthenticated, authLoading, token, taskUpdateTrigger]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null); // Clear previous errors
      const response = await apiClient.getTasks();

      // Backend returns tasks array directly, not wrapped in { success, data }
      if (Array.isArray(response)) {
        setTasks(response);
      } else if (response && response.success) {
        // Handle wrapped format if backend changes
        setTasks(response.data || []);
      } else if (response && response.error) {
        // Handle error response
        const errorMsg = response.error?.message || response.error?.detail || 'Failed to fetch tasks';
        setError(errorMsg);
      } else if (response && typeof response === 'object') {
        // Unexpected response format - log it for debugging
        console.warn('Unexpected response format:', response);
        setError('Failed to fetch tasks: Unexpected response format');
      } else {
        // Response is null, undefined, or something unexpected
        setError('Failed to fetch tasks');
      }
    } catch (err: any) {
      // Handle different error types
      let errorMessage = 'An unexpected error occurred';
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err?.message) {
        errorMessage = err.message;
      } else if (err?.detail) {
        errorMessage = err.detail;
      } else if (typeof err === 'object') {
        errorMessage = JSON.stringify(err);
      }
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskCreated = (newTask: Task) => {
    setTasks([...tasks, newTask]);
    setShowForm(false);
    setToast({ message: 'Task created successfully!', type: 'success' });
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
    setToast({ message: 'Task updated successfully!', type: 'success' });
  };

  const handleTaskDeleted = async (taskId: number) => {
    try {
      await apiClient.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
      setToast({ message: 'Task deleted successfully!', type: 'success' });
    } catch (err: any) {
      // Handle different error types
      let errorMessage = 'Failed to delete task';
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err?.message) {
        errorMessage = err.message;
      } else if (err?.detail) {
        errorMessage = err.detail;
      }
      setError(errorMessage);
      setToast({ message: errorMessage, type: 'error' });
    }
  };

  const handleToggleComplete = async (taskId: number, currentStatus: boolean) => {
    try {
      const response = await apiClient.updateTaskCompletion(taskId, !currentStatus);

      // Backend returns task directly, not wrapped in { success, data }
      if (response.id) {
        // Direct task object from backend
        handleTaskUpdated(response);
        setToast({
          message: `Task ${!currentStatus ? 'marked as complete' : 'marked as incomplete'}!`,
          type: 'success'
        });
      } else if (response.success) {
        // Handle wrapped format if backend changes
        handleTaskUpdated(response.data);
        setToast({
          message: `Task ${!currentStatus ? 'marked as complete' : 'marked as incomplete'}!`,
          type: 'success'
        });
      } else {
        const errorMsg = response.error?.message || 'Failed to update task';
        setError(errorMsg);
        setToast({ message: errorMsg, type: 'error' });
      }
    } catch (err: any) {
      // Handle different error types
      let errorMessage = 'Failed to update task';
      if (err instanceof Error) {
        errorMessage = err.message;
      } else if (typeof err === 'string') {
        errorMessage = err;
      } else if (err?.message) {
        errorMessage = err.message;
      } else if (err?.detail) {
        errorMessage = err.detail;
      }
      setError(errorMessage);
      setToast({ message: errorMessage, type: 'error' });
    }
  };

  const closeToast = () => {
    setToast(null);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <p>Loading tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-l-4 border-red-400 p-4 m-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 0L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-red-700">
              {error} <button onClick={fetchTasks} className="underline ml-2">Retry</button>
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="divide-y divide-gray-200">
      {toast && <Toast message={toast.message} type={toast.type} onClose={closeToast} />}

      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-6">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Your Tasks</h3>
          <p className="text-sm text-gray-500 mt-1">{tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}</p>
        </div>

        <Button
          onClick={() => setShowForm(!showForm)}
          variant={showForm ? "outline" : "primary"}
          size="md"
          className="flex items-center"
        >
          {showForm ? (
            <>
              <svg className="-ml-1 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
              Cancel
            </>
          ) : (
            <>
              <svg className="-ml-0.5 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Add Task
            </>
          )}
        </Button>
      </div>

      {showForm && (
        <div className="mb-6 p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-100 animate-fadeIn shadow-light">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-md font-semibold text-gray-900">Create New Task</h4>
            <div className="h-2 w-2 rounded-full bg-[rgb(var(--primary-rgb))]"></div>
          </div>
          <TaskForm onComplete={handleTaskCreated} onCancel={() => setShowForm(false)} />
        </div>
      )}

      {tasks.length === 0 ? (
        <div className="text-center py-12 animate-scaleIn">
          <div className="mx-auto h-16 w-16 rounded-full bg-gray-100 flex items-center justify-center mb-4">
            <svg className="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h3 className="mt-2 text-lg font-medium text-gray-900">No tasks yet</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating your first task.</p>
          <div className="mt-6">
            <Button
              onClick={() => setShowForm(true)}
              variant="primary"
              size="md"
              className="flex items-center mx-auto"
            >
              <svg className="-ml-0.5 mr-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Create your first task
            </Button>
          </div>
        </div>
      ) : (
        <ul className="divide-y divide-gray-100">
          {tasks.map((task) => (
            <TaskCard
              key={task.id}
              task={task}
              onToggleComplete={handleToggleComplete}
              onUpdate={handleTaskUpdated}
              onDelete={handleTaskDeleted}
            />
          ))}
        </ul>
      )}
    </div>
  );
};