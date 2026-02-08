# Frontend Todo Application with AI Chatbot

This is a production-quality frontend for a multi-user Todo application built with Next.js, TypeScript, and Tailwind CSS, featuring an integrated AI chatbot for natural language task management.

## Features

- User authentication (sign up and sign in)
- Todo management (create, read, update, delete)
- Protected routes and session management
- Responsive design for desktop, tablet, and mobile
- Accessible UI components
- AI-powered chatbot with natural language interface
- Floating chatbot icon accessible from all pages
- Seamless integration with existing UI

## Tech Stack

- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth
- React Server Components

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the `frontend` directory
3. Install dependencies:

```bash
npm install
```

### Running the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

### Building for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── signup/
│   │   │   └── signin/
│   │   ├── dashboard/
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ui/
│   │   ├── auth/
│   │   └── todo/
│   ├── lib/
│   │   └── api/
│   └── styles/
├── public/
└── package.json
```

## API Integration

The application uses a centralized API client located at `src/lib/api/client.ts` which automatically handles JWT token attachment and error normalization.

The AI chatbot functionality uses an additional API client located at `src/lib/api-client.ts` for chat-specific operations.

## Security

- Protected routes ensure only authenticated users can access the dashboard
- 401 responses trigger automatic redirects to the sign-in page
- Session expiration is handled automatically
- Form validation prevents invalid submissions