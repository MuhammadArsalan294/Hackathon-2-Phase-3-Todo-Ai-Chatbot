# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-First Development Compliance
- [ ] All work originates from files inside the /specs directory
- [ ] Specifications are the single source of truth
- [ ] No implementation without explicit, approved specification

### Agent Responsibility Boundaries Compliance
- [ ] Plan respects agent role boundaries
- [ ] Cross-cutting changes coordinated through Primary Orchestrator
- [ ] No agent performing another agent's responsibility

### No Manual Coding Rule Compliance
- [ ] Plan supports agent-based implementation
- [ ] No provisions for manual human code writing
- [ ] Deviations reflected in specs first

### Authentication & Identity Rule Compliance
- [ ] Frontend authentication handled by Better Auth
- [ ] Backend does not manage passwords or sessions
- [ ] User identity derived from verified JWT token
- [ ] user_id not accepted from URL parameters or request bodies

### Security First Compliance
- [ ] All API endpoints require authentication (unless explicitly stated)
- [ ] Unauthorized requests return 401
- [ ] User data isolation at API and database levels
- [ ] Users can only access/modify own data

### API Design Rules Compliance
- [ ] RESTful conventions followed
- [ ] API endpoints match API specs exactly
- [ ] Backend behavior aligns with acceptance criteria

### Database Ownership Rule Compliance
- [ ] Users table managed externally by Better Auth
- [ ] No duplicated user credentials in backend schema
- [ ] Task records reference users via user_id

### Frontend Rules Compliance
- [ ] Backend communication through centralized API client
- [ ] JWT tokens handled securely and attached automatically
- [ ] Protected pages inaccessible to unauthenticated users

### Monorepo Discipline Compliance
- [ ] Frontend and backend in single monorepo
- [ ] Clear separation of specs, frontend, and backend
- [ ] CLAUDE.md files define navigation and behavioral rules

### Validation & Compliance Check
- [ ] Features validated against acceptance criteria
- [ ] Integration testing confirms end-to-end behavior
- [ ] Spec updates precede implementation when conflicts arise

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
