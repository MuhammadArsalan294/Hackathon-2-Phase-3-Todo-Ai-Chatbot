from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from db import get_session
from dependencies.auth import get_current_user
from ..models.conversation import Conversation
from ..services.conversation_service import conversation_service
from ..services.chat_service import chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat_endpoint(
    request: Request,
    conversation_id: Optional[int] = None,
    message: str = None,
    db_session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Main chat endpoint that handles user messages and returns AI responses
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