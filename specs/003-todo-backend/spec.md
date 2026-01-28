# Feature Specification: Todo Backend Implementation

**Feature Branch**: `003-todo-backend`
**Created**: 2026-01-18
**Status**: Draft
**Input**: User description: "Project: Phase II – Todo Full-Stack Web Application (Backend Implementation)

Objective:
Design and implement a complete, secure, and production-ready backend using FastAPI that integrates seamlessly with the already-built Next.js frontend. The backend must support multi-user Todo management with JWT-based authentication and persistent storage using Neon PostgreSQL.

Tech Stack:
- Backend Framework: FastAPI
- Language: Python
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT verification only)
- Architecture: Monorepo with Spec-Kit

Environment Configuration:
- Database connection must use environment variable: NEON_DATABASE_URL
- JWT verification must use environment variable: BETTER_AUTH_SECRET
- Backend must trust JWTs issued by Better Auth frontend
- No secrets may be hardcoded

Core Backend Responsibilities:

1. Authentication & Authorization
- Backend must not implement signup or signin
- Backend must only verify JWT tokens issued by Better Auth
- JWT must be extracted from:
  Authorization: Bearer <token>
- Backend must:
  - Verify JWT signature using BETTER_AUTH_SECRET
  - Validate token expiry
  - Extract authenticated user_id and email from token
- user_id must never be accepted via:
  - URL parameters
  - Request body
  - Query parameters

2. API Security Rules
- All API endpoints must require valid JWT
- Requests without valid JWT must return 401 Unauthorized
- Requests attempting to access other users' data must be denied
- User isolation must be enforced at:
  - API layer
  - Database query layer

3. REST API Design
- Base path: /api
- Endpoints:
  - GET    /api/tasks
  - POST   /api/tasks
  - GET    /api/tasks/{id}
  - PUT    /api/tasks/{id}
  - DELETE /api/tasks/{id}
  - PATCH  /api/tasks/{id}/complete
- API behavior must exactly match frontend expectations
- All task queries must be filtered by authenticated user_id

4. Database Design & Persistence
- Use SQLModel for all database interactions
- Connect to Neon PostgreSQL using NEON_DATABASE_URL
- Database schema must include:
  Table: tasks
    - id (primary key, integer)
    - user_id (string, required)
    - title (string, required)
    - description (text, optional)
    - completed (boolean, default false)
    - created_at (timestamp)
    - updated_at (timestamp)
- Index user_id for efficient filtering
- Do not create or manage users table (Better Auth owns users)

5. Backend Project Structure
- main.py → FastAPI app entry point
- db.py → database engine and session
- models.py → SQLModel models
- routes/ → API route handlers
- dependencies/ → auth and database dependencies
- middleware/ → JWT verification (if applicable)

6. Frontend Integration Requirements
- Backend must support CORS for Next.js frontend
- API responses must be JSON and frontend-friendly
- Error responses must be consistent and predictable
- 401 responses must trigger frontend logout/redirect behavior
- Backend must not require frontend changes to integrate

7. Validation & Error Handling
- Validate request payloads using Pydantic models
- Handle:
  - Invalid JWT
  - Expired JWT
  - Missing resources (404)
  - Unauthorized access (401)
- Return meaningful HTTP status codes

8. Constraints
- No frontend code modifications in this phase
- No authentication UI or session handling in backend
- No manual coding outside agent execution
- Follow Spec-Kit and CLAUDE.md rules strictly

Acceptance Criteria:
- Backend runs independently
- JWT-secured APIs function correctly
- Tasks persist in Neon database
- Multi-user data isolation is enforced
- Frontend integrates without modification
- Backend passes all integration scenarios defined in specs

Output:
- Backend-related specs under:
  - /specs/api
  - /specs/database
- Complete FastAPI backend implementation
- No frontend or UI code"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Management (Priority: P1)

As an authenticated user, I want to create, read, update, and delete my personal tasks through a secure API, so that I can manage my productivity while ensuring my data remains private and protected from other users.

**Why this priority**: This is the core functionality of the todo application and represents the essential value proposition for users. Without secure task management, the application serves no purpose.

**Independent Test**: Can be fully tested by authenticating with a JWT token, performing CRUD operations on tasks, and verifying that only the authenticated user's tasks are accessible. Delivers core value of managing personal tasks securely.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token, **When** user creates a new task via POST /api/tasks, **Then** the task is saved to the database linked to the user's ID and returns a success response
2. **Given** user has created tasks and is authenticated, **When** user requests GET /api/tasks, **Then** only tasks belonging to the authenticated user are returned
3. **Given** user has tasks and is authenticated, **When** user attempts to access another user's task via GET /api/tasks/{id}, **Then** a 404 or 403 error is returned

---

### User Story 2 - Authentication and Authorization (Priority: P1)

As a user of the todo application, I want the backend to validate my authentication token on every request, so that unauthorized users cannot access or manipulate my data.

**Why this priority**: Security is paramount for any application handling user data. Without proper authentication and authorization, the application would be vulnerable to data breaches and unauthorized access.

**Independent Test**: Can be fully tested by making requests with valid tokens, expired tokens, invalid tokens, and no tokens, and verifying appropriate responses (200 for valid, 401 for invalid/unauthorized). Delivers protection of user data through proper access controls.

**Acceptance Scenarios**:

1. **Given** user has a valid JWT token, **When** user makes any API request with Authorization: Bearer <token>, **Then** the request is processed normally
2. **Given** user has an expired or invalid JWT token, **When** user makes any API request, **Then** a 401 Unauthorized response is returned
3. **Given** user makes a request without any authentication token, **When** request reaches the API, **Then** a 401 Unauthorized response is returned

---

### User Story 3 - Task Completion Tracking (Priority: P2)

As a user managing my tasks, I want to be able to mark tasks as completed or incomplete, so that I can track my progress and organize my workload effectively.

**Why this priority**: This enhances the core task management functionality by adding state management for tasks, which is essential for productivity tracking.

**Independent Test**: Can be fully tested by creating tasks, updating their completion status via PATCH /api/tasks/{id}/complete, and verifying the status updates correctly. Delivers value by allowing users to track task progress.

**Acceptance Scenarios**:

1. **Given** user has an existing task, **When** user sends PATCH /api/tasks/{id}/complete with completed: true, **Then** the task's completed status is updated to true
2. **Given** user has a completed task, **When** user sends PATCH /api/tasks/{id}/complete with completed: false, **Then** the task's completed status is updated to false
3. **Given** user attempts to update another user's task completion status, **When** PATCH request is made, **Then** a 404 or 403 error is returned

---

### Edge Cases

- What happens when a JWT token expires mid-request? The system should validate token expiry before processing the request and return 401 if expired.
- How does the system handle database connection failures? The system should return appropriate server error responses (5xx) when database connectivity issues occur.
- What occurs when a user tries to access a non-existent task ID? The system should return a 404 Not Found response.
- How does the system handle malformed JWT tokens? The system should return a 401 Unauthorized response.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST follow spec-first development - all work originates from files inside the /specs directory
- **FR-002**: System MUST ensure agent responsibility boundaries are respected - each agent operates within its defined role
- **FR-003**: System MUST ensure no manual coding - all implementation performed by agents based on specs
- **FR-004**: System MUST handle authentication via Better Auth on frontend - backend never manages passwords or sessions
- **FR-005**: System MUST derive user identity from verified JWT token
- **FR-006**: System MUST ensure user_id is never accepted from URL parameters or request bodies
- **FR-007**: System MUST require authentication for all API endpoints (unless explicitly stated otherwise)
- **FR-008**: System MUST return 401 for unauthorized requests
- **FR-009**: System MUST ensure users can only access and modify their own data
- **FR-010**: System MUST follow RESTful conventions for API endpoints
- **FR-011**: System MUST match API endpoints exactly to API specs: GET /api/tasks, POST /api/tasks, GET /api/tasks/{id}, PUT /api/tasks/{id}, DELETE /api/tasks/{id}, PATCH /api/tasks/{id}/complete
- **FR-012**: System MUST align backend behavior with acceptance criteria, not assumptions
- **FR-013**: System MUST ensure the users table is owned and managed externally by Better Auth
- **FR-014**: System MUST ensure backend database schema does not duplicate user credentials
- **FR-015**: System MUST ensure all task records reference users via user_id
- **FR-016**: System MUST ensure all backend communication goes through a centralized API client
- **FR-017**: System MUST ensure JWT tokens are securely handled and attached automatically to requests
- **FR-018**: System MUST ensure protected pages are not accessible to unauthenticated users
- **FR-019**: System MUST maintain frontend and backend in a single monorepo with clear separation
- **FR-020**: System MUST validate every feature against its acceptance criteria
- **FR-021**: System MUST perform integration testing to confirm end-to-end behavior
- **FR-022**: System MUST verify JWT signature using BETTER_AUTH_SECRET environment variable
- **FR-023**: System MUST connect to Neon PostgreSQL using NEON_DATABASE_URL environment variable
- **FR-024**: System MUST implement proper error handling for invalid JWT, expired JWT, missing resources (404), and unauthorized access (401)
- **FR-025**: System MUST ensure all task queries are filtered by authenticated user_id to enforce user isolation
- **FR-026**: System MUST support CORS for Next.js frontend integration
- **FR-027**: System MUST return JSON responses that are compatible with frontend expectations
- **FR-028**: System MUST validate request payloads using Pydantic models
- **FR-029**: System MUST return meaningful HTTP status codes for all responses
- **FR-030**: System MUST ensure the tasks database table contains id (primary key, integer), user_id (string, required), title (string, required), description (text, optional), completed (boolean, default false), created_at (timestamp), updated_at (timestamp)

### Key Entities

- **Task**: Represents a user's personal task with properties like title, description, completion status, timestamps, and user association
- **User**: Represents an authenticated user identified by user_id extracted from JWT token, with ownership relationship to tasks
- **Authentication Token**: Represents the JWT token issued by Better Auth that provides user identity and access rights

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Backend runs independently and serves requests without crashing under normal load conditions
- **SC-002**: All JWT-secured APIs function correctly with proper authentication and authorization validation
- **SC-003**: Tasks persist reliably in Neon PostgreSQL database with proper data integrity
- **SC-004**: Multi-user data isolation is enforced completely - users cannot access or modify other users' tasks
- **SC-005**: Frontend integrates seamlessly with backend without requiring any modifications to existing frontend code
- **SC-006**: Backend passes all defined integration scenarios with 100% success rate
- **SC-007**: API endpoints respond with appropriate status codes (200 for success, 401 for unauthorized, 404 for not found, etc.)
- **SC-008**: Database queries consistently filter tasks by user_id, ensuring data privacy between users