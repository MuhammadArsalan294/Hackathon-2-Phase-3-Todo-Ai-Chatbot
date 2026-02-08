from __future__ import annotations
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional


class MessageBase(SQLModel):
    conversation_id: int = Field(..., description="ID of the conversation this message belongs to")
    user_id: str = Field(..., description="ID of the user who sent this message")
    role: str = Field(..., description="Role of the sender ('user' or 'assistant')")
    content: str = Field(..., description="Content of the message")


class Message(MessageBase, table=True):
    """
    Represents individual exchanges between user and AI in a conversation, with role (user/assistant) and content
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp when message was created")


class MessageRead(MessageBase):
    id: int
    created_at: datetime