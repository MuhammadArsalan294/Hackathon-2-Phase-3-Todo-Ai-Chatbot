from __future__ import annotations
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional


class ConversationBase(SQLModel):
    user_id: str = Field(..., description="ID of the user who owns this conversation")


class Conversation(ConversationBase, table=True):
    """
    Represents a user's chat session with the AI assistant, containing metadata like creation time and user association
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp when conversation was created")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp when conversation was last updated")


class ConversationRead(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime