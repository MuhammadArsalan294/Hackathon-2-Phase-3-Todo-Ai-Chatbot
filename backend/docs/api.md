# Todo Backend API Documentation

## Overview

The Todo Backend API provides secure task management functionality with JWT-based authentication and user isolation.

## Authentication

All API endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt-token>
```

Tokens are issued by Better Auth and must be included with every request.

## Endpoints

### Tasks

#### GET /api/tasks
Get all tasks for the authenticated user.

**Response:**
- 200: Array of Task objects
- 401: Unauthorized

#### POST /api/tasks
Create a new task for the authenticated user.

**Request Body:**
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (optional, default false)"
}
```

**Response:**
- 201: Created Task object
- 400: Bad Request
- 401: Unauthorized

#### GET /api/tasks/{id}
Get a specific task by ID.

**Response:**
- 200: Task object
- 401: Unauthorized
- 404: Task not found

#### PUT /api/tasks/{id}
Update a specific task.

**Request Body:**
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

**Response:**
- 200: Updated Task object
- 400: Bad Request
- 401: Unauthorized
- 404: Task not found

#### PATCH /api/tasks/{id}/complete
Update the completion status of a task.

**Request Body:**
```json
{
  "completed": "boolean (required)"
}
```

**Response:**
- 200: Updated Task object
- 400: Bad Request
- 401: Unauthorized
- 404: Task not found

#### DELETE /api/tasks/{id}
Delete a specific task.

**Response:**
- 204: No Content
- 401: Unauthorized
- 404: Task not found

## Error Handling

Standard error response format:

```json
{
  "detail": "Human-readable error message",
  "error_code": "Machine-readable error code"
}
```

### Common Error Codes:
- `AUTHENTICATION_REQUIRED`: 401 - Missing or invalid JWT
- `RESOURCE_NOT_FOUND`: 404 - Resource doesn't exist or belongs to another user
- `VALIDATION_ERROR`: 422 - Request payload validation failed
- `INTERNAL_ERROR`: 500 - Unexpected server error