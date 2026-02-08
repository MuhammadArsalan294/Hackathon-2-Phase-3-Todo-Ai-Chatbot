'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface TaskUpdateContextType {
  taskUpdateTrigger: number;
  triggerTaskUpdate: () => void;
}

const TaskUpdateContext = createContext<TaskUpdateContextType | undefined>(undefined);

export const TaskUpdateProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [taskUpdateTrigger, setTaskUpdateTrigger] = useState(0);

  const triggerTaskUpdate = () => {
    setTaskUpdateTrigger(prev => prev + 1);
  };

  return (
    <TaskUpdateContext.Provider value={{ taskUpdateTrigger, triggerTaskUpdate }}>
      {children}
    </TaskUpdateContext.Provider>
  );
};

export const useTaskUpdate = (): TaskUpdateContextType => {
  const context = useContext(TaskUpdateContext);
  if (context === undefined) {
    throw new Error('useTaskUpdate must be used within a TaskUpdateProvider');
  }
  return context;
};