# Implementation Plan: Todo AI Chatbot Integration

**Branch**: `1-chatbot-integration` | **Date**: 2026-02-04 | **Spec**: [specs/1-chatbot-integration/spec.md](../1-chatbot-integration/spec.md)

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an AI-powered chatbot integrated into the existing Todo web application that allows authenticated users to manage tasks using natural language. The system will leverage OpenAI ChatKit for the frontend UI, MCP tools for safe data operations, and maintain stateless server architecture while ensuring strict user isolation and JWT-based authentication.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript, Next.js 14+ with App Router
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Neon PostgreSQL, OpenAI ChatKit
**Storage**: Neon PostgreSQL database with existing task schema plus new conversation/message tables
**Testing**: pytest for backend, Jest/Vitest for frontend
**Target Platform**: Web server (Linux/Windows/Mac compatible), Browser-based frontend
**Project Type**: Web application (integrated into existing frontend/backend)
**Performance Goals**: Handle 100 concurrent conversations, respond within 3 seconds for 90% of interactions
**Constraints**: <200ms p95 for database operations, stateless server architecture, user isolation required
**Scale/Scope**: Support thousands of users with persistent conversations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-First Development Compliance
- [x] All work originates from files inside the /specs directory
- [x] Specifications are the single source of truth
- [x] No implementation without explicit, approved specification

### Agent Responsibility Boundaries Compliance
- [x] Plan respects agent role boundaries
- [x] Cross-cutting changes coordinated through Primary Orchestrator
- [x] No agent performing another agent's responsibility

### No Manual Coding Rule Compliance
- [x] Plan supports agent-based implementation
- [x] No provisions for manual human code writing
- [x] Deviations reflected in specs first

### Authentication & Identity Rule Compliance
- [x] Frontend authentication handled by Better Auth
- [x] Backend does not manage passwords or sessions
- [x] User identity derived from verified JWT token
- [x] user_id not accepted from URL parameters or request bodies

### Security First Compliance
- [x] All API endpoints require authentication (unless explicitly stated)
- [x] Unauthorized requests return 401
- [x] User data isolation at API and database levels
- [x] Users can only access/modify own data

### API Design Rules Compliance
- [x] RESTful conventions followed
- [x] API endpoints match API specs exactly
- [x] Backend behavior aligns with acceptance criteria

### Database Ownership Rule Compliance
- [x] Users table managed externally by Better Auth
- [x] No duplicated user credentials in backend schema
- [x] Task records reference users via user_id

### Frontend Rules Compliance
- [x] Backend communication through centralized API client
- [x] JWT tokens handled securely and attached automatically
- [x] Protected pages inaccessible to unauthenticated users

### Monorepo Discipline Compliance
- [x] Frontend and backend in single monorepo
- [x] Clear separation of specs, frontend, and backend
- [x] CLAUDE.md files define navigation and behavioral rules

### Validation & Compliance Check
- [x] Features validated against acceptance criteria
- [x] Integration testing confirms end-to-end behavior
- [x] Spec updates precede implementation when conflicts arise

### Phase III Constitution Compliance
- [x] Integration Over Replacement - Chatbot supplements existing UI
- [x] MCP-Only Mutations - All data changes through MCP tools
- [x] Reuse Phase II Backend Logic - Leverage existing task services
- [x] Stateless Chat Server - No in-memory conversation state
- [x] JWT-Based User Identity - Extract identity from JWT only
- [x] User Isolation Guarantee - Strict user data separation
- [x] AI Agent Behavior Rules - Follow allowed/forbidden behaviors
- [x] Tool Usage Rules - Stateless, explicit, idempotent tools
- [x] Conversation Persistence - Store in database only

## Project Structure

### Documentation (this feature)

```text
specs/1-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py
│   │   ├── message.py
│   │   └── __init__.py
│   ├── services/
│   │   ├── chat_service.py
│   │   ├── conversation_service.py
│   │   └── __init__.py
│   ├── api/
│   │   ├── chat_router.py
│   │   └── __init__.py
│   ├── mcp_server/
│   │   ├── server.py
│   │   ├── tools/
│   │   │   ├── add_task_tool.py
│   │   │   ├── list_tasks_tool.py
│   │   │   ├── complete_task_tool.py
│   │   │   ├── delete_task_tool.py
│   │   │   └── update_task_tool.py
│   │   └── __init__.py
│   └── main.py
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── ChatBotIcon.tsx
│   │   ├── ChatPanel.tsx
│   │   └── ChatKitWrapper.tsx
│   ├── pages/
│   │   └── api/
│   │       └── chat.ts
│   ├── services/
│   │   └── api-client.ts
│   └── providers/
│       └── ChatKitProvider.tsx
└── tests/
```

**Structure Decision**: Web application structure chosen since the feature involves both frontend (ChatKit integration) and backend (API, MCP tools) components. The existing monorepo structure is extended with new components for the chatbot functionality while maintaining clear separation between frontend and backend concerns.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
|           |            |                                     |