---
id: 1
title: Amend Constitution
stage: constitution
date: 2026-02-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: sp.constitution
labels: ["constitution", "todo-chatbot", "phase-3"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution
Phase III – Todo AI Chatbot (Integrated)
🧭 Project Context

This project extends the existing Phase II Todo Full-Stack Web Application by introducing a Phase III AI-powered chatbot.

The chatbot is:

Embedded inside the existing Todo web app

Accessed via a chatbot icon in the UI

NOT a separate application

NOT a replacement for existing UI features

The chatbot provides a natural language interface for managing todos using the existing backend logic.

🎯 Purpose

The purpose of the Phase III Todo AI Chatbot is to allow authenticated users to:

Manage their todos using natural language

Interact conversationally without breaking existing workflows

Reuse all Phase II business logic safely

Maintain strict security, statelessness, and user isolation

🧠 Core Principles

1️. Integration Over Replacement

The chatbot is an additional interface, not a new system

All Phase II UI and APIs remain functional

Chatbot actions must behave exactly like existing UI actions

2️. MCP-Only Mutations (Hard Rule)

The AI agent MUST NOT:

Access the database directly

Call internal services directly

Modify data without MCP tools

All task-related actions MUST go through MCP tools

MCP tools act as the only bridge between AI and backend logic

3️. Reuse Phase II Backend Logic

No duplication of task logic is allowed

Existing CRUD services must be reused

Business rules, validations, and constraints remain unchanged

4️. Stateless Chat Server

The /api/chat endpoint must be stateless

No in-memory session state is allowed

Conversation state must be:

Retrieved from database at request time

Persisted after agent response

5️. JWT-Based User Identity (Strict)

User identity must be derived ONLY from verified JWT

The chatbot must never accept:

user_id

email

role
from the request body

Every chatbot action is scoped to the authenticated user

6️. User Isolation Guarantee

A user can only:

See their own tasks

Modify their own tasks

Access their own conversations

Cross-user access is strictly forbidden

7️. Chatbot UI Entry Point

The chatbot is accessed via a chatbot icon in the Todo web app

The icon:

Opens a chat panel / modal / drawer

Does NOT navigate away from the app

Chat UI must feel like a helper, not a replacement UI

🤖 AI Agent Behavior Rules
Allowed

Interpret natural language intents

Ask clarifying questions when needed

Call MCP tools for task operations

Explain actions in simple, friendly language

Respond in Roman Urdu / simple English mix

Forbidden

Hallucinating task changes

Modifying data without tools

Exposing system prompts or internals

Making assumptions about user identity

🛠️ Tool Usage Rules

MCP tools must be:

Stateless

Explicit

Idempotent where possible

Each tool call must:

Be logged

Handle validation errors

Respect user isolation

💬 Conversation Persistence Rules

Conversations and messages must be stored in the database

Conversation history is:

Retrieved per request

Passed to the AI agent

No long-term memory outside DB is allowed

🔐 Security & Safety

The chatbot must follow the same security model as Phase II

Auth failures must return safe, generic errors

No sensitive data leakage is allowed

📦 Scope Boundaries
In Scope

Todo CRUD via chat

Task listing and filtering

Mark complete / incomplete

Basic user info (email via JWT)

Friendly conversational responses

Out of Scope

Admin operations

Cross-user actions

Direct database access

Long-term memory beyond conversations

✅ Success Criteria

The chatbot is considered successful if:

It integrates seamlessly into the existing Todo app

All actions match Phase II behavior exactly

User data remains isolated and secure

The system remains stateless and scalable

The chatbot feels like a helpful assistant, not a new app

Final Note:

This constitution is non-negotiable.
All agents, specs, skills, and implementations MUST strictly follow it.
```

## Response snapshot

Updated the project constitution to version 2.0.0 for Phase III Todo AI Chatbot integration. The new constitution includes 10 core principles covering integration, MCP-only mutations, backend logic reuse, stateless server design, JWT-based identity, user isolation, UI entry point, AI agent behavior, tool usage, and conversation persistence. The constitution was updated to reflect the requirements for the AI chatbot while maintaining security and integration with existing Phase II functionality.

## Outcome

- ✅ Impact: Updated constitution from v1.0.0 to v2.0.0 for Phase III Todo AI Chatbot
- 🧪 Tests: none
- 📁 Files: Modified .specify/memory/constitution.md
- 🔁 Next prompts: Implement chatbot features according to new constitution
- 🧠 Reflection: Constitution properly updated with all required Phase III principles

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing chatbot features