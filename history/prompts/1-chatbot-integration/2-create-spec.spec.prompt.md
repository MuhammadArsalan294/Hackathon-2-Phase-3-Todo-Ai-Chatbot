---
id: 2
title: Create Spec
stage: spec
date: 2026-02-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-chatbot-integration
branch: 1-chatbot-integration
user: user
command: sp.specify
labels: ["spec", "chatbot", "integration", "todo"]
links:
  spec: specs/1-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-chatbot-integration/spec.md
 - specs/1-chatbot-integration/checklists/requirements.md
tests:
 - none
---

## Prompt

```
/sp.specify

Project: Phase III – Todo AI Chatbot (Integration into Existing Phase II App)

Context:
An existing Phase II Todo Full-Stack Web Application has already been implemented using:
- Next.js (App Router) frontend
- FastAPI backend
- Better Auth with JWT
- SQLModel + Neon PostgreSQL

This Phase III project must extend the existing application by embedding an AI-powered chatbot inside it.
The chatbot is accessed via a chatbot icon within the existing UI and must not break or replace any Phase II functionality.

No new standalone application is allowed.

---

Objective:
Design and implement an AI-powered Todo chatbot that allows authenticated users to manage their tasks using natural language.

The chatbot must:
- Add, update, delete, complete, and list tasks
- Answer basic user questions (e.g., logged-in email)
- Persist conversation history
- Remain fully stateless on the server
- Use MCP tools as the only way to modify data

---

Non-Negotiable Constraints:
- Follow /sp.constitution strictly
- Reuse Phase II backend business logic
- Do NOT duplicate task logic
- Do NOT store state in memory
- Do NOT accept user_id or email from request body
- User identity must be derived ONLY from JWT
- All mutations MUST go through MCP tools

---

Architecture Overview:

Frontend:
- Existing Next.js app
- Integrate OpenAI ChatKit UI
- Chatbot opens via chatbot icon (floating or header)
- Chat UI communicates with backend POST /api/chat

Backend:
- FastAPI server
- Single stateless chat endpoint
- OpenAI Agents SDK for AI reasoning
- Official MCP SDK for task tools
- SQLModel ORM
- Neon PostgreSQL for persistence

---

Chat API Specification:

Endpoint:
POST /api/chat

Authentication:
- JWT required (Better Auth)
- Extract user identity from token

Request Body:
- conversation_id (integer, optional)
- message (string, required)

Behavior:
- If conversation_id is missing, create a new conversation
- Fetch conversation + message history from database
- Append the new user message
- Run AI agent with full history and MCP tools
- Persist assistant response
- Return response to client

Response Body:
- conversation_id (integer)
- response (string)
- tool_calls (array)

---

Database Models:

Task:
- id
- user_id
- title
- description
- completed
- created_at
- updated_at

Conversation:
- id
- user_id
- created_at
- updated_at

Message:
- id
- conversation_id
- user_id
- role (user | assistant)
- content
- created_at

---

MCP Tooling Requirements:

Implement an MCP server using the Official MCP SDK that exposes the following tools.
Each tool MUST:
- Be stateless
- Derive user identity from JWT context
- Call existing Phase II task services
- Handle errors gracefully

Tools:

1. add_task
   Params: title (string, required), description (string, optional)
   Action: Create new task for authenticated user

2. list_tasks
   Params: status ("all" | "pending" | "completed", optional)
   Action: Return user's tasks filtered by status

3. complete_task
   Params: task_id (integer, required)
   Action: Mark task as completed

4. delete_task
   Params: task_id (integer, required)
   Action: Delete task

5. update_task
   Params: task_id (integer, required), title (optional), description (optional)
   Action: Update task fields

---

AI Agent Behavior:

- Interpret natural language intent
- Select correct MCP tool
- Chain tools when necessary
- Confirm actions in friendly tone
- Ask clarification if task reference is ambiguous
- Respond in Roman Urdu + simple English

---

Error Handling:

- Task not found → polite explanation
- Unauthorized access → generic auth error
- Invalid input → ask user to rephrase

---

Deliverables:

- Integrated chatbot UI triggered via icon
- Stateless FastAPI chat endpoint
- MCP server with task tools
- Persisted conversations and messages
- Fully working natural language todo management
- No regression in Phase II functionality

---

Completion Criteria:

The chatbot must:
- Manage todos correctly via natural language
- Respect user isolation
- Survive server restarts without data loss
- Scale horizontally
- Feel like a helpful assistant inside the existing app

End of specification.
```

## Response snapshot

Created a comprehensive specification for the Todo AI Chatbot Integration feature. The spec includes four prioritized user stories covering natural language task management, conversational operations, persistent conversation history, and user information access. It defines 44 functional requirements that ensure the chatbot integrates properly with the existing system while adhering to the constitutional constraints (stateless server, JWT-based identity, MCP-only mutations, etc.). The success criteria establish measurable outcomes for accuracy, response time, user success rate, data persistence, user isolation, and scalability.

## Outcome

- ✅ Impact: Created complete specification for Phase III Todo AI Chatbot Integration
- 🧪 Tests: none
- 📁 Files: Created specs/1-chatbot-integration/spec.md and specs/1-chatbot-integration/checklists/requirements.md
- 🔁 Next prompts: Proceed to planning phase with /sp.plan
- 🧠 Reflection: Spec covers all requirements from user description and aligns with constitutional principles

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin planning implementation