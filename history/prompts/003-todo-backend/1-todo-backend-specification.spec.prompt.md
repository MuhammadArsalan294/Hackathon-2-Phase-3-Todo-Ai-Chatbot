---
id: 1
title: "Todo Backend Specification"
stage: spec
date_iso: "2026-01-18"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "003-todo-backend"
branch: "003-todo-backend"
user: "user"
command: "/sp.specify"
labels: ["specification", "backend", "fastapi", "todo"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - "specs/003-todo-backend/spec.md"
  - "specs/003-todo-backend/checklists/requirements.md"
tests_yaml: []
---

## Prompt Text

```
/sp.specify

Project: Phase II – Todo Full-Stack Web Application (Backend Implementation)

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
- No frontend or UI code
```

## Response Text

Created comprehensive specification for the Todo Backend Implementation feature. The specification includes:

- Three prioritized user stories covering secure task management, authentication/authorization, and task completion tracking
- Detailed acceptance scenarios for each user story
- Identified edge cases for JWT expiration, database failures, and access control
- 30 functional requirements covering authentication, data isolation, API behavior, and error handling
- Key entities definition for Task, User, and Authentication Token
- 8 measurable success criteria focusing on backend performance, security, and integration

The specification has been validated through a quality checklist and is ready for the planning phase.

## Outcome

The specification for the Todo Backend Implementation has been successfully created and validated. It comprehensively covers all requirements from the original feature description including JWT-based authentication, user isolation, REST API design, and database persistence. The spec is ready for the planning phase.