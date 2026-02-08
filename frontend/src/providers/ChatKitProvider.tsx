import React, { createContext, useContext, ReactNode } from 'react';

// Define the shape of our context
interface ChatKitContextType {
  // Add any context values needed for the ChatKit functionality
  // For now, this is a placeholder as we're using a mock implementation
  isChatKitReady: boolean;
  initializeChatKit: () => void;
}

// Create the context with default values
const ChatKitContext = createContext<ChatKitContextType | undefined>(undefined);

// Props for the provider component
interface ChatKitProviderProps {
  children: ReactNode;
}

// Provider component
export const ChatKitProvider: React.FC<ChatKitProviderProps> = ({ children }) => {
  const initializeChatKit = () => {
    // In a real implementation, this would initialize the OpenAI ChatKit
    console.log('Initializing ChatKit...');
  };

  const contextValue: ChatKitContextType = {
    isChatKitReady: true, // For mock implementation, assume it's ready
    initializeChatKit
  };

  return (
    <ChatKitContext.Provider value={contextValue}>
      {children}
    </ChatKitContext.Provider>
  );
};

// Custom hook to use the ChatKit context
export const useChatKit = (): ChatKitContextType => {
  const context = useContext(ChatKitContext);
  if (context === undefined) {
    throw new Error('useChatKit must be used within a ChatKitProvider');
  }
  return context;
};