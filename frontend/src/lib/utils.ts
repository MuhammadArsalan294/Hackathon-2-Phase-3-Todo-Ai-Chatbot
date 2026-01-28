// Global utility functions for error handling and loading states

export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: {
    message: string;
    code?: string;
    details?: any;
  };
}

export const handleApiError = (error: any): string => {
  if (error.message === 'Unauthorized') {
    // Trigger logout or redirect to login
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/signin';
    return 'Session expired. Please sign in again.';
  }

  if (error instanceof TypeError && error.message.includes('fetch')) {
    return 'Network error. Please check your connection.';
  }

  if (typeof error === 'string') {
    return error;
  }

  if (error?.response?.data?.error?.message) {
    return error.response.data.error.message;
  }

  return 'An unexpected error occurred. Please try again.';
};

export const sleep = (ms: number): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

// Loading state management
export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface LoadingStateType {
  state: LoadingState;
  message?: string;
}

export const getInitialLoadingState = (): LoadingStateType => ({
  state: 'idle'
});

export const setLoadingState = (state: LoadingState, message?: string): LoadingStateType => ({
  state,
  message
});