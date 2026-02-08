# Todo Backend with AI Chatbot Integration

A secure, production-ready FastAPI backend for the Todo application with JWT-based authentication, Neon PostgreSQL integration, and AI-powered chatbot functionality.

## Features

- JWT-based authentication using Better Auth tokens
- Secure task management with user isolation
- RESTful API endpoints
- Neon PostgreSQL database integration
- AI-powered chatbot with natural language task management
- MCP (Model Context Protocol) tools for safe data operations
- Stateless chat server architecture

## Installation

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
NEON_DATABASE_URL=your_neon_database_url
BETTER_AUTH_SECRET=your_better_auth_secret
OPENAI_API_KEY=your_openai_api_key
```

## Usage

```bash
cd backend
uvicorn main:app --reload
```

## Chatbot Setup

The AI chatbot functionality is integrated into the existing Todo application. The backend provides:

- `/api/chat` endpoint for natural language task management
- MCP (Model Context Protocol) tools for safe task operations
- Conversation and message persistence in the database
- JWT-based user authentication and isolation