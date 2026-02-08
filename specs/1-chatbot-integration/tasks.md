---
description: "Task list for Todo AI Chatbot Integration implementation"
---

# Tasks: Todo AI Chatbot Integration

**Input**: Design documents from `/specs/1-chatbot-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend/src/models/conversation.py with SQLModel for Conversation entity
- [X] T002 Create backend/src/models/message.py with SQLModel for Message entity
- [X] T003 [P] Install OpenAI and MCP SDK dependencies in backend requirements
- [X] T004 [P] Install OpenAI ChatKit dependencies in frontend package.json

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create database migration for conversation and message tables
- [X] T006 [P] Create backend/src/services/conversation_service.py with CRUD operations
- [X] T007 [P] Create backend/src/api/chat_router.py with POST /api/chat endpoint
- [X] T008 Create backend/src/mcp_server/server.py for MCP tools
- [X] T009 Create backend/src/mcp_server/tools/add_task_tool.py
- [X] T010 Create backend/src/mcp_server/tools/list_tasks_tool.py
- [X] T011 Create backend/src/mcp_server/tools/complete_task_tool.py
- [X] T012 Create backend/src/mcp_server/tools/update_task_tool.py
- [X] T013 Create backend/src/mcp_server/tools/delete_task_tool.py
- [X] T014 Create backend/src/services/chat_service.py to coordinate chat operations
- [X] T015 Create frontend/src/components/ChatBotIcon.tsx component
- [X] T016 Create frontend/src/components/ChatPanel.tsx component
- [X] T017 Create frontend/src/components/ChatKitWrapper.tsx component
- [X] T018 Create frontend/src/providers/ChatKitProvider.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to manage tasks using natural language commands like adding, listing, and completing tasks

**Independent Test**: Can be fully tested by sending natural language commands like "Add a task to buy groceries" and verifying that a new task is created in the system, delivering the value of effortless task creation.

### Implementation for User Story 1

- [X] T019 [P] [US1] Implement add_task MCP tool to create tasks for authenticated user
- [X] T020 [P] [US1] Implement list_tasks MCP tool to return user's tasks filtered by status
- [X] T021 [P] [US1] Implement complete_task MCP tool to mark tasks as completed
- [X] T022 [US1] Create backend/src/services/chat_service.py to handle conversation lifecycle
- [X] T023 [US1] Implement POST /api/chat endpoint with JWT authentication
- [X] T024 [US1] Implement conversation creation and retrieval logic
- [X] T025 [US1] Implement message persistence for user and assistant messages
- [X] T026 [US1] Configure OpenAI agent with system instructions and MCP tools
- [X] T027 [US1] Create frontend/src/components/ChatBotIcon.tsx with floating button
- [X] T028 [US1] Create frontend/src/components/ChatPanel.tsx with open/close behavior
- [X] T029 [US1] Connect frontend chat UI to backend POST /api/chat endpoint
- [X] T030 [US1] Implement JWT token passing from existing auth middleware

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Conversational Task Operations (Priority: P1)

**Goal**: Enable authenticated users to perform all task CRUD operations through the chatbot (create, read, update, delete)

**Independent Test**: Can be fully tested by performing all CRUD operations (create, read, update, delete) through natural language commands and verifying the corresponding changes in the task system, delivering complete task management capability.

### Implementation for User Story 2

- [X] T031 [P] [US2] Enhance update_task MCP tool to update task title and description
- [X] T032 [P] [US2] Enhance delete_task MCP tool to safely delete tasks
- [X] T033 [US2] Add update_task functionality to chat agent
- [X] T034 [US2] Add delete_task functionality to chat agent
- [X] T035 [US2] Test update and delete operations through chat interface

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Persistent Conversation History (Priority: P2)

**Goal**: Ensure conversation history persists across sessions so users can continue conversations

**Independent Test**: Can be fully tested by starting a conversation, closing the chat, reopening it, and continuing the conversation with context from previous messages, delivering a seamless conversational experience.

### Implementation for User Story 3

- [X] T036 [US3] Enhance conversation retrieval to load full message history
- [X] T037 [US3] Implement conversation_id lifecycle management in frontend
- [X] T038 [US3] Add conversation history display in ChatPanel component
- [X] T039 [US3] Test conversation persistence across page refreshes and sessions

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - User Information Access (Priority: P2)

**Goal**: Allow users to ask the chatbot for basic user information like their logged-in identity

**Independent Test**: Can be fully tested by asking "Who am I logged in as?" and receiving the correct user information, delivering account awareness functionality.

### Implementation for User Story 4

- [X] T040 [US4] Implement user information retrieval from JWT in chat service
- [X] T041 [US4] Add user info functionality to AI agent system instructions
- [X] T042 [US4] Test user identity queries through chat interface

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T043 [P] Add error handling for task not found scenarios
- [X] T044 [P] Add error handling for invalid input scenarios
- [X] T045 [P] Add security validation to ensure user isolation
- [X] T046 [P] Implement tool chaining for multi-step operations
- [X] T047 [P] Add friendly confirmation messages for all operations
- [X] T048 [P] Ensure Roman Urdu + simple English response format
- [X] T049 [P] Update README with Chatbot setup instructions
- [X] T050 Run end-to-end validation of all user stories

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 functionality
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 functionality
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 functionality

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all implementation tasks for User Story 1 together:
Task: "Implement add_task MCP tool to create tasks for authenticated user"
Task: "Implement list_tasks MCP tool to return user's tasks filtered by status"
Task: "Implement complete_task MCP tool to mark tasks as completed"
Task: "Create frontend/src/components/ChatBotIcon.tsx with floating button"
Task: "Create frontend/src/components/ChatPanel.tsx with open/close behavior"
```

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
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All constitutional requirements must be maintained (stateless, JWT-based identity, MCP-only mutations, user isolation)