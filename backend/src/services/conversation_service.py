from typing import List, Optional
from sqlmodel import Session, select
from ..models.conversation import Conversation, ConversationRead
from ..models.message import Message


class ConversationService:
    def create_conversation(self, user_id: str, db_session: Session) -> ConversationRead:
        """Create a new conversation for the user"""
        conversation = Conversation(user_id=user_id)
        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)

        # Return a ConversationRead instance
        return ConversationRead(
            id=conversation.id,
            user_id=conversation.user_id,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )

    def get_conversation_by_id(self, conversation_id: int, user_id: str, db_session: Session) -> Optional[Conversation]:
        """Get a specific conversation by ID for the user"""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = db_session.execute(statement)
        return result.scalar_one_or_none()

    def get_user_conversations(self, user_id: str, db_session: Session) -> List[Conversation]:
        """Get all conversations for a specific user"""
        statement = select(Conversation).where(Conversation.user_id == user_id)
        result = db_session.execute(statement)
        return result.scalars().all()

    def get_conversation_with_messages(self, conversation_id: int, user_id: str, db_session: Session) -> tuple:
        """Get conversation with all associated messages"""
        conversation = self.get_conversation_by_id(conversation_id, user_id, db_session)
        if conversation:
            # Get associated messages
            message_statement = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.created_at.asc())
            result = db_session.execute(message_statement)
            messages = result.scalars().all()
            return conversation, messages
        else:
            # Return empty messages list if conversation not found
            return None, []


conversation_service = ConversationService()