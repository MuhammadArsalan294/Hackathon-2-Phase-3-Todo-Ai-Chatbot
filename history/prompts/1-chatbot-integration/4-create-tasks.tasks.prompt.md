---
id: 4
title: Create Tasks
stage: tasks
date: 2026-02-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-chatbot-integration
branch: 1-chatbot-integration
user: user
command: sp.tasks
labels: ["tasks", "chatbot", "implementation", "planning"]
links:
  spec: specs/1-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-chatbot-integration/tasks.md
tests:
 - none
---

## Prompt

```
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
```

## Response snapshot

Generated comprehensive implementation tasks for the Todo AI Chatbot Integration feature. The tasks.md file organizes 50 tasks across 7 phases: Setup, Foundational, and 4 user stories (Natural Language Task Management, Conversational Task Operations, Persistent Conversation History, and User Information Access). The tasks follow constitutional requirements including stateless architecture, JWT-based identity, MCP-only mutations, and user isolation. Tasks are structured to enable independent implementation and testing of each user story, with foundational components blocking user story work until completion. The implementation strategy supports both MVP delivery (starting with US1) and parallel team development.

## Outcome

- ✅ Impact: Created complete task breakdown for Phase III Todo AI Chatbot implementation
- 🧪 Tests: none
- 📁 Files: Created specs/1-chatbot-integration/tasks.md with 50 detailed tasks
- 🔁 Next prompts: Begin implementation with individual tasks
- 🧠 Reflection: Tasks organized by user story to enable independent development

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Start with foundational tasks (T001-T018)