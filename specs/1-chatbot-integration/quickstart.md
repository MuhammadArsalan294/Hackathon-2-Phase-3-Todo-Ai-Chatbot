# Quickstart Guide: Todo AI Chatbot Integration

## Prerequisites
- Node.js 18+ for frontend
- Python 3.11+ for backend
- Neon PostgreSQL database
- Better Auth configured
- OpenAI API key
- NEXT_PUBLIC_OPENAI_DOMAIN_KEY for ChatKit

## Setup Steps

### 1. Environment Variables
Add these to your `.env` file:
```bash
NEON_DATABASE_URL=your_neon_db_url
BETTER_AUTH_SECRET=your_better_auth_secret
BETTER_AUTH_URL=your_better_auth_frontend_url
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_openai_domain_key
OPENAI_API_KEY=your_openai_api_key
```

### 2. Database Migration
Run the database migration to create conversation and message tables:
```bash
# From backend directory
python -m alembic upgrade head
```

### 3. Install Dependencies
```bash
# Frontend
cd frontend
npm install

# Backend
cd backend
pip install -r requirements.txt
```

### 4. Start Services
```bash
# Terminal 1: Start backend
cd backend
uvicorn main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev
```

## Usage

### 1. Access the Chatbot
- Navigate to the Todo app
- Click the chatbot icon in the header/floating button
- The chat panel will open without navigating away

### 2. Natural Language Commands
Try these commands:
- "Add a task to buy groceries"
- "Show me my tasks"
- "Complete task 1"
- "Update task 1 to say buy milk instead of bread"
- "Delete task 2"
- "Who am I logged in as?"

### 3. Conversation Continuity
- Your conversation history persists across sessions
- Close and reopen the chat to see previous messages
- Multiple conversations are kept separate

## Architecture Overview

### Frontend Components
- `ChatBotIcon.tsx`: Floating button that opens the chat panel
- `ChatPanel.tsx`: Modal/container for the chat interface
- `ChatKitWrapper.tsx`: Wrapper for OpenAI ChatKit integration
- `ChatKitProvider.tsx`: Provider for ChatKit context

### Backend Components
- `chat_router.py`: Handles POST /api/chat requests
- `conversation_service.py`: Manages conversation lifecycle
- `chat_service.py`: Coordinates chat operations
- `mcp_server/`: MCP tools for task operations
  - `add_task_tool.py`
  - `list_tasks_tool.py`
  - `complete_task_tool.py`
  - `delete_task_tool.py`
  - `update_task_tool.py`

### Data Flow
1. User sends message via ChatKit UI
2. Frontend calls POST /api/chat with JWT
3. Backend extracts user identity from JWT
4. Conversation history retrieved from DB
5. AI agent runs with MCP tools
6. Tool operations modify tasks via existing services
7. Assistant response saved to DB
8. Response returned to frontend