'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Modal } from '@/components/ui/Modal';
import { TaskForm } from '@/components/todo/TaskForm';

interface Task {
  id?: number;
  user_id?: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at?: string;
  updated_at?: string;
}

interface TaskCardProps {
  task: Task & { id: number };
  onToggleComplete: (id: number, currentStatus: boolean) => void;
  onUpdate: (task: Task) => void;
  onDelete: (id: number) => void;
}

export const TaskCard: React.FC<TaskCardProps> = ({ task, onToggleComplete, onUpdate, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [isConfirmingDelete, setIsConfirmingDelete] = useState(false);

  const handleSave = (updatedTask: Task) => {
    onUpdate(updatedTask);
    setIsEditing(false);
  };

  const handleDeleteConfirmed = () => {
    onDelete(task.id);
    setIsConfirmingDelete(false);
  };

  return (
    <>
      <li className="py-4 border-b border-gray-100 last:border-b-0 hover:bg-gray-50/50 transition-colors duration-200">
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 pt-1">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => onToggleComplete(task.id, task.completed)}
                className="h-5 w-5 text-[rgb(var(--primary-rgb))] focus:ring-[rgb(var(--primary-rgb))] border-[rgb(var(--border-rgb))] rounded cursor-pointer"
              />
            </div>
            <div className="min-w-0 flex-1">
              <p
                className={`text-sm font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}
              >
                {task.title}
              </p>
              {task.description && (
                <p className="mt-1 text-sm text-gray-600">
                  {task.description}
                </p>
              )}
              <div className="mt-3 flex items-center text-xs text-gray-500">
                <div className="flex items-center">
                  <svg className="mr-1 h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span>Created: {task.created_at ? new Date(task.created_at).toLocaleDateString() : 'N/A'}</span>
                </div>
                {task.completed && (
                  <span className="ml-3 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                    <svg className="-ml-0.5 mr-1 h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Completed
                  </span>
                )}
              </div>
            </div>
          </div>
          <div className="flex space-x-2 ml-4">
            <Button
              onClick={() => setIsEditing(true)}
              variant="ghost"
              size="sm"
              icon
              className="text-gray-500 hover:text-gray-700"
            >
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </Button>
            <Button
              onClick={() => setIsConfirmingDelete(true)}
              variant="ghost"
              size="sm"
              icon
              className="text-gray-500 hover:text-red-600"
            >
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </Button>
          </div>
        </div>
      </li>

      {/* Edit Task Modal */}
      <Modal
        isOpen={isEditing}
        onClose={() => setIsEditing(false)}
        title="Edit Task"
      >
        <TaskForm
          task={task}
          onComplete={handleSave}
          onCancel={() => setIsEditing(false)}
        />
      </Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={isConfirmingDelete}
        onClose={() => setIsConfirmingDelete(false)}
        title="Confirm Deletion"
      >
        <p className="mb-4">Are you sure you want to delete the task "{task.title}"?</p>
        <div className="flex justify-end space-x-2">
          <Button
            onClick={() => setIsConfirmingDelete(false)}
            variant="outline"
          >
            Cancel
          </Button>
          <Button
            onClick={handleDeleteConfirmed}
            variant="danger"
          >
            Delete
          </Button>
        </div>
      </Modal>
    </>
  );
};