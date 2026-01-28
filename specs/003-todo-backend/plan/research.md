# Research Document: Todo Backend Implementation

**Feature**: 003-todo-backend
**Created**: 2026-01-18
**Status**: Completed

## Research Tasks Completed

### RT-001: JWT Verification Implementation

#### Decision: JWT Library Selection
- **Chosen**: PyJWT with cryptography backend
- **Rationale**: Industry standard, well-maintained, supports RS256 for Better Auth, extensive documentation
- **Alternatives considered**:
  - python-jose: Good but less actively maintained
  - authlib: More comprehensive but overkill for simple verification

#### JWT Verification Algorithm
- Use `jwt.decode()` with `algorithms=["RS256"]` for Better Auth compatibility
- Verify audience claim matches expected value
- Validate expiration time using `exp` claim
- Extract `user_id` from standard claims or custom claims depending on Better Auth configuration

### RT-002: Neon PostgreSQL Connection Pooling

#### Decision: Database Connection Management
- **Chosen**: Async SQLAlchemy session with context managers and Neon-specific settings
- **Rationale**: Compatible with Neon's serverless model, proper async handling, connection reuse
- **Alternatives considered**: Direct psycopg2 connections (synchronous), sync sessions (blocking)

#### Neon-Specific Configuration
- Use `pool_pre_ping=True` to handle connection timeouts
- Set `pool_recycle=300` (5 minutes) to prevent stale connections
- Use `pool_size=5` and `max_overflow=10` for serverless compatibility
- Enable async execution with `asyncio` support

### RT-003: FastAPI Security Patterns

#### Decision: Authentication Dependency Pattern
- **Chosen**: FastAPI dependency injection with security scheme
- **Rationale**: Clean separation of concerns, reusable across endpoints, integrates well with FastAPI's OpenAPI generation
- **Implementation**: Create dependency that extracts JWT from header, validates it, and returns user identity

#### Security Scheme Implementation
- Use `HTTPBearer` scheme for token extraction
- Implement dependency that validates token and returns current user
- Apply to all protected endpoints using FastAPI's dependency injection

### RT-004: CORS Configuration for Next.js

#### Decision: CORS Middleware Configuration
- **Chosen**: Allow specific origins with credentials support
- **Rationale**: Secure by default while enabling frontend integration
- **Configuration**: Allow credentials, specific methods, and authorization headers

#### Recommended CORS Settings
- `allow_origins`: Specific frontend URL (e.g., http://localhost:3000 for development)
- `allow_credentials`: True (to support authentication cookies if needed)
- `allow_methods`: ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
- `allow_headers`: ["Authorization", "Content-Type"]

## Technology Best Practices Resolved

### FastAPI Best Practices
- Use Pydantic models for request/response validation
- Implement dependency injection for common functionality
- Use async/await for database operations
- Leverage FastAPI's automatic OpenAPI documentation

### Security Best Practices
- Never accept user_id from URL parameters or request body
- Always validate JWT tokens before processing requests
- Implement proper error handling without leaking sensitive information
- Use parameterized queries to prevent SQL injection

### Database Best Practices
- Use async SQLAlchemy sessions for non-blocking operations
- Implement proper connection pooling for Neon compatibility
- Use SQLModel for type-safe database interactions
- Apply proper indexing for performance

## Integration Patterns

### Better Auth JWT Integration
- Expect JWT in Authorization: Bearer <token> header
- Verify token signature using BETTER_AUTH_SECRET
- Extract user information from token claims
- Map to internal user representation

### Frontend-Backend Contract
- RESTful API under /api base path
- Consistent error response format
- JSON request/response payloads
- Standard HTTP status codes

## Open Questions Resolved

### Environment Configuration
- **NEON_DATABASE_URL**: Required for database connection
- **BETTER_AUTH_SECRET**: Required for JWT verification
- **ALLOWED_ORIGINS**: For CORS configuration (comma-separated list)

### JWT Claim Mapping
- **user_id**: Expected in token claims (standard or custom)
- **exp**: Expiration time validation required
- **aud**: Audience validation (if applicable)

### Error Response Format
- Consistent JSON structure: `{"detail": "message", "error_code": "code"}`
- Standard HTTP status codes (401, 404, 422, etc.)
- User-friendly messages without exposing system details