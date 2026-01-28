# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

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
- **FR-011**: System MUST match API endpoints exactly to API specs
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

*Example of marking unclear requirements:*

- **FR-022**: System MUST [specific capability] - [NEEDS CLARIFICATION: details not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
