# Data Model: Frontend Todo Application

**Feature**: 002-frontend-todo-app
**Date**: 2026-01-18

## Entity Definitions

### User Entity

Represents an authenticated user in the system.

**Fields**:
- `id` (string): Unique identifier for the user
- `email` (string): User's email address for authentication
- `name` (string, optional): User's display name
- `createdAt` (datetime): Account creation timestamp
- `updatedAt` (datetime): Last update timestamp

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Name (if provided) must be 1-50 characters

**State Transitions**:
- `logged_out` → `logging_in` → `authenticated` → `logging_out` → `logged_out`

### Task Entity

Represents a todo item belonging to a user.

**Fields**:
- `id` (string): Unique identifier for the task
- `userId` (string): Reference to the owning user (foreign key)
- `title` (string): Task title/description
- `completed` (boolean): Completion status
- `createdAt` (datetime): Task creation timestamp
- `updatedAt` (datetime): Last update timestamp

**Validation Rules**:
- Title must be 1-200 characters
- userId must reference an existing user
- Completed defaults to false

**State Transitions**:
- `created` → `in_progress` → `completed` OR `created` → `deleted`

## Relationships

- **User → Task**: One-to-many (one user owns many tasks)
- **Foreign Key Constraint**: Task.userId references User.id

## Data Flow Patterns

### Authentication Flow
```
User credentials → Better Auth → JWT token → Frontend storage → API requests
```

### Task Operations Flow
```
User interaction → API client → JWT attachment → Backend service → Database
```

## Frontend State Model

### Authentication State
```
{
  isAuthenticated: boolean,
  user: User | null,
  token: string | null,
  loading: boolean,
  error: string | null
}
```

### Task State
```
{
  tasks: Task[],
  loading: boolean,
  error: string | null,
  creating: boolean,
  editing: string | null // taskId being edited
}
```

## API Response Structures

### Authentication Responses
```
POST /api/auth/signup
Response: {
  success: boolean,
  user: User,
  token: string
}

POST /api/auth/signin
Response: {
  success: boolean,
  user: User,
  token: string
}

POST /api/auth/logout
Response: {
  success: boolean
}
```

### Task Operation Responses
```
GET /api/tasks
Response: {
  success: boolean,
  data: Task[]
}

POST /api/tasks
Request: { title: string }
Response: {
  success: boolean,
  data: Task
}

PUT /api/tasks/{id}
Request: { title?: string, completed?: boolean }
Response: {
  success: boolean,
  data: Task
}

DELETE /api/tasks/{id}
Response: {
  success: boolean
}
```

## Error Response Structure
```
{
  success: boolean,
  error: {
    message: string,
    code: string,
    details?: any
  }
}
```