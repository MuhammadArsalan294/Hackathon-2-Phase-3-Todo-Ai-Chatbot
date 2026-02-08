# Research: Todo AI Chatbot Integration

## Decision: OpenAI ChatKit Integration Approach
**Rationale**: Using OpenAI ChatKit provides a pre-built, well-designed UI component that can be easily integrated into our existing Next.js application. It handles UI complexities like message threading, loading states, and responsive design.
**Alternatives considered**: Building a custom chat interface from scratch, using other chat libraries like Stream Chat or SendBird, or using generic UI libraries like Material UI or Tailwind UI components.

## Decision: MCP Server Implementation
**Rationale**: Using the Official MCP SDK ensures proper integration with AI agents and provides a standardized way to expose backend functionality to the AI. It enforces the required architecture where all data mutations happen through tools.
**Alternatives considered**: Direct API calls from the agent, custom tool protocols, or GraphQL-based tool interfaces.

## Decision: Conversation Storage Strategy
**Rationale**: Storing conversations and messages in the database ensures persistence across server restarts and enables stateless server architecture. It aligns with the constitutional requirement for database-only storage.
**Alternatives considered**: In-memory storage (violates stateless requirement), file-based storage, or external storage services.

## Decision: JWT Token Extraction Method
**Rationale**: Extracting user identity from JWT tokens passed in the Authorization header is the most secure and standard approach that aligns with the existing Better Auth implementation.
**Alternatives considered**: Passing user_id in request body (prohibited by constitution), cookie-based extraction, or session-based identification.

## Decision: Frontend Integration Point
**Rationale**: Adding a floating chatbot icon that opens a modal/chat panel provides easy access without disrupting the existing UI flow, fulfilling the constitutional requirement that the chatbot acts as a helper, not a replacement UI.
**Alternatives considered**: Full-page chat interface, permanent sidebar, or replacing existing UI elements.

## Decision: AI Agent Configuration
**Rationale**: Using OpenAI's agent framework with specific system instructions ensures the agent behaves according to constitutional requirements (no direct DB access, proper tool usage, etc.).
**Alternatives considered**: Different AI providers, custom AI implementations, or rule-based chatbots.