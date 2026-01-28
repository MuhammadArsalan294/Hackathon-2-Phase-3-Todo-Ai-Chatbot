---
id: 001
title: Amend Constitution
stage: constitution
date: 2026-01-18
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: 001-frontend-todo-app
user: user
command: /sp.constitution
labels: [constitution, spec-driven-development, todo-app]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests:
  - No automated tests run for constitution update
---

## Prompt

```text
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
- No agent may perform another agent's responsibility.
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
```

## Response snapshot

Updated the constitution template with all specified principles and aligned related templates (plan, spec, tasks) to ensure consistency with the new constitution requirements.

## Outcome

- ✅ Impact: Updated constitution with 10 core principles and aligned templates
- 🧪 Tests: No automated tests run for constitution update
- 📁 Files: 4 files updated to maintain consistency
- 🔁 Next prompts: Implementation can now proceed following new constitution
- 🧠 Reflection: Constitution now serves as authoritative guide for all future development

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing features following new constitution