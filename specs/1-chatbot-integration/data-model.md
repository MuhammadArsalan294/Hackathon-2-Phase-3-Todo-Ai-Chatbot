# Data Model: Todo AI Chatbot Integration

## Entity: Conversation
- **id**: integer (primary key, auto-increment)
- **user_id**: string (foreign key to Better Auth user, required)
- **created_at**: timestamp (required, default: now)
- **updated_at**: timestamp (required, auto-updates)

- **Relationships**:
  - One-to-many with Message entity (one conversation has many messages)
  - Belongs to User (via user_id foreign key)

- **Validation rules**:
  - user_id must exist in Better Auth users table
  - created_at must be in the past or present
  - updated_at must be >= created_at

## Entity: Message
- **id**: integer (primary key, auto-increment)
- **conversation_id**: integer (foreign key to Conversation, required)
- **user_id**: string (foreign key to Better Auth user, required)
- **role**: string enum ("user" | "assistant", required)
- **content**: text (required)
- **created_at**: timestamp (required, default: now)

- **Relationships**:
  - Belongs to Conversation (via conversation_id foreign key)
  - Belongs to User (via user_id foreign key)

- **Validation rules**:
  - conversation_id must exist in conversations table
  - user_id must exist in Better Auth users table
  - role must be either "user" or "assistant"
  - content must not be empty

## Entity: Task (existing, extended)
- **id**: integer (primary key, auto-increment)
- **user_id**: string (foreign key to Better Auth user, required)
- **title**: string (required)
- **description**: text (optional)
- **completed**: boolean (required, default: false)
- **created_at**: timestamp (required, default: now)
- **updated_at**: timestamp (required, auto-updates)

- **Relationships**:
  - Belongs to User (via user_id foreign key)

- **Validation rules**:
  - user_id must exist in Better Auth users table
  - title must not be empty
  - created_at must be in the past or present
  - updated_at must be >= created_at

## State Transitions

### Message States
- New message is created with role and content
- Messages are immutable after creation

### Task States
- Task starts as "pending" (completed = false)
- Task transitions to "completed" when completed = true
- Task can transition back to "pending" if uncompleted
- Task is deleted entirely when removed

### Conversation States
- New conversation is created when user initiates chat
- Conversation is updated when new messages are added
- Conversation remains active indefinitely (no explicit end state)