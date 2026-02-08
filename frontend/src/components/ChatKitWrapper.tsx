import React, { useEffect, useState, useRef, useCallback } from 'react';
import { sendChatMessage } from '../lib/api-client';
import { useTaskUpdate } from '@/contexts/TaskUpdateContext';

interface ChatKitWrapperProps {
  conversationId: number | null;
  onConversationIdChange: (id: number) => void;
}

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
}

const ChatKitWrapper: React.FC<ChatKitWrapperProps> = ({ conversationId, onConversationIdChange }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { triggerTaskUpdate } = useTaskUpdate();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, []);

  // Load conversation history if conversationId is provided
  useEffect(() => {
    if (conversationId) {
      // In a real implementation, we would load the conversation history from the API
      // For now, we'll just keep the current messages
    }
  }, [conversationId]);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the list immediately
    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: inputValue
    };

    setMessages(prev => [...prev, userMessage]);
    const tempInputValue = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await sendChatMessage(tempInputValue, conversationId || undefined);

      // Add assistant response to messages
      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Update conversation ID if it was returned and we didn't have one
      if (response.conversation_id && !conversationId) {
        onConversationIdChange(response.conversation_id);
      }

      // Check if the response contains task-related operations and trigger update
      if (response.tool_calls && response.tool_calls.length > 0) {
        const hasTaskOperation = response.tool_calls.some(toolCall =>
          toolCall.name.includes('task') ||
          ['create_task', 'update_task', 'delete_task', 'complete_task'].includes(toolCall.name)
        );

        if (hasTaskOperation) {
          triggerTaskUpdate();
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the conversation
      const errorMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.'
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div ref={chatContainerRef} className="flex-grow overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`p-3 rounded-lg max-w-[90%] sm:max-w-[80%] break-words ${
              message.role === 'user'
                ? 'bg-blue-100 ml-auto'
                : 'bg-gray-100 mr-auto'
            }`}
          >
            <div className="font-medium text-xs sm:text-sm mb-1">
              {message.role === 'user' ? 'You' : 'Assistant'}
            </div>
            <div className="text-gray-800 whitespace-pre-wrap text-xs sm:text-sm">{message.content}</div>
          </div>
        ))}

        {isLoading && (
          <div className="p-3 rounded-lg max-w-[90%] sm:max-w-[80%] bg-gray-100 mr-auto">
            <div className="font-medium text-xs sm:text-sm mb-1">Assistant</div>
            <div className="text-gray-800 text-xs sm:text-sm">Thinking...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-3 sm:p-4 border-t border-gray-200">
        <div className="flex flex-col sm:flex-row gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-grow border border-gray-300 rounded-lg px-3 py-2 sm:px-4 sm:py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed min-h-[40px] text-sm"
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !inputValue.trim()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-blue-400 disabled:cursor-not-allowed min-h-[40px] sm:ml-0 text-sm"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatKitWrapper;