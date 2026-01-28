# Quickstart Guide: Frontend Todo Application

**Feature**: 002-frontend-todo-app
**Date**: 2026-01-18

## Getting Started

This guide helps you quickly set up and run the frontend todo application.

### Prerequisites

- Node.js 18+
- npm or yarn package manager
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```

2. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

3. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

4. **Set up environment variables**
   Create a `.env.local` file in the frontend directory:
   ```
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
   ```

5. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

6. **Open your browser**
   Visit [http://localhost:3000](http://localhost:3000) to see the application

### Key Features Access

- **Sign up**: Navigate to `/signup` to create a new account
- **Sign in**: Navigate to `/signin` to log into existing account
- **Dashboard**: Access the todo dashboard at `/dashboard` (protected route)
- **Protected routes**: All routes under `/dashboard` require authentication

### Development Commands

- `npm run dev` - Start development server with hot reloading
- `npm run build` - Build the application for production
- `npm run start` - Start production server
- `npm run lint` - Check code for linting errors
- `npm test` - Run unit tests

### API Integration

The application uses a centralized API client located at `lib/api/client.ts` which automatically handles:
- JWT token attachment to requests
- Error handling and normalization
- Loading states
- Authentication status checks

### Environment Variables

- `NEXT_PUBLIC_API_BASE_URL` - Base URL for API endpoints
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Base URL for Better Auth service

### Troubleshooting

**Issue**: Getting 401 errors when accessing protected routes
**Solution**: Ensure your JWT token is properly stored in the authentication provider and being attached to requests

**Issue**: Cannot connect to API
**Solution**: Verify that the `NEXT_PUBLIC_API_BASE_URL` is set correctly and the backend service is running

**Issue**: Authentication not persisting
**Solution**: Check that the Better Auth provider is properly wrapped around your app layout