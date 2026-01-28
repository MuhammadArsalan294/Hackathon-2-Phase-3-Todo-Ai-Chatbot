# Quickstart Guide: Todo Backend Development

**Feature**: 003-todo-backend
**Created**: 2026-01-18

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Poetry or pip for dependency management
- Access to Neon PostgreSQL database
- Better Auth secret key

### Environment Variables
Create a `.env` file with the following variables:

```bash
# Database Configuration
NEON_DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname

# Authentication Configuration
BETTER_AUTH_SECRET=your_better_auth_secret_key

# Development Configuration
DEBUG=true
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install poetry
   poetry install
   ```
   OR
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (see above)

## Project Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── db.py                   # Database engine and session
├── models.py               # SQLModel models
├── dependencies/           # Auth and database dependencies
│   ├── __init__.py
│   ├── auth.py            # JWT authentication dependency
│   └── database.py        # Database session dependency
├── routes/                # API route handlers
│   ├── __init__.py
│   ├── tasks.py           # Task-related endpoints
│   └── auth.py            # Authentication endpoints (if needed)
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── jwt.py             # JWT handling utilities
│   └── security.py        # Security utilities
├── config/                # Configuration settings
│   ├── __init__.py
│   └── settings.py        # Settings management
└── requirements.txt       # Python dependencies
```

## Running the Application

### Development
```bash
# Install dependencies
poetry install

# Run the application
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or with pip:
```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Key Components

### Authentication
The backend expects JWT tokens in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

The JWT verification extracts the user_id from the token claims and uses it to filter all database queries.

### Database Models
The main entity is the Task model defined in `models.py`:
- `id`: Primary key
- `user_id`: Foreign key linking to user (extracted from JWT)
- `title`: Task title (required)
- `description`: Task description (optional)
- `completed`: Completion status (default: false)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### API Endpoints
- `GET /api/tasks` - Get all tasks for authenticated user
- `POST /api/tasks` - Create a new task for authenticated user
- `GET /api/tasks/{id}` - Get specific task (user-owned)
- `PUT /api/tasks/{id}` - Update specific task (user-owned)
- `DELETE /api/tasks/{id}` - Delete specific task (user-owned)
- `PATCH /api/tasks/{id}/complete` - Update completion status

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_tasks.py
```

### Test Structure
Tests are organized in the `tests/` directory:
- `test_auth.py` - Authentication and authorization tests
- `test_tasks.py` - Task CRUD operation tests
- `test_security.py` - Security boundary tests
- `conftest.py` - Test fixtures and configuration

## Deployment

### Environment Configuration
For production deployment, ensure these environment variables are set:
- `NEON_DATABASE_URL`: Production database connection string
- `BETTER_AUTH_SECRET`: Production authentication secret
- `DEBUG`: Set to `false` for production
- `ALLOWED_ORIGINS`: Production frontend URLs

### Database Migrations
Database schema is managed through SQLModel's create engine functionality. For production deployments:
1. Run database initialization scripts
2. Verify database connectivity
3. Test authentication flow

## Troubleshooting

### Common Issues
- **Authentication errors**: Verify BETTER_AUTH_SECRET matches the one used by Better Auth
- **Database connection**: Check NEON_DATABASE_URL format and network connectivity
- **CORS errors**: Ensure ALLOWED_ORIGINS includes your frontend URL
- **JWT validation**: Verify JWT token format and expiration

### Logs
Application logs are written to stdout in JSON format for easy parsing and monitoring.