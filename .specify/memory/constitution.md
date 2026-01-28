<!-- SYNC IMPACT REPORT:
Version change: N/A (initial version) → 1.0.0
Modified principles: None (new constitution)
Added sections: All principles and sections
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->

# Phase II – Todo Full-Stack Web Application Constitution

## Core Principles

### I. Spec-First Development
No agent may implement or modify code without an explicit, approved specification. All work must originate from files inside the /specs directory. Specs are the single source of truth.

### II. Agent Responsibility Boundaries
Each agent must operate strictly within its defined role. No agent may perform another agent's responsibility. Cross-cutting changes must be coordinated through the Primary Orchestrator.

### III. No Manual Coding Rule
Humans do not write application code. All implementation is performed by agents based on specs. Any deviation must be reflected first in specs.

### IV. Authentication & Identity Rule
User authentication is handled exclusively by Better Auth on the frontend. Backend never manages passwords or sessions. User identity must always be derived from a verified JWT token. user_id must never be accepted from URL parameters or request bodies.

### V. Security First
All API endpoints require authentication unless explicitly stated otherwise. Unauthorized requests must return 401. Users can only access and modify their own data. Data isolation is mandatory at API and database levels.

### VI. API Design Rules
RESTful conventions must be followed. API endpoints must match the API specs exactly. Backend behavior must align with acceptance criteria, not assumptions.

### VII. Database Ownership Rule
The users table is owned and managed externally by Better Auth. Backend database schema must not duplicate user credentials. All task records must reference users via user_id.

### VIII. Frontend Rules
All backend communication must go through a centralized API client. JWT tokens must be securely handled and attached automatically to requests. Protected pages must not be accessible to unauthenticated users.

### IX. Monorepo Discipline
Frontend and backend live in a single monorepo. Specs, frontend, and backend must remain clearly separated. CLAUDE.md files define navigation and behavioral rules for agents.

### X. Validation & Compliance
Every feature must be validated against its acceptance criteria. Integration testing must confirm end-to-end behavior. If implementation and spec conflict, the spec must be updated first.

## Enforcement
Any violation of this constitution invalidates the implementation. Agents must stop and report if a rule conflict is detected.

## Outcome
A secure, scalable, multi-user, spec-driven full-stack Todo application that strictly follows agentic development principles.

## Governance
This constitution defines the non-negotiable rules, principles, and boundaries that all agents must follow while designing and implementing Phase II of the Todo Full-Stack Web Application using a spec-driven, agentic workflow. All agents must comply with these principles during development. Any amendments require explicit documentation and approval.

**Version**: 1.0.0 | **Ratified**: 2026-01-18 | **Last Amended**: 2026-01-18
