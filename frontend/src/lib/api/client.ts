// Centralized API client for the frontend todo application
// Implements JWT token handling and attachment mechanism

class ApiClient {
  private baseUrl: string;
  private token: string | null;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    this.token = null;
  }

  setToken(token: string) {
    this.token = token;
  }

  clearToken() {
    this.token = null;
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseUrl}${endpoint}`;

    const headers = {
      'Content-Type': 'application/json',
      ...(this.token ? { 'Authorization': `Bearer ${this.token}` } : {}),
      ...options.headers,
    };

    // Debug logging
    if (endpoint.includes('/tasks')) {
      console.log('API Request:', { method: options.method || 'GET', url, hasToken: !!this.token });
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      // Handle 401 responses by clearing auth and throwing error
      if (response.status === 401) {
        // Clear the token and redirect to signin
        this.clearToken();
        localStorage.removeItem('token');
        localStorage.removeItem('user');

        // Throw error to be handled by caller
        throw new Error('Unauthorized: Please sign in again');
      }

      // Handle 204 No Content (e.g., DELETE requests)
      if (response.status === 204) {
        return { success: true };
      }

      // Check if response is OK
      if (!response.ok) {
        let errorData: any = {};
        try {
          errorData = await response.json();
        } catch (e) {
          // Response is not JSON, use status text
          errorData = { message: response.statusText };
        }

        // Handle FastAPI validation errors (422) - detail can be array or string
        let errorMessage = '';
        if (errorData.detail) {
          if (Array.isArray(errorData.detail)) {
            // FastAPI validation errors are arrays
            errorMessage = errorData.detail.map((err: any) =>
              `${err.loc?.join('.') || ''}: ${err.msg || ''}`
            ).join(', ') || 'Validation error';
          } else if (typeof errorData.detail === 'string') {
            errorMessage = errorData.detail;
          } else if (typeof errorData.detail === 'object') {
            // If detail is an object, stringify it properly
            errorMessage = JSON.stringify(errorData.detail);
          }
        } else if (errorData.message) {
          errorMessage = errorData.message;
        } else if (errorData.error) {
          // Handle the case where error is in 'error' property of response
          errorMessage = errorData.error;
        } else {
          errorMessage = `Request failed with status ${response.status}`;
        }

        throw new Error(errorMessage || `Request failed with status ${response.status}`);
      }

      // Parse JSON response
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        const data = await response.json();
        return data;
      } else {
        // Non-JSON response
        const text = await response.text();
        return text ? { success: true, data: text } : { success: true };
      }
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      
      // Ensure error is always an Error object with a message
      if (error instanceof Error) {
        throw error;
      } else if (typeof error === 'string') {
        throw new Error(error);
      } else if (error && typeof error === 'object') {
        const message = (error as any).message || (error as any).detail || JSON.stringify(error);
        throw new Error(message);
      } else {
        throw new Error('An unexpected error occurred');
      }
    }
  }

  // Authentication methods
  async signup(email: string, password: string, name?: string) {
    return this.request('/api/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    });
  }

  async signin(email: string, password: string) {
    return this.request('/api/auth/signin', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async forgotPassword(email: string) {
    return this.request('/api/auth/forgot-password', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  }

  async resetPassword(email: string, newPassword: string) {
    return this.request('/api/auth/reset-password', {
      method: 'POST',
      body: JSON.stringify({ email, new_password: newPassword }),
    });
  }

  async logout() {
    return this.request('/api/auth/logout', {
      method: 'POST',
    });
  }

  // Task methods
  async getTasks() {
    return this.request('/api/tasks');
  }

  async createTask(title: string, completed: boolean = false, description?: string) {
    return this.request('/api/tasks', {
      method: 'POST',
      body: JSON.stringify({ title, completed, description }),
    });
  }

  async updateTask(id: number, updates: Partial<{ title: string; description?: string; completed: boolean }>) {
    return this.request(`/api/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  async updateTaskCompletion(id: number, completed: boolean) {
    return this.request(`/api/tasks/${id}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  }

  async deleteTask(id: number) {
    return this.request(`/api/tasks/${id}`, {
      method: 'DELETE',
    });
  }
}

export const apiClient = new ApiClient();