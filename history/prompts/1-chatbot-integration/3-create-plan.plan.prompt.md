---
id: 3
title: Create Plan
stage: plan
date: 2026-02-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-chatbot-integration
branch: 1-chatbot-integration
user: user
command: sp.plan
labels: ["plan", "chatbot", "integration", "architecture"]
links:
  spec: specs/1-chatbot-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-chatbot-integration/plan.md
 - specs/1-chatbot-integration/research.md
 - specs/1-chatbot-integration/data-model.md
 - specs/1-chatbot-integration/quickstart.md
 - specs/1-chatbot-integration/contracts/chat-api.yaml
 - specs/1-chatbot-integration/contracts/mcp-tools.yaml
tests:
 - none
---

## Prompt

```
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
```

## Response snapshot

Completed comprehensive planning for the Todo AI Chatbot Integration feature. Created the implementation plan document with technical context, constitution compliance checks, and project structure. Developed supporting documentation including research findings, data models for conversations/messages, quickstart guide, and API contracts for both the chat endpoint and MCP tools. All artifacts align with constitutional requirements for stateless architecture, JWT-based authentication, MCP-only mutations, and user isolation.

## Outcome

- ✅ Impact: Created complete implementation plan for Phase III Todo AI Chatbot
- 🧪 Tests: none
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and API contracts
- 🔁 Next prompts: Proceed to task generation with /sp.tasks
- 🧠 Reflection: Plan comprehensively addresses all constitutional requirements and technical constraints

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate implementation tasks