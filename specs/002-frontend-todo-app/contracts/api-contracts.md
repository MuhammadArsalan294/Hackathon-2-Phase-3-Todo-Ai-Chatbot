# API Contracts: Frontend Todo Application

**Feature**: 002-frontend-todo-app
**Date**: 2026-01-18

## Overview

This document defines the API contracts for the frontend todo application. These contracts serve as the interface between the frontend and the future backend implementation, ensuring consistency and enabling parallel development.

## Authentication Endpoints

### POST /api/auth/signup
Register a new user account

**Request Body**:
```json
{
  "email": "string",
  "password": "string",
  "name": "string (optional)"
}
```

**Success Response** (200):
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "string",
      "email": "string",
      "name": "string",
      "createdAt": "datetime",
      "updatedAt": "datetime"
    },
    "token": "string (JWT)"
  }
}
```

**Error Response** (400, 409, 500):
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "string"
  }
}
```

### POST /api/auth/signin
Authenticate an existing user

**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Success Response** (200):
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "string",
      "email": "string",
      "name": "string",
      "createdAt": "datetime",
      "updatedAt": "datetime"
    },
    "token": "string (JWT)"
  }
}
```

**Error Response** (400, 401, 500):
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "string"
  }
}
```

### POST /api/auth/logout
End the current user session

**Headers**:
- Authorization: Bearer {token}

**Success Response** (200):
```json
{
  "success": true
}
```

**Error Response** (401, 500):
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "string"
  }
}
```

## Task Management Endpoints

### GET /api/tasks
Retrieve all tasks for the authenticated user

**Headers**:
- Authorization: Bearer {token}

**Success Response** (200):
```json
{
  "success": true,
  "data": [
    {
      "id": "string",
      "userId": "string",
      "title": "string",
      "completed": "boolean",
      "createdAt": "datetime",
      "updatedAt": "datetime"
    }
  ]
}
```

**Error Response** (401, 500):
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "string"
  }
}
```

### POST /api/tasks
Create a new task for the authenticated user

**Headers**:
- Authorization: Bearer {token}

**Request Body**:
```json
{
  "title": "string (1-200 characters)",
  "completed": "boolean (optional, defaults to false)"
}
```

**Success Response** (201):
```json
{
  "success": true,
  "data": {
    "id": "string",
    "userId": "string",
    "title": "string",
    "completed": "boolean",
    "createdAt": "datetime",
    "updatedAt": "datetime"
  }
}
```

**Error Response** (400, 401, 500):
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "string"
  }
}
```

### PUT /api/tasks/{id}
Update an existing task

**Headers**:
- Authorization: Bearer {token}

**Path Parameter**:
- id: string (task identifier)

**Request Body**:
```json
{
  "title": "string (optional)",
  "completed": "boolean (optional)"
}
```

**Success Response** (200):
```json
{
  "success": true,
  "data": {
    "id": "string",
    "userId": "string",
    "title": "string",
    "completed": "boolean",
    "createdAt": "datetime",
    "updatedAt": "datetime"
  }
}
```

**Error Response** (400, 401, 404, 500):
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "string"
  }
}
```

### DELETE /api/tasks/{id}
Delete a task

**Headers**:
- Authorization: Bearer {token}

**Path Parameter**:
- id: string (task identifier)

**Success Response** (200):
```json
{
  "success": true
}
```

**Error Response** (401, 404, 500):
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "string"
  }
}
```

## Error Codes

- `AUTH_REQUIRED`: 401 - Authentication required
- `INVALID_CREDENTIALS`: 401 - Invalid email or password
- `TASK_NOT_FOUND`: 404 - Task does not exist
- `USER_NOT_FOUND`: 404 - User does not exist
- `VALIDATION_ERROR`: 400 - Request validation failed
- `DUPLICATE_EMAIL`: 409 - Email already exists
- `INTERNAL_ERROR`: 500 - Internal server error

## Security Requirements

1. All endpoints except authentication require JWT token in Authorization header
2. Users can only access their own resources
3. All sensitive data must be transmitted over HTTPS
4. Passwords must be hashed and never stored in plaintext
5. Tokens must have appropriate expiration times

## Rate Limiting

- Authentication attempts: 5 per minute per IP
- API requests: 1000 per hour per user