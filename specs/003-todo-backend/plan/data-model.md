# Data Model: Todo Backend Implementation

**Feature**: 003-todo-backend
**Created**: 2026-01-18
**Status**: Final

## Entity Definitions

### Task Entity

#### Fields
- **id** (Integer, Primary Key, Auto-increment)
  - Purpose: Unique identifier for each task
  - Constraints: Required, Unique, Auto-generated

- **user_id** (String, Required)
  - Purpose: Links task to the authenticated user
  - Constraints: Required, Indexed for performance
  - Format: String identifier from JWT token claims

- **title** (String, Required)
  - Purpose: Brief description of the task
  - Constraints: Required, Max length 255 characters
  - Validation: Must not be empty after trimming whitespace

- **description** (Text, Optional)
  - Purpose: Detailed information about the task
  - Constraints: Optional, Unlimited length
  - Default: NULL

- **completed** (Boolean, Required)
  - Purpose: Indicates completion status of the task
  - Constraints: Required, Boolean value
  - Default: False

- **created_at** (DateTime, Required)
  - Purpose: Timestamp when task was created
  - Constraints: Required, Auto-generated on creation
  - Format: ISO 8601 datetime string

- **updated_at** (DateTime, Required)
  - Purpose: Timestamp when task was last modified
  - Constraints: Required, Auto-updated on modification
  - Format: ISO 8601 datetime string

#### Relationships
- **One User to Many Tasks**: Tasks are associated with users via user_id foreign key
- **Ownership**: Each task belongs to exactly one user who has full CRUD access

#### Indexes
- **Primary Index**: id (auto-created by primary key)
- **User Filter Index**: user_id (for efficient user-scoped queries)
- **Composite Index**: (user_id, created_at) (for sorted retrieval of user's tasks)

#### Validation Rules
- **Title Validation**: Must be provided and not empty after trimming
- **User Association**: user_id must correspond to a valid authenticated user
- **Boolean Conversion**: completed field must be a valid boolean value
- **Immutable User**: user_id cannot be changed after task creation

### User Entity (Reference Only)

#### Fields (Managed by Better Auth)
- **user_id** (String, Required)
  - Purpose: Unique identifier for the user
  - Source: Extracted from JWT token claims

- **email** (String, Optional)
  - Purpose: User's email address
  - Source: Extracted from JWT token claims

#### Relationship to Task
- **User Identity**: User identity is derived from JWT token, not stored in backend database
- **Task Ownership**: Tasks reference user via user_id from JWT claims

## State Transitions

### Task State Changes
- **Creation**: New task with completed=False (default)
- **Update**: Any field except user_id can be modified
- **Completion Toggle**: completed field can be switched between true/false
- **Deletion**: Task permanently removed from database

### Access Control States
- **Authenticated**: User has valid JWT token
- **Authorized**: User can access specific task (based on user_id match)
- **Forbidden**: User attempts to access another user's task

## Data Integrity Constraints

### Referential Integrity
- **User Reference**: All tasks must have a valid user_id (enforced by application logic)
- **No Orphaned Records**: Tasks cannot exist without associated user

### Business Logic Constraints
- **User Isolation**: Tasks can only be accessed/modified by their owner
- **Immutable Ownership**: Task ownership cannot be transferred between users
- **Required Fields**: Title and user_id must be present on creation

## Database Schema (SQLModel)

### Task Model Definition
```python
from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime
from typing import Optional

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
```

### Index Specifications
- **Single Column**: CREATE INDEX idx_task_user_id ON tasks(user_id)
- **Composite**: CREATE INDEX idx_task_user_created ON tasks(user_id, created_at DESC)

## API Data Structures

### Request Bodies
- **Create Task**: `{title: string, description?: string, completed?: boolean}`
- **Update Task**: `{title?: string, description?: string, completed?: boolean}`
- **Toggle Completion**: `{completed: boolean}`

### Response Objects
- **Task Object**: `{id: number, user_id: string, title: string, description: string, completed: boolean, created_at: string, updated_at: string}`

## Validation Rules Implementation

### Pydantic Models
```python
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip() if v else v

class TaskToggleComplete(BaseModel):
    completed: bool
```

## Performance Considerations

### Query Optimization
- **User Filtering**: All queries must filter by user_id for security and performance
- **Index Usage**: Queries should leverage the user_id index
- **Pagination**: Large result sets should be paginated

### Security Implications
- **Data Isolation**: All queries must be scoped to authenticated user
- **No Cross-User Access**: User_id in JWT determines query scope
- **Proper Validation**: All user inputs must be validated before database operations