
# Skill: Todo AI Chatbot Integration

## Overview
This skill defines how the Phase III Todo AI Chatbot is integrated into the existing Phase II Todo Full-Stack Web Application. It guides Claude Code to implement **frontend ChatKit UI**, **backend FastAPI + Agents SDK + MCP tools**, and full **task management functionality** using natural language.

The chatbot must handle:
- Task creation, listing, updating, deletion, completion
- Multi-user task isolation (via JWT)
- Conversation history persistence (stateless server)
- User information display
- Friendly confirmations and error handling

---

## Frontend Integration (ChatKit UI)

### Component Placement
- Add a chatbot icon/button visible in all layouts (app-wide layout)
- Clicking opens the ChatKit interface (modal or sidebar)
- Chat interface must:
  - Accept user natural language messages
  - Show assistant responses and confirmations
  - Display errors gracefully

### Implementation Instructions
- Use **OpenAI ChatKit** for UI
- Connect frontend to backend **POST /api/{user_id}/chat** endpoint
- Attach JWT token automatically from Better Auth session
- Store conversation_id locally (optional) for continuity
- Respect existing Tailwind styling and reusable components
- Do not modify Phase II Todo app pages outside the ChatKit modal

### Frontend Responsibilities
- Send user messages to backend chat endpoint
- Display AI responses returned from MCP tools
- Support multi-turn conversations
- Auto-scroll and handle empty/loading states

---

## Backend Integration (FastAPI + Agents SDK)

### Chat Endpoint
- **POST /api/{user_id}/chat**
- Accept:
  - conversation_id (optional, integer)
  - message (string, required)
- Return:
  - conversation_id (integer)
  - response (string)
  - tool_calls (array)
- Verify JWT from **Authorization: Bearer <token>**
- Enforce user isolation (no user_id from URL/body)
- Log messages and assistant responses in database

### MCP Tools
The following tools must be implemented and callable by AI agent:

#### add_task
- Input: user_id, title, description (optional)
- Output: task_id, status, title

#### list_tasks
- Input: user_id, status ("all", "pending", "completed")
- Output: array of task objects

#### complete_task
- Input: user_id, task_id
- Output: task_id, status, title

#### delete_task
- Input: user_id, task_id
- Output: task_id, status, title

#### update_task
- Input: user_id, task_id, title (optional), description (optional)
- Output: task_id, status, title

---

## Database Models

### tasks (existing)
- id (integer, primary key)
- user_id (string, required)
- title (string, required)
- description (text, optional)
- completed (boolean, default false)
- created_at (timestamp)
- updated_at (timestamp)

### conversations
- id (integer, primary key)
- user_id (string, required)
- created_at, updated_at (timestamps)

### messages
- id (integer, primary key)
- conversation_id (integer, required)
- user_id (string, required)
- role: "user" | "assistant"
- content: string
- created_at: timestamp

---

## Agent Behavior

- **Task Creation**: Detect phrases like "Add a task", "Remember", etc., call `add_task`
- **Task Listing**: Detect "Show me", "List", "Pending", call `list_tasks`
- **Task Completion**: Detect "Mark as complete", "Done", call `complete_task`
- **Task Deletion**: Detect "Delete", "Remove", call `delete_task`
- **Task Update**: Detect "Change", "Update", call `update_task`
- **User Info**: Respond to queries about current logged-in user using JWT
- **Confirmation**: Always confirm actions
- **Error Handling**: Handle task not found, invalid input, unauthorized access gracefully

---

## Conversation Flow

1. Receive user message from frontend
2. Fetch conversation history from database
3. Append new user message to history
4. Run agent with MCP tools
5. Store assistant response in database
6. Return response + tool_calls to frontend
7. Server remains stateless for next request

---

## Environment Variables

- `NEON_DATABASE_URL` → Neon PostgreSQL connection
- `BETTER_AUTH_SECRET` → JWT verification secret
- `BETTER_AUTH_URL` → Better Auth frontend URL
- `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` → ChatKit domain key

---

## Notes

- The chatbot **must appear as an icon** in the existing Todo app layout
- Stateless architecture ensures horizontal scalability
- MCP tools allow AI to perform CRUD without backend logic duplication
- Follow **Spec-Kit conventions** and **agentic workflow**

