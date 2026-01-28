'use client';

import React, { useState, useEffect } from 'react';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { apiClient } from '@/lib/api/client';

interface Task {
  id?: number;
  user_id?: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at?: string;
  updated_at?: string;
}

interface TaskFormProps {
  task?: Task;
  onComplete: (task: Task) => void;
  onCancel?: () => void;
}

export const TaskForm: React.FC<TaskFormProps> = ({ task, onComplete, onCancel }) => {
  const [title, setTitle] = useState(task?.title || '');
  const [completed, setCompleted] = useState(task?.completed || false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isEditing = !!task?.id;

  const [description, setDescription] = useState(task?.description || '');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      let response;
      if (isEditing) {
        // Update existing task
        response = await apiClient.updateTask(task.id!, { title, description, completed });
      } else {
        // Create new task
        response = await apiClient.createTask(title, completed, description);
      }

      // Backend returns task directly, not wrapped in { success, data }
      if (response.id) {
        // Direct task object from backend
        onComplete(response);
      } else if (response.success) {
        // Handle wrapped format if backend changes
        onComplete(response.data);
      } else {
        setError(response.error?.message || (isEditing ? 'Failed to update task' : 'Failed to create task'));
      }
    } catch (err: any) {
      // Handle different error types
      let errorMessage = isEditing ? 'Failed to update task' : 'Failed to create task';
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
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <Input
          label="Task Title"
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          required
          fullWidth
        />
        <p className="mt-1 text-xs text-gray-500">Give your task a clear and descriptive title</p>
      </div>

      <div>
        <Input
          label="Description"
          type="textarea"
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add details..."
          fullWidth
          rows={3}
        />
        <p className="mt-1 text-xs text-gray-500">Provide more context or details about the task</p>
      </div>

      <div className="flex items-center">
        <input
          type="checkbox"
          id="completed"
          checked={completed}
          onChange={(e) => setCompleted(e.target.checked)}
          className="h-4 w-4 text-[rgb(var(--primary-rgb))] focus:ring-[rgb(var(--primary-rgb))] border-[rgb(var(--border-rgb))] rounded cursor-pointer"
        />
        <label htmlFor="completed" className="ml-2 block text-sm text-gray-700">
          Mark as completed
        </label>
      </div>

      {error && (
        <div className="rounded-lg bg-red-50 p-4 border border-red-100">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="flex flex-col sm:flex-row sm:space-x-3 space-y-3 sm:space-y-0">
        <Button
          type="submit"
          loading={loading}
          variant={isEditing ? 'primary' : 'primary'}
          className="flex-1"
        >
          {loading ? (isEditing ? 'Updating...' : 'Creating...') : (isEditing ? 'Update Task' : 'Create Task')}
        </Button>

        {onCancel && (
          <Button
            type="button"
            onClick={onCancel}
            variant="outline"
            className="flex-1"
          >
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
};