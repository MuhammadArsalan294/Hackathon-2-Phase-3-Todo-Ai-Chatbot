##################################################################################
CHATBOT PROMPT
##################################################################################

Ab mjhe /sp.constitution bna kar do ye yad rakhna mainey phase 2 todo full stack web application bna li hai os ky andar he phase 3 todo ai chatbot bnana hai ye chatbot icon main hona chaiye.

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

#####################################################################################################

ab /sp.specify prompt do


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


#####################################################################################################

/sp.plan prompt do

/sp.plan

Project: Phase III – Todo AI Chatbot (Integrated into Existing Phase II App)

Objective:
Implement an AI-powered chatbot inside the existing Todo web application that allows users to manage tasks using natural language, following the /sp.constitution and /sp.specify strictly.

No new standalone app is allowed.

---

High-Level Implementation Plan:

────────────────────────────────────
PHASE 1: Frontend Integration (Chat UI)
────────────────────────────────────

1. Integrate OpenAI ChatKit into the existing Next.js frontend
   - Add ChatKit provider at app root
   - Configure domain allowlist key via env variable
   - Ensure compatibility with existing auth flow

2. Add Chatbot Icon Entry Point
   - Add floating or header chatbot icon
   - Clicking icon opens chat panel / modal / drawer
   - Chat UI must not redirect or reload the page

3. Connect Chat UI to Backend
   - Send messages to POST /api/chat
   - Pass JWT automatically via existing auth middleware
   - Handle conversation_id lifecycle

---

────────────────────────────────────
PHASE 2: Backend Chat Endpoint
────────────────────────────────────

4. Create Stateless Chat API
   - Implement POST /api/chat in FastAPI
   - Extract user identity from JWT
   - Reject unauthenticated requests

5. Conversation Persistence
   - Create conversation if not provided
   - Fetch conversation + messages from database
   - Persist user and assistant messages
   - Never store state in memory

---

────────────────────────────────────
PHASE 3: AI Agent Setup
────────────────────────────────────

6. Configure OpenAI Agents SDK
   - Define agent with system instructions
   - Attach MCP tools
   - Ensure agent is deterministic and safe

7. Message Construction
   - Build agent message array using DB history
   - Append new user message
   - Pass full context to agent runner

---

────────────────────────────────────
PHASE 4: MCP Server & Tools
────────────────────────────────────

8. Implement MCP Server
   - Use Official MCP SDK
   - MCP runs inside backend
   - Tools are stateless

9. Implement MCP Tools
   - add_task
   - list_tasks
   - complete_task
   - update_task
   - delete_task

10. Tool Logic
    - Reuse Phase II task services
    - Enforce user isolation
    - Handle validation and errors

---

────────────────────────────────────
PHASE 5: Agent ↔ Tool Execution
────────────────────────────────────

11. Tool Invocation Flow
    - Agent selects correct tool
    - MCP tool executes backend logic
    - Tool response returned to agent
    - Agent generates confirmation message

12. Tool Chaining
    - Support multi-step reasoning
    - Example: find task → update → confirm

---

────────────────────────────────────
PHASE 6: Error Handling & Safety
────────────────────────────────────

13. Graceful Errors
    - Task not found
    - Invalid input
    - Unauthorized access

14. Safety Guards
    - Prevent hallucinated updates
    - Block direct DB access
    - Enforce constitution rules

---

────────────────────────────────────
PHASE 7: Testing & Validation
────────────────────────────────────

15. Test Natural Language Commands
    - Add, list, update, delete, complete tasks
    - Ambiguous task references
    - Multiple conversations

16. Stateless Validation
    - Restart server
    - Resume conversation
    - Verify no data loss

---

────────────────────────────────────
PHASE 8: Final Review
────────────────────────────────────

17. Verify No Regression
    - Phase II UI still works
    - Existing APIs unchanged

18. Documentation
    - Update README
    - Add setup steps for ChatKit domain key

---

Completion Definition:

The project is complete when:
- Chatbot works inside existing Todo app
- All task operations work via natural language
- Conversations persist correctly
- System is stateless and scalable
- No manual code changes were required

End of plan.


#####################################################################################################

Tm ny mjhe jo agent or /sp.constitution or specify or plan ka prompt dia hai es sy chatbot ban jaye ga or wo proper answer krey ga or tasks add krey ga or remove bhi krey ga or mark bhi krey ga or mere phle sy bnai hui todo app main bney ga ye.

ye bas itna he kam karon ya or kuch bhi kron. (ye jab kaha chatgpt ko os ny kaha /sp.tasks or /sp.implement prompt kro)

#####################################################################################################

/sp.tasks do 

/sp.tasks

Project: Phase III – Todo AI Chatbot (Integrated into Existing Phase II App)

Objective:
Break down the /sp.plan into concrete, executable implementation tasks that Claude Code can complete step by step, without manual coding, while strictly following /sp.constitution and /sp.specify.

---

TASK GROUP 1: Frontend – Chatbot UI Integration

1. Add OpenAI ChatKit to the existing Next.js application
   - Install and configure ChatKit
   - Read NEXT_PUBLIC_OPENAI_DOMAIN_KEY from environment
   - Wrap app with ChatKit provider

2. Implement Chatbot Icon
   - Add chatbot icon to header or as floating button
   - Icon must be visible on all authenticated pages
   - Clicking icon opens a chat panel/modal/drawer

3. Build Chat UI Container
   - Embed ChatKit UI inside the panel
   - Ensure UI does not navigate away from current page
   - Maintain clean open/close behavior

4. Connect Chat UI to Backend
   - Send messages to POST /api/chat
   - Automatically include JWT via existing auth middleware
   - Manage conversation_id returned by backend

---

TASK GROUP 2: Backend – Database Layer

5. Create Conversation Model
   - SQLModel table for conversations
   - Fields: id, user_id, created_at, updated_at

6. Create Message Model
   - SQLModel table for messages
   - Fields: id, conversation_id, user_id, role, content, created_at

7. Run database migrations
   - Ensure backward compatibility with Phase II tables

---

TASK GROUP 3: Backend – Chat API

8. Implement POST /api/chat endpoint
   - Require JWT authentication
   - Extract user identity from token
   - Reject unauthenticated requests

9. Conversation Lifecycle Logic
   - Create conversation if conversation_id not provided
   - Fetch conversation + message history from DB
   - Enforce user isolation

10. Message Persistence
    - Store user message before agent run
    - Store assistant response after agent completes

---

TASK GROUP 4: AI Agent Setup

11. Configure OpenAI Agents SDK
    - Define agent with system instructions
    - Ensure Roman Urdu + simple English tone
    - Attach MCP tools

12. Agent Runner
    - Build message array from DB history
    - Append new user message
    - Execute agent per request (no memory retained)

---

TASK GROUP 5: MCP Server & Tools

13. Implement MCP Server
    - Use Official MCP SDK
    - Run MCP inside FastAPI backend
    - Ensure stateless execution

14. Implement MCP Tool: add_task
    - Create task for authenticated user
    - Reuse Phase II task service

15. Implement MCP Tool: list_tasks
    - Filter tasks (all, pending, completed)
    - Return user-scoped tasks only

16. Implement MCP Tool: complete_task
    - Mark task as completed
    - Validate ownership

17. Implement MCP Tool: update_task
    - Update title and/or description
    - Validate ownership

18. Implement MCP Tool: delete_task
    - Delete task safely
    - Validate ownership

---

TASK GROUP 6: Agent ↔ Tool Execution Flow

19. Tool Invocation Handling
    - Pass tool results back to agent
    - Allow tool chaining when needed

20. Confirmation Responses
    - Agent confirms actions clearly
    - Friendly, conversational tone

---

TASK GROUP 7: Error Handling & Safety

21. Handle Task Not Found Errors
    - Return polite, clear messages

22. Handle Invalid Inputs
    - Ask user to clarify or rephrase

23. Enforce Security Rules
    - No direct DB access by agent
    - No user_id from request body

---

TASK GROUP 8: Testing & Validation

24. Test Natural Language Scenarios
    - Add task
    - List tasks
    - Update task
    - Complete task
    - Delete task

25. Test Multi-Conversation Support
    - Resume old conversation
    - Create new conversation

26. Test Statelessness
    - Restart server
    - Verify conversation continuity

---

TASK GROUP 9: Final Verification

27. Regression Testing
    - Ensure Phase II UI still works
    - Ensure existing APIs unchanged

28. Documentation Update
    - Update README with Chatbot setup
    - Document ChatKit domain allowlist steps

---

Completion Criteria:

- Chatbot fully integrated into existing Todo app
- All task operations work via natural language
- Conversations persist correctly
- Server remains stateless
- Phase II functionality untouched

End of tasks.

#####################################################################################################

/sp.implement do


/sp.implement

Project: Phase III – Todo AI Chatbot (Integrated into Existing Phase II Todo App)

Objective:
Automatically implement all tasks defined in /sp.tasks for Phase III Todo AI Chatbot, fully integrating it into the existing Phase II Todo Full-Stack Web Application. Implementation must follow /sp.constitution and /sp.specify strictly, using Spec-Kit conventions. No manual coding is allowed.

Implementation Instructions for Claude Code:

1. Frontend – Chatbot UI Integration

Install and configure OpenAI ChatKit in the existing Next.js app.

Read NEXT_PUBLIC_OPENAI_DOMAIN_KEY from environment variables.

Wrap the Next.js app with the ChatKit provider.

Add chatbot icon to header or as a floating button visible on all authenticated pages.

Clicking icon opens a chat panel/modal/drawer with ChatKit UI embedded.

Connect Chat UI to backend: POST /api/chat with JWT attached via existing auth middleware.

Handle conversation_id and update UI state accordingly.

2. Backend – Database Layer

Create Conversation table: id, user_id, created_at, updated_at.

Create Message table: id, conversation_id, user_id, role, content, created_at.

Run database migrations safely, ensuring backward compatibility with Phase II tables.

3. Backend – Chat API

Implement POST /api/chat endpoint:

Require JWT authentication.

Extract user identity from JWT only. Reject unauthenticated requests.

Conversation lifecycle logic:

Create conversation if conversation_id not provided.

Fetch conversation + message history from DB.

Enforce user isolation.

Message persistence:

Store user message before agent execution.

Store agent response after tool execution.

4. AI Agent Setup

Configure OpenAI Agents SDK:

Use system instructions: Roman Urdu + simple English tone.

Attach all MCP tools (add_task, list_tasks, complete_task, update_task, delete_task).

Implement Agent Runner:

Build message array from DB history + new user message.

Execute agent per request; stateless execution.

5. MCP Server & Tools

Implement MCP Server inside FastAPI backend using Official MCP SDK.

Implement the following tools for AI agent:

add_task: Create new task, reuse Phase II task service.

list_tasks: Return user-scoped tasks filtered by status.

complete_task: Mark task complete. Validate ownership.

update_task: Update task title/description. Validate ownership.

delete_task: Delete task safely. Validate ownership.

6. Agent ↔ Tool Execution Flow

Tool invocation must return results back to agent.

Support tool chaining in one agent turn if needed.

Agent confirms actions in friendly conversational tone.

7. Error Handling & Safety

Handle task-not-found errors with polite messages.

Handle invalid inputs by asking user to clarify.

Enforce security: no direct DB access by agent, never accept user_id from request body.

8. Testing & Validation

Test natural language scenarios: add, list, update, complete, delete tasks.

Test multi-conversation support: resume old conversations, create new ones.

Test stateless server behavior: restart server, verify conversation continuity.

9. Final Verification

Regression testing: ensure Phase II Todo app UI and API still work.

Update documentation: README with Chatbot setup and ChatKit domain allowlist instructions.

Completion Criteria:

Chatbot fully integrated into Phase II app.

All task operations work via natural language commands.

Conversations persist correctly in DB; server remains stateless.

Multi-user data isolation enforced.

Existing Phase II UI & functionality unaffected.

Claude Code implements all frontend, backend, AI agent, MCP tools automatically.

#####################################################################################################