import React, { useState } from 'react';
import ChatKitWrapper from './ChatKitWrapper';

interface ChatPanelProps {
  onClose: () => void;
}

const ChatPanel: React.FC<ChatPanelProps> = ({ onClose }) => {
  const [conversationId, setConversationId] = useState<number | null>(null);

  return (
    <div className="fixed bottom-24 right-4 sm:right-6 bg-white rounded-lg shadow-xl border border-gray-200 w-[calc(100vw-32px)] sm:w-[calc(100vw-48px)] max-w-xs sm:max-w-md md:w-96 h-[40vh] sm:h-96 md:h-96 max-h-[70vh] z-50 flex flex-col">
      {/* Header */}
      <div className="bg-blue-600 text-white p-3 rounded-t-lg flex justify-between items-center">
        <h3 className="font-semibold text-sm sm:text-base truncate">Todo Assistant</h3>
        <button
          onClick={onClose}
          className="text-white hover:text-gray-200 focus:outline-none"
          aria-label="Close chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>

      {/* Chat Content */}
      <div className="flex-grow overflow-hidden">
        <ChatKitWrapper
          conversationId={conversationId}
          onConversationIdChange={setConversationId}
        />
      </div>
    </div>
  );
};

export default ChatPanel;