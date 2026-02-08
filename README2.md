/sp.constitution

Project: Phase II – Todo Full-Stack Web Application

Purpose:
This constitution defines the non-negotiable rules, principles, and boundaries that all agents must follow while designing and implementing Phase II of the Todo Full-Stack Web Application using a spec-driven, agentic workflow.

Constitution Principles:

1. Spec-First Development
- No agent may implement or modify code without an explicit, approved specification.
- All work must originate from files inside the /specs directory.
- Specs are the single source of truth.

2. Agent Responsibility Boundaries
- Each agent must operate strictly within its defined role.
- No agent may perform another agent’s responsibility.
- Cross-cutting changes must be coordinated through the Primary Orchestrator.

3. No Manual Coding Rule
- Humans do not write application code.
- All implementation is performed by agents based on specs.
- Any deviation must be reflected first in specs.

4. Authentication & Identity Rule
- User authentication is handled exclusively by Better Auth on the frontend.
- Backend never manages passwords or sessions.
- User identity must always be derived from a verified JWT token.
- user_id must never be accepted from URL parameters or request bodies.

5. Security First
- All API endpoints require authentication unless explicitly stated otherwise.
- Unauthorized requests must return 401.
- Users can only access and modify their own data.
- Data isolation is mandatory at API and database levels.

6. API Design Rules
- RESTful conventions must be followed.
- API endpoints must match the API specs exactly.
- Backend behavior must align with acceptance criteria, not assumptions.

7. Database Ownership Rule
- The users table is owned and managed externally by Better Auth.
- Backend database schema must not duplicate user credentials.
- All task records must reference users via user_id.

8. Frontend Rules
- All backend communication must go through a centralized API client.
- JWT tokens must be securely handled and attached automatically.
- Protected pages must not be accessible to unauthenticated users.

9. Monorepo Discipline
- Frontend and backend live in a single monorepo.
- Specs, frontend, and backend must remain clearly separated.
- CLAUDE.md files define navigation and behavioral rules for agents.

10. Validation & Compliance
- Every feature must be validated against its acceptance criteria.
- Integration testing must confirm end-to-end behavior.
- If implementation and spec conflict, the spec must be updated first.

Enforcement:
- Any violation of this constitution invalidates the implementation.
- Agents must stop and report if a rule conflict is detected.

Outcome:
A secure, scalable, multi-user, spec-driven full-stack Todo application that strictly follows agentic development principles.


##################################################################################
FRONTEND PROMPT
##################################################################################

/sp.specify

Project: Phase II – Todo Full-Stack Web Application (Frontend First)

Objective:
Design and implement a modern, professional, and production-quality frontend for a multi-user Todo application using Next.js (App Router). The frontend must be built first, with backend integration planned but abstracted behind a clean API client.

Tech Stack:
- Framework: Next.js 16+ (App Router)
- Language: TypeScript
- Styling: Tailwind CSS
- Authentication: Better Auth (JWT-based)
- State Management: React Server Components + minimal client state
- Architecture: Monorepo with Spec-Kit

Frontend Design Goals:
- Clean, minimal, professional UI (SaaS-grade)
- Responsive design (desktop, tablet, mobile)
- Fast initial load using Server Components
- Clear user feedback (loading, empty states, errors)
- Accessibility-aware components

Core Frontend Features:

1. Authentication UI
- Signup page
- Signin page
- Auth-aware navigation
- Loading and error states
- Redirect unauthenticated users to signin

2. Layout & Navigation
- App-wide layout with header and content area
- User context visible (email or avatar)
- Logout action
- Protected routes under authenticated layout

3. Todo Dashboard
- Task list view
- Create task form (inline or modal)
- Edit task
- Delete task (with confirmation)
- Toggle task completion
- Empty state UI when no tasks exist

4. UI/UX Requirements
- Use reusable components (buttons, inputs, modals, cards)
- Consistent spacing, typography, and color system
- Clear visual hierarchy
- Subtle animations or transitions where appropriate
- No cluttered layouts

5. API Abstraction (Frontend Only)
- All backend communication must go through a centralized API client
- API client must automatically attach JWT token
- Backend implementation is abstracted and mocked if needed

6. Error & State Handling
- Graceful handling of loading states
- 401 handling (auto redirect to signin)
- Form validation feedback
- User-friendly error messages

7. Folder Structure
- /app → routing and layouts
- /components → reusable UI components
- /lib → api client and auth helpers
- /styles → global styles (if needed)

Constraints:
- No backend implementation in this phase
- No direct API calls outside the API client
- UI must be production-ready, not demo-style
- Follow Spec-Kit conventions strictly
- No manual coding outside agent execution

Acceptance Criteria:
- Frontend runs independently
- Auth flows function visually and logically
- Todo UI fully usable with mocked or abstracted data
- UI quality matches professional SaaS standards
- Codebase is clean, scalable, and spec-driven

Output:
- Frontend-focused specs under /specs/ui and /specs/features
- No backend code
- No database logic

-----------------------------------------------------------------------------

/sp.plan

Project: Phase II – Todo Full-Stack Web Application (Frontend First)

Goal:
Generate a detailed, step-by-step execution plan to design and implement a production-quality frontend for a multi-user Todo application using Next.js (App Router), before backend integration.

Planning Requirements:
- Follow the approved frontend-first specification
- Adhere strictly to Spec-Kit conventions
- Respect agent responsibility boundaries
- No backend or database implementation in this phase

Plan Must Include:

1. Specification Breakdown
- Identify all frontend-related specs to be created or updated
- Define spec file locations under:
  - /specs/ui
  - /specs/features
- Map each spec to a concrete UI outcome

2. Information Architecture
- Define page structure and routing using App Router
- Public vs protected routes
- Layout hierarchy (auth layout vs app layout)

3. UI Component Strategy
- Identify reusable UI components (buttons, inputs, modals, cards)
- Define component responsibilities and reusability rules
- Establish consistent design patterns

4. Authentication Flow (Frontend Only)
- Signup and signin UI flow
- Auth-aware navigation and layouts
- Redirect logic for unauthenticated users
- Logout behavior

5. Todo Dashboard Flow
- Task list display states (loading, empty, populated)
- Create, edit, delete, and complete task UI flows
- Confirmation and feedback patterns

6. API Client Abstraction
- Define centralized API client responsibilities
- JWT attachment strategy
- Mock or placeholder data handling
- Error normalization approach

7. State & Error Handling
- Loading indicators
- Form validation feedback
- Global error handling strategy
- 401 and session-expired handling

8. Styling & UX Quality
- Tailwind usage guidelines
- Spacing, typography, and color consistency
- Accessibility considerations
- Responsive behavior across screen sizes

9. Integration Readiness
- Clearly mark backend-dependent areas
- Ensure API contracts align with future backend specs
- Avoid frontend rewrites during backend integration

10. Validation & Review
- UI quality checklist (professional SaaS standard)
- Functional validation steps
- Spec compliance verification

Output Format:
- Ordered execution roadmap
- Each step clearly linked to specs
- No implementation code
- Clear handoff points for backend phase


---------------------------------------------------------------------------------

/sp.tasks

---------------------------------------------------------------------------------

/sp.implement

---------------------------------------------------------------------------------

better auth search on google
https://www.better-auth.com/
docs on click
installation on click
2.Set Environment Variables (1. Secret Key main Generate secrete on click then copy key and paste .env file)

Create a .env file on frontend
BETTER_AUTH_SECRET=RUsCCUetloa99hxgGomI36Gk9fy8Ubaf
BETTER_AUTH_URL=https://localhost:8000/



######################################################################
BACKEND PROMPT
######################################################################


Ab mjhe backend banana hai mere hackathon ka document already tumhare pass hai jissey humne frontend bnaya hai.
Ab mjhe backend ky liye /sp.specify ki prompt likh kar do or prompt aesa ho jo full backend bana kar dy or integrate bhi ho jaye frontend ky sath.
Or ye meri .env ki file hai
NEON_DATABASE_URL='postgresql://neondb_owner:npg_6QrC0nugmDHc@ep-long-rain-ahu2hj7j-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
BETTER_AUTH_SECRET=RUsCCUetloa99hxgGomI36Gk9fy8Ubaf
BETTER_AUTH_URL=https://localhost:3000/

Ab mjhe full detail ky sath backend ky liye /sp.specify ki prompt bna kar do


----------------------------------------------------------------------

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
- Requests attempting to access other users’ data must be denied
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

-------------------------------------------------------------------

/sp.plan

Project: Phase II – Todo Full-Stack Web Application (Backend)

Goal:
Generate a complete, step-by-step execution plan to implement a secure, production-ready FastAPI backend that integrates seamlessly with the already-built Next.js frontend. The backend must support JWT-based authentication, user-scoped task management, and persistent storage using Neon PostgreSQL.

Planning Constraints:
- Frontend is already implemented and must not be changed
- Authentication UI and signup/signin are handled by Better Auth on frontend
- Backend must only verify JWT and enforce authorization
- Follow Spec-Kit and CLAUDE.md rules strictly
- No manual coding

The Plan Must Include:

1. Spec Review & Alignment
- Identify all backend-relevant specs to read and enforce:
  - /specs/api
  - /specs/database
  - /specs/features (task-crud, authentication)
- Verify API contracts match frontend expectations
- Confirm acceptance criteria for backend responsibilities

2. Backend Project Initialization
- Define FastAPI project structure
- Configure application entry point
- Configure environment variable loading
- Prepare backend to run independently

3. Database Integration (Neon PostgreSQL)
- Configure database engine using NEON_DATABASE_URL
- Initialize SQLModel session handling
- Ensure connection pooling compatibility with Neon
- Define database lifecycle management

4. Database Schema Implementation
- Define SQLModel models for tasks
- Apply constraints, defaults, and indexes
- Ensure user_id is mandatory on all task records
- Prepare schema for multi-user scalability

5. Authentication & JWT Verification
- Design JWT verification flow
- Extract token from Authorization header
- Verify token signature using BETTER_AUTH_SECRET
- Validate token expiry
- Extract authenticated user_id and email
- Reject invalid or missing tokens with 401

6. Authorization Dependency Design
- Create a reusable dependency to provide current authenticated user
- Ensure no route accepts user_id from request body or URL
- Centralize auth logic for all routes

7. API Route Implementation
- Implement REST endpoints under /api:
  - GET /api/tasks
  - POST /api/tasks
  - GET /api/tasks/{id}
  - PUT /api/tasks/{id}
  - DELETE /api/tasks/{id}
  - PATCH /api/tasks/{id}/complete
- Enforce user-scoped queries on every operation
- Validate request payloads using Pydantic models

8. Error Handling Strategy
- Standardize error responses
- Handle:
  - Unauthorized access (401)
  - Forbidden access attempts
  - Resource not found (404)
  - Validation errors (422)
- Ensure frontend-friendly error formats

9. CORS & Frontend Integration
- Configure CORS to allow frontend origin
- Support Authorization headers
- Ensure compatibility with frontend API client
- Do not require frontend changes

10. Security Enforcement
- Confirm no endpoint bypasses authentication
- Validate that users cannot access others’ tasks
- Ensure sensitive information is never logged
- Follow security-first principles

11. Testing & Integration Validation
- Define end-to-end backend test scenarios:
  - Valid JWT → successful request
  - Missing JWT → 401
  - Invalid JWT → 401
  - Cross-user access attempt → denied
- Validate database persistence
- Confirm frontend-backend contract correctness

12. Final Review & Readiness
- Verify all specs are satisfied
- Confirm backend runs cleanly
- Ensure backend is ready for hackathon evaluation
- Prepare handoff notes for Phase II completion

Output Format:
- Ordered execution roadmap
- Each step mapped to backend responsibilities
- No implementation code
- Clear integration checkpoints with frontend


-------------------------------------------------------------------

/sp.tasks

------------------------------------------------------------------

/sp.implement

-------------------------------------------------------------------

################################################################################################
################################################################################################

Ab mainey phase 2 todo full stack web apllication main agent or skill ky bad ye abhi jo sara prompt bheja hai frontend or backend asey mainey ye bhi bna lia hai ab mere todo web application successfully ban gai hai tm es ko dekh lo achy sy