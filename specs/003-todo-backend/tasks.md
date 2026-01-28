---
description: "Task list for Todo Backend Implementation"
---

# Tasks: Todo Backend Implementation

**Input**: Design documents from `/specs/003-todo-backend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/` at repository root
- Paths adjusted for the Todo Backend implementation

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in backend/
- [X] T002 Initialize Python project with FastAPI, SQLModel, PyJWT dependencies in backend/
- [X] T003 [P] Configure linting and formatting tools in backend/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Setup database schema and migrations framework using SQLModel in backend/db.py (respecting Database Ownership Rule)
- [X] T005 [P] Implement authentication/authorization framework with JWT verification in backend/auth/jwt_handler.py (using Better Auth, JWT tokens)
- [X] T006 [P] Setup API routing and middleware structure following RESTful conventions in backend/main.py
- [X] T007 Create base Task model in backend/models/task.py with user_id references
- [X] T008 Configure error handling and logging infrastructure returning 401 for unauthorized access in backend/utils/errors.py
- [X] T009 Setup environment configuration management with NEON_DATABASE_URL and BETTER_AUTH_SECRET in backend/config/settings.py
- [X] T010 Establish centralized API client for backend communication in backend/api/client.py
- [X] T011 Implement user data isolation mechanisms ensuring users can only access own data in backend/services/task_service.py
- [X] T012 Set up user authentication checks for protected pages in backend/dependencies/auth.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Secure Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to create, read, update, and delete their personal tasks through a secure API with data isolation

**Independent Test**: Authenticate with a JWT token, perform CRUD operations on tasks, and verify that only the authenticated user's tasks are accessible

### Implementation for User Story 1

- [X] T013 [P] [US1] Create Task model in backend/models/task.py with all required fields (id, user_id, title, description, completed, timestamps)
- [X] T014 [P] [US1] Create TaskCreate and TaskUpdate Pydantic schemas in backend/schemas/task.py
- [X] T015 [US1] Implement TaskService in backend/services/task_service.py with CRUD operations and user isolation (depends on T013)
- [X] T016 [US1] Implement GET /api/tasks endpoint in backend/routes/tasks.py with authentication and user filtering (depends on T015)
- [X] T017 [US1] Implement POST /api/tasks endpoint in backend/routes/tasks.py with authentication and user assignment (depends on T015)
- [X] T018 [US1] Implement GET /api/tasks/{id} endpoint in backend/routes/tasks.py with authentication and user validation (depends on T015)
- [X] T019 [US1] Implement PUT /api/tasks/{id} endpoint in backend/routes/tasks.py with authentication and user validation (depends on T015)
- [X] T020 [US1] Implement DELETE /api/tasks/{id} endpoint in backend/routes/tasks.py with authentication and user validation (depends on T015)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Authentication and Authorization (Priority: P1)

**Goal**: Ensure the backend validates authentication token on every request to prevent unauthorized access to user data

**Independent Test**: Make requests with valid tokens, expired tokens, invalid tokens, and no tokens, and verify appropriate responses (200 for valid, 401 for invalid/unauthorized)

### Implementation for User Story 2

- [X] T021 [P] [US2] Enhance JWT verification module in backend/auth/jwt_handler.py with expiry validation
- [X] T022 [US2] Create reusable authentication dependency in backend/dependencies/auth.py to extract user_id from token (depends on T021)
- [X] T023 [US2] Apply authentication dependency to all existing task endpoints in backend/routes/tasks.py (depends on T022)
- [X] T024 [US2] Implement 401 response handling for invalid/expired tokens in backend/utils/errors.py
- [X] T025 [US2] Add request logging for authentication events in backend/middleware/logging.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Completion Tracking (Priority: P2)

**Goal**: Allow users to mark tasks as completed or incomplete to track progress and organize workload

**Independent Test**: Create tasks, update their completion status via PATCH /api/tasks/{id}/complete, and verify the status updates correctly

### Implementation for User Story 3

- [X] T026 [P] [US3] Create TaskCompletionUpdate Pydantic schema in backend/schemas/task.py
- [X] T027 [US3] Enhance TaskService with completion update method in backend/services/task_service.py (depends on T015)
- [X] T028 [US3] Implement PATCH /api/tasks/{id}/complete endpoint in backend/routes/tasks.py with authentication and user validation (depends on T027)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T029 [P] Add comprehensive documentation in backend/docs/
- [X] T030 Add CORS middleware configuration for Next.js frontend integration in backend/main.py
- [X] T031 [P] Add unit tests for all services in backend/tests/unit/
- [X] T032 Add integration tests for all endpoints in backend/tests/integration/
- [X] T033 Security hardening and validation
- [X] T034 Run validation to ensure all acceptance criteria are met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Integrates with US1 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence