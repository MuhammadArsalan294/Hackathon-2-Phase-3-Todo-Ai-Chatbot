# Claude Agent Context: Frontend UI/UX Refinement

## Project Context
- **Project**: Todo Full-Stack Application – Frontend Debug & UI Refinement
- **Feature**: 004-frontend-refinement
- **Goal**: Create professional, SaaS-grade frontend with enhanced authentication and task management

## Technology Stack
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Hooks (useState, useEffect)
- **Authentication**: Better Auth integration
- **API**: Centralized API client with JWT handling

## Key Requirements
- Professional Signup and Signin UI with card-based layouts
- Functional Todo dashboard with proper task management
- Editable task inputs with controlled components
- Working Add Task functionality
- Proper JWT token handling and API integration
- Responsive, SaaS-grade UI with consistent design system

## Architecture
- Main layout: src/app/layout.tsx
- Authentication pages: src/app/(auth)/
- Dashboard: src/app/dashboard/page.tsx
- Components: src/components/
- API client: src/lib/api/client.ts
- Auth context: src/lib/auth.tsx
- UI components: src/components/ui/

## Environment Variables
- NEXT_PUBLIC_API_BASE_URL: Backend API base URL
- NEXT_PUBLIC_BETTER_AUTH_URL: Authentication service URL

## API Contract
- Base path: /api
- Endpoints: GET/POST/PUT/PATCH/DELETE /api/tasks
- Authentication: Authorization: Bearer <token>
- Response format: { success: boolean, data?: any, error?: { message: string } }

## Security Constraints
- JWT tokens stored securely in localStorage
- All API requests must include Authorization header
- Proper error handling for authentication failures
- Session cleanup on logout

## Files to Refine
- src/app/(auth)/signin/page.tsx: Professional signin page
- src/app/(auth)/signup/page.tsx: Professional signup page
- src/app/dashboard/page.tsx: Enhanced dashboard layout
- src/components/todo/TaskList.tsx: Improved task list component
- src/components/todo/TaskForm.tsx: Enhanced task form with controlled inputs
- src/components/todo/TaskCard.tsx: Improved task display component
- src/components/ui/Navbar.tsx: Updated branding to "Todo Pro"
- src/lib/api/client.ts: Fixed API client with proper error handling
- src/components/ui/Input.tsx: Extended to support textarea