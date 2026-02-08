from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API routes
from routes import tasks
from routes import auth
from middleware.logging import LoggingMiddleware
from src.api.chat_router import router as chat_router
from db import get_session
from dependencies.auth import get_current_user
from src.services.conversation_service import conversation_service
from src.services.chat_service import chat_service

app = FastAPI(title="Todo Backend API", version="1.0.0")

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# CORS middleware - allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Allow all headers including Authorization
)

# Include API routes
# Note: tasks.router has its own routes, adding "/api/tasks" makes routes like "/api/tasks/"
app.include_router(tasks.router, prefix="/api/tasks")
# Note: auth.router has prefix="/auth", so with prefix="/api" it becomes "/api/auth"
app.include_router(auth.router, prefix="/api", tags=["auth"])
# Include chat router
app.include_router(chat_router, prefix="/api", tags=["chat"])

# Add a specific route for /chat to make it compatible with frontend
@app.post("/chat")
async def chat_endpoint_alias(
    request: Request,
    conversation_id: Optional[int] = None,
    message: str = None,
    db_session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Alias endpoint for chat to support frontend API calls
    """
    # Extract message from request body if not provided as parameter
    if message is None:
        body = await request.json()
        message = body.get("message")
        conversation_id = body.get("conversation_id", conversation_id)

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    # Get or create conversation
    if conversation_id is None:
        conversation = conversation_service.create_conversation(current_user, db_session)
        conversation_id = conversation.id
    else:
        # Verify user owns this conversation
        conversation = conversation_service.get_conversation_by_id(conversation_id, current_user, db_session)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found or access denied")

    # Process the chat message and get response
    response_data = chat_service.process_message(
        conversation_id=conversation_id,
        user_id=current_user,
        message=message,
        db_session=db_session
    )

    return {
        "conversation_id": conversation_id,
        "response": response_data["response"],
        "tool_calls": response_data.get("tool_calls", [])
    }

@app.get("/")
def read_root():
    return {"message": "Todo Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}