/**
 * API Client for the Todo AI Chatbot
 */

// Base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

/**
 * Interface for chat message requests
 */
interface ChatMessageRequest {
  conversation_id?: number;
  message: string;
}

/**
 * Interface for chat message responses
 */
interface ChatMessageResponse {
  conversation_id: number;
  response: string;
  tool_calls: Array<{
    name: string;
    arguments: Record<string, any>;
  }>;
}

/**
 * Send a chat message to the backend
 */
export const sendChatMessage = async (
  message: string,
  conversationId?: number
): Promise<ChatMessageResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add authorization header if available
        ...(typeof window !== 'undefined' && localStorage.getItem('token')
          ? { Authorization: `Bearer ${localStorage.getItem('token')}` }
          : {}),
      },
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: ChatMessageResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

/**
 * Interface for conversation data
 */
interface Conversation {
  id: number;
  user_id: string;
  created_at: string;
  updated_at: string;
}

/**
 * Get conversation history
 */
export const getConversationHistory = async (
  conversationId: number
): Promise<Conversation> => {
  try {
    const response = await fetch(`${API_BASE_URL}/conversations/${conversationId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // Add authorization header if available
        ...(typeof window !== 'undefined' && localStorage.getItem('token')
          ? { Authorization: `Bearer ${localStorage.getItem('token')}` }
          : {}),
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: Conversation = await response.json();
    return data;
  } catch (error) {
    console.error('Error getting conversation history:', error);
    throw error;
  }
};