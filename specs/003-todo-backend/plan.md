# Implementation Plan: Todo Backend Implementation

**Feature**: 003-todo-backend
**Created**: 2026-01-18
**Status**: Draft
**Authors**: [Author Names]
**Reviewers**: [Reviewer Names]

## Technical Context

This plan outlines the implementation of a secure, production-ready FastAPI backend for the Todo application. The backend will support JWT-based authentication, user-scoped task management, and persistent storage using Neon PostgreSQL. The frontend is already implemented and must not be changed.

### Architecture Overview

- **Backend Framework**: FastAPI
- **Language**: Python
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (JWT verification only)
- **Architecture**: Monorepo with Spec-Kit

### Key Components

- **Authentication**: JWT verification using BETTER_AUTH_SECRET
- **Database**: SQLModel with Neon PostgreSQL integration
- **API Layer**: REST endpoints under /api with user isolation
- **Security**: Mandatory authentication and user data isolation

### Technology Stack

- FastAPI for web framework
- SQLModel for ORM
- PyJWT for JWT handling
- python-multipart for form data handling
- uvicorn for ASGI server
- psycopg2-binary for PostgreSQL driver

### Known Unknowns

- Specific environment variables for deployment
- Exact CORS origins for frontend integration
- Database connection pool settings for Neon compatibility

## Constitution Check

### Compliance Verification

- ✅ **Spec-First Development**: All work originates from /specs directory
- ✅ **Agent Responsibility Boundaries**: Following defined roles
- ✅ **No Manual Coding**: All implementation will be agent-performed
- ✅ **Authentication & Identity**: Backend only verifies JWT, no password/session management
- ✅ **Security First**: All endpoints require authentication, user data isolation enforced
- ✅ **API Design Rules**: Following RESTful conventions and exact API specs
- ✅ **Database Ownership**: Not creating users table, only task records with user_id
- ✅ **Frontend Rules**: Will support centralized API client and JWT handling
- ✅ **Monorepo Discipline**: Keeping backend separate from frontend
- ✅ **Validation & Compliance**: Will validate against acceptance criteria

### Gate Status

- **Open Issues**: None identified
- **Risk Level**: Medium (security-sensitive implementation)
- **Compliance Status**: Compliant

## Phase 0: Research & Resolution

### Research Tasks

#### RT-001: JWT Verification Implementation
- **Objective**: Research JWT verification best practices with Better Auth
- **Focus**: Signature verification using BETTER_AUTH_SECRET, token expiry validation
- **Deliverable**: JWT verification algorithm and implementation pattern

#### RT-002: Neon PostgreSQL Connection Pooling
- **Objective**: Research optimal connection pooling for Neon Serverless
- **Focus**: Connection lifecycle, pooling strategies, timeout configurations
- **Deliverable**: Database engine configuration recommendations

#### RT-003: FastAPI Security Patterns
- **Objective**: Research dependency injection for authentication
- **Focus**: Creating reusable auth dependencies, security schemes
- **Deliverable**: Authentication dependency pattern

#### RT-004: CORS Configuration for Next.js
- **Objective**: Research optimal CORS settings for frontend integration
- **Focus**: Origin allowances, header configurations, credentials handling
- **Deliverable**: CORS middleware configuration

### Research Outcomes

#### Decision: JWT Library Selection
- **Chosen**: PyJWT with cryptography backend
- **Rationale**: Industry standard, well-maintained, supports RS256 for Better Auth
- **Alternatives considered**: python-jose, authlib

#### Decision: Database Connection Management
- **Chosen**: Async SQLAlchemy session with context managers
- **Rationale**: Compatible with Neon's serverless model, proper async handling
- **Alternatives considered**: Direct psycopg2 connections, sync sessions

#### Decision: Error Response Format
- **Chosen**: Standard HTTP error responses with JSON bodies
- **Rationale**: Consistent with FastAPI conventions, frontend-friendly
- **Alternatives considered**: Custom error objects

## Phase 1: Design & Contracts

### Data Model: Task Entity

#### Fields
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Required, Foreign Key Reference)
- `title`: String (Required, Max 255 chars)
- `description`: Text (Optional)
- `completed`: Boolean (Default: False)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated)

#### Relationships
- One User to Many Tasks (via user_id foreign key)

#### Validation Rules
- Title must not be empty
- User_id must be present and valid
- Completed field must be boolean

#### Indexes
- Index on user_id for efficient filtering
- Composite index on (user_id, created_at) for sorting

### API Contract: Task Management Endpoints

#### GET /api/tasks
- **Method**: GET
- **Auth Required**: Yes
- **Query Parameters**: None
- **Response**: 200 OK with array of Task objects
- **Error Responses**: 401 Unauthorized

#### POST /api/tasks
- **Method**: POST
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "title": "string (required)",
    "description": "string (optional)",
    "completed": "boolean (optional, default false)"
  }
  ```
- **Response**: 201 Created with created Task object
- **Error Responses**: 400 Bad Request, 401 Unauthorized

#### GET /api/tasks/{id}
- **Method**: GET
- **Auth Required**: Yes
- **Path Parameter**: id (integer, required)
- **Response**: 200 OK with Task object
- **Error Responses**: 401 Unauthorized, 404 Not Found

#### PUT /api/tasks/{id}
- **Method**: PUT
- **Auth Required**: Yes
- **Path Parameter**: id (integer, required)
- **Request Body**: Same as POST
- **Response**: 200 OK with updated Task object
- **Error Responses**: 400 Bad Request, 401 Unauthorized, 404 Not Found

#### DELETE /api/tasks/{id}
- **Method**: DELETE
- **Auth Required**: Yes
- **Path Parameter**: id (integer, required)
- **Response**: 204 No Content
- **Error Responses**: 401 Unauthorized, 404 Not Found

#### PATCH /api/tasks/{id}/complete
- **Method**: PATCH
- **Auth Required**: Yes
- **Path Parameter**: id (integer, required)
- **Request Body**:
  ```json
  {
    "completed": "boolean (required)"
  }
  ```
- **Response**: 200 OK with updated Task object
- **Error Responses**: 400 Bad Request, 401 Unauthorized, 404 Not Found

### Security Contract

#### Authentication Flow
1. Client includes Authorization: Bearer <token> header
2. Backend extracts and validates JWT
3. Backend extracts user_id from token claims
4. Backend associates user_id with all operations
5. Backend filters all queries by user_id

#### Authorization Rules
- All endpoints require valid JWT
- All data access filtered by authenticated user_id
- No user_id accepted from URL/query/body parameters
- Cross-user access attempts return 404 (not 403 for privacy)

### Error Response Format

#### Standard Error Response
```json
{
  "detail": "Human-readable error message",
  "error_code": "Machine-readable error code"
}
```

#### Common Error Codes
- `AUTHENTICATION_REQUIRED`: 401 - Missing or invalid JWT
- `RESOURCE_NOT_FOUND`: 404 - Resource doesn't exist or belongs to another user
- `VALIDATION_ERROR`: 422 - Request payload validation failed
- `INTERNAL_ERROR`: 500 - Unexpected server error

## Phase 2: Implementation Roadmap

### Sprint 1: Foundation Setup
#### Task 2.1.1: Initialize Project Structure
- **Objective**: Set up FastAPI project with proper directory structure
- **Steps**:
  - Create main.py with FastAPI app instance
  - Configure logging and environment loading
  - Set up basic configuration management
- **Dependencies**: None
- **Acceptance**: Project structure matches spec requirements

#### Task 2.1.2: Environment Configuration
- **Objective**: Implement environment variable management
- **Steps**:
  - Create settings module with Pydantic BaseSettings
  - Define required environment variables (NEON_DATABASE_URL, BETTER_AUTH_SECRET)
  - Implement validation for required variables
- **Dependencies**: Task 2.1.1
- **Acceptance**: Environment variables properly loaded and validated

#### Task 2.1.3: Database Layer Setup
- **Objective**: Configure SQLModel and database connection
- **Steps**:
  - Create db.py with engine and session setup
  - Implement async session dependency
  - Configure connection pooling for Neon compatibility
- **Dependencies**: Task 2.1.2
- **Acceptance**: Database connection established successfully

### Sprint 2: Data Models & Authentication
#### Task 2.2.1: Task Model Implementation
- **Objective**: Create SQLModel model for tasks
- **Steps**:
  - Define Task model with all required fields
  - Implement proper indexing strategy
  - Add validation and default value configurations
- **Dependencies**: Task 2.1.3
- **Acceptance**: Task model matches specification and creates proper database schema

#### Task 2.2.2: JWT Verification Module
- **Objective**: Implement JWT verification functionality
- **Steps**:
  - Create JWT utility module
  - Implement token verification using BETTER_AUTH_SECRET
  - Add token expiry validation
  - Create user_id extraction function
- **Dependencies**: Task 2.1.2
- **Acceptance**: JWT tokens properly verified and user_id extracted

#### Task 2.2.3: Authentication Dependency
- **Objective**: Create reusable auth dependency
- **Steps**:
  - Implement FastAPI dependency for authentication
  - Extract and validate JWT from Authorization header
  - Return current_user_id for use in route handlers
- **Dependencies**: Task 2.2.2
- **Acceptance**: Authentication dependency works across all endpoints

### Sprint 3: API Implementation
#### Task 2.3.1: Task CRUD Routes - Part 1
- **Objective**: Implement GET and POST endpoints for tasks
- **Steps**:
  - Create routes/tasks.py with GET /api/tasks
  - Implement POST /api/tasks with proper validation
  - Apply authentication dependency
  - Implement user_id filtering for queries
- **Dependencies**: Task 2.2.3, Task 2.2.1
- **Acceptance**: GET and POST endpoints work with proper authentication and filtering

#### Task 2.3.2: Task CRUD Routes - Part 2
- **Objective**: Implement PUT, DELETE endpoints for tasks
- **Steps**:
  - Implement GET /api/tasks/{id} with user isolation
  - Implement PUT /api/tasks/{id} with user validation
  - Implement DELETE /api/tasks/{id} with user validation
- **Dependencies**: Task 2.3.1
- **Acceptance**: PUT and DELETE endpoints respect user isolation

#### Task 2.3.3: Task Completion Endpoint
- **Objective**: Implement PATCH endpoint for task completion
- **Steps**:
  - Create PATCH /api/tasks/{id}/complete endpoint
  - Validate completion status in request body
  - Update task completion status with user validation
- **Dependencies**: Task 2.3.2
- **Acceptance**: Task completion endpoint works with proper validation

### Sprint 4: Security & Integration
#### Task 2.4.1: Security Hardening
- **Objective**: Implement comprehensive security measures
- **Steps**:
  - Configure CORS for frontend integration
  - Implement rate limiting if needed
  - Add request validation using Pydantic models
  - Sanitize and validate all inputs
- **Dependencies**: Task 2.3.3
- **Acceptance**: All security measures implemented and tested

#### Task 2.4.2: Error Handling & Logging
- **Objective**: Implement standardized error responses and logging
- **Steps**:
  - Create custom exception handlers
  - Implement structured logging
  - Standardize error response format
  - Log security events appropriately
- **Dependencies**: Task 2.4.1
- **Acceptance**: Error responses follow standard format and proper logging implemented

#### Task 2.4.3: Frontend Integration Validation
- **Objective**: Validate backend works with existing frontend
- **Steps**:
  - Test all endpoints with frontend API calls
  - Verify 401 responses trigger proper frontend behavior
  - Confirm data isolation works correctly
  - Validate response formats match frontend expectations
- **Dependencies**: Task 2.4.2
- **Acceptance**: Backend integrates seamlessly with existing frontend

### Sprint 5: Testing & Validation
#### Task 2.5.1: Unit Testing
- **Objective**: Create comprehensive unit tests
- **Steps**:
  - Write tests for JWT verification module
  - Test database operations and models
  - Validate authentication dependency
  - Test individual route functions
- **Dependencies**: Task 2.4.3
- **Acceptance**: Unit test coverage >= 80% and all tests pass

#### Task 2.5.2: Integration Testing
- **Objective**: Create end-to-end integration tests
- **Steps**:
  - Test complete user workflows
  - Validate cross-user data isolation
  - Test authentication failure scenarios
  - Verify error handling behavior
- **Dependencies**: Task 2.5.1
- **Acceptance**: All integration tests pass and validate requirements

#### Task 2.5.3: Final Validation & Documentation
- **Objective**: Complete final validation and documentation
- **Steps**:
  - Run complete test suite
  - Verify all acceptance criteria met
  - Update API documentation
  - Prepare handoff documentation
- **Dependencies**: Task 2.5.2
- **Acceptance**: All requirements validated and documentation complete

## Risk Assessment

### High-Risk Areas
- **JWT Security**: Vulnerabilities in token validation could allow unauthorized access
- **Data Isolation**: Cross-user data access could expose private information
- **Database Security**: SQL injection or improper parameterization

### Mitigation Strategies
- **Code Reviews**: All authentication and authorization code requires security review
- **Testing**: Comprehensive testing of security boundaries
- **Monitoring**: Structured logging of security-related events

## Success Metrics

### Technical Metrics
- All API endpoints respond within 500ms under normal load
- 99.9% uptime during testing period
- Zero security vulnerabilities in authentication layer

### Business Metrics
- All acceptance criteria from feature spec satisfied
- Frontend integration works without code changes
- Multi-user data isolation fully enforced

## Dependencies & Prerequisites

### External Dependencies
- Neon PostgreSQL database provisioned with proper connection string
- Better Auth configured and issuing valid JWT tokens
- Frontend application available for integration testing

### Internal Dependencies
- Feature specification approved and stable
- Development environment with Python 3.8+
- Access to required environment variables

## Rollback Plan

If implementation fails to meet requirements:
1. Revert all changes to backend code
2. Maintain existing frontend functionality
3. Document lessons learned for future implementation
4. Consider alternative authentication approaches if JWT proves problematic