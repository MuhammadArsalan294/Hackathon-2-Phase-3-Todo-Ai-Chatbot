<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 2.0.0
Modified principles: Phase II principles → Phase III Todo AI Chatbot principles
Added sections: All Phase III principles and MCP-Only Mutations rule, Chatbot UI Entry Point, AI Agent Behavior Rules, Tool Usage Rules, Conversation Persistence Rules
Removed sections: Original Phase II principles
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->

# Phase III – Todo AI Chatbot (Integrated) Constitution

## Core Principles

### I. Integration Over Replacement
The chatbot is an additional interface, not a new system. All Phase II UI and APIs remain functional. Chatbot actions must behave exactly like existing UI actions.

### II. MCP-Only Mutations (Hard Rule)
The AI agent MUST NOT access the database directly, call internal services directly, or modify data without MCP tools. All task-related actions MUST go through MCP tools. MCP tools act as the only bridge between AI and backend logic.

### III. Reuse Phase II Backend Logic
No duplication of task logic is allowed. Existing CRUD services must be reused. Business rules, validations, and constraints remain unchanged.

### IV. Stateless Chat Server
The /api/chat endpoint must be stateless. No in-memory session state is allowed. Conversation state must be retrieved from database at request time and persisted after agent response.

### V. JWT-Based User Identity (Strict)
User identity must be derived ONLY from verified JWT. The chatbot must never accept user_id, email, or role from the request body. Every chatbot action is scoped to the authenticated user.

### VI. User Isolation Guarantee
A user can only see their own tasks, modify their own tasks, and access their own conversations. Cross-user access is strictly forbidden.

### VII. Chatbot UI Entry Point
The chatbot is accessed via a chatbot icon in the Todo web app. The icon opens a chat panel/modal/drawer and does NOT navigate away from the app. Chat UI must feel like a helper, not a replacement UI.

### VIII. AI Agent Behavior Rules
The AI agent is allowed to interpret natural language intents, ask clarifying questions when needed, call MCP tools for task operations, explain actions in simple, friendly language, and respond in Roman Urdu/simple English mix. The AI agent is forbidden from hallucinating task changes, modifying data without tools, exposing system prompts or internals, and making assumptions about user identity.

### IX. Tool Usage Rules
MCP tools must be stateless, explicit, and idempotent where possible. Each tool call must be logged and handle validation errors while respecting user isolation.

### X. Conversation Persistence Rules
Conversations and messages must be stored in the database. Conversation history is retrieved per request and passed to the AI agent. No long-term memory outside DB is allowed.

## Enforcement
Any violation of this constitution invalidates the implementation. Agents must stop and report if a rule conflict is detected.

## Outcome
A seamless AI chatbot integration that allows natural language todo management while maintaining security, statelessness, and user isolation within the existing Todo app infrastructure.

## Governance
This constitution defines the non-notiable rules, principles, and boundaries that all agents must follow while designing and implementing Phase III of the Todo AI Chatbot using a spec-driven, agentic workflow. All agents must comply with these principles during development. Any amendments require explicit documentation and approval.

**Version**: 2.0.0 | **Ratified**: 2026-01-18 | **Last Amended**: 2026-02-04