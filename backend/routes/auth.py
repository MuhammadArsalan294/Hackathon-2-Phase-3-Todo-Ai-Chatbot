from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime, timedelta
import jwt
from config.settings import settings
from services.email_service import EmailService
import hashlib


router = APIRouter(prefix="/auth")


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with salt"""
    # In a real application, you'd want to use bcrypt or argon2
    # For this mock implementation, we'll use SHA-256 with a salt
    salt = "todo_app_salt_2026"  # In production, use a random unique salt per user
    return hashlib.sha256((password + salt).encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash"""
    return hash_password(plain_password) == hashed_password


# Models for auth requests/responses
class SignupRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None


class SigninRequest(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str


class AuthResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[dict] = None


import json
import os
from datetime import datetime

# Define the path for the mock user storage file
MOCK_USERS_FILE = "mock_users.json"
MOCK_PASSWORD_RESET_TOKENS_FILE = "mock_password_reset_tokens.json"

def load_mock_users():
    """Load mock users from file, or return empty dict if file doesn't exist"""
    if os.path.exists(MOCK_USERS_FILE):
        try:
            with open(MOCK_USERS_FILE, 'r') as f:
                users = json.load(f)
                # Convert string dates back to datetime objects
                for email, user_data in users.items():
                    if 'created_at' in user_data:
                        user_data['created_at'] = datetime.fromisoformat(user_data['created_at'])
                    if 'password_updated_at' in user_data:
                        user_data['password_updated_at'] = datetime.fromisoformat(user_data['password_updated_at'])
                return users
        except (json.JSONDecodeError, ValueError):
            pass

    # Return empty dict if file doesn't exist or is corrupted
    return {}

def save_mock_users(users):
    """Save mock users to file"""
    # Create a copy of users with datetime objects converted to ISO format strings
    users_copy = {}
    for email, user_data in users.items():
        user_copy = user_data.copy()
        if 'created_at' in user_copy and isinstance(user_copy['created_at'], datetime):
            user_copy['created_at'] = user_copy['created_at'].isoformat()
        if 'password_updated_at' in user_copy and isinstance(user_copy['password_updated_at'], datetime):
            user_copy['password_updated_at'] = user_copy['password_updated_at'].isoformat()
        users_copy[email] = user_copy

    with open(MOCK_USERS_FILE, 'w') as f:
        json.dump(users_copy, f)

def load_password_reset_tokens():
    """Load password reset tokens from file"""
    if os.path.exists(MOCK_PASSWORD_RESET_TOKENS_FILE):
        try:
            with open(MOCK_PASSWORD_RESET_TOKENS_FILE, 'r') as f:
                tokens = json.load(f)
                # Convert string dates back to datetime objects
                for token, token_data in tokens.items():
                    if 'expires_at' in token_data:
                        token_data['expires_at'] = datetime.fromisoformat(token_data['expires_at'])
                return tokens
        except (json.JSONDecodeError, ValueError):
            pass

    return {}

def save_password_reset_tokens(tokens):
    """Save password reset tokens to file"""
    # Create a copy of tokens with datetime objects converted to ISO format strings
    tokens_copy = {}
    for token, token_data in tokens.items():
        token_copy = token_data.copy()
        if 'expires_at' in token_copy and isinstance(token_copy['expires_at'], datetime):
            token_copy['expires_at'] = token_copy['expires_at'].isoformat()
        tokens_copy[token] = token_copy

    with open(MOCK_PASSWORD_RESET_TOKENS_FILE, 'w') as f:
        json.dump(tokens_copy, f)

def cleanup_expired_tokens():
    """Remove expired password reset tokens"""
    global password_reset_tokens
    current_time = datetime.utcnow()
    expired_tokens = []

    for token, token_data in password_reset_tokens.items():
        if 'expires_at' in token_data and token_data['expires_at'] < current_time:
            expired_tokens.append(token)

    for token in expired_tokens:
        del password_reset_tokens[token]

    if expired_tokens:
        save_password_reset_tokens(password_reset_tokens)

# Initialize mock storage from files
mock_users = load_mock_users()
password_reset_tokens = load_password_reset_tokens()

# Clean up any expired tokens on startup
cleanup_expired_tokens()


@router.post("/signup", response_model=AuthResponse)
async def signup(signup_data: SignupRequest):
    """Mock signup endpoint to satisfy frontend expectations"""
    try:
        # Check if user already exists
        if signup_data.email in mock_users:
            return AuthResponse(
                success=False,
                error={"message": "User already exists"},
                data=None
            )

        # Create a mock user
        user_id = str(uuid.uuid4())
        mock_users[signup_data.email] = {
            "id": user_id,
            "email": signup_data.email,
            "name": signup_data.name,
            "created_at": datetime.utcnow(),
            "password": hash_password(signup_data.password),  # Hash the password
            "password_updated_at": datetime.utcnow()  # Track when password was last updated
        }

        # Save the updated users to file
        save_mock_users(mock_users)

        # Generate a mock JWT token (similar to what Better Auth would do)
        current_time = datetime.utcnow()
        token_data = {
            "userId": user_id,  # Better Auth typically uses userId
            "email": signup_data.email,
            "password_updated_at": mock_users[signup_data.email]["password_updated_at"].timestamp(),  # Include password update time
            "exp": current_time + timedelta(days=30),  # 30 day expiration
            "iat": int(current_time.timestamp()),  # Issued at time (as integer to avoid precision issues)
            "nbf": int(current_time.timestamp())   # Not before time (as integer to avoid precision issues)
        }

        token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm="HS256")

        # Return success response with token
        return AuthResponse(
            success=True,
            data={
                "token": token,
                "user": {
                    "id": user_id,
                    "email": signup_data.email,
                    "name": signup_data.name
                }
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        return AuthResponse(
            success=False,
            error={"message": str(e)},
            data=None
        )


@router.post("/signin", response_model=AuthResponse)
async def signin(signin_data: SigninRequest):
    """Mock signin endpoint to satisfy frontend expectations"""
    try:
        # Check if user exists
        if signin_data.email not in mock_users:
            return AuthResponse(
                success=False,
                error={"message": "Please sign up first"},
                data=None
            )

        # Verify password
        user = mock_users[signin_data.email]
        if not verify_password(signin_data.password, user['password']):
            return AuthResponse(
                success=False,
                error={"message": "Invalid credentials"},
                data=None
            )

        # Generate a JWT token
        current_time = datetime.utcnow()
        token_data = {
            "userId": user["id"],
            "email": user["email"],
            "password_updated_at": user["password_updated_at"].timestamp(),  # Include password update time
            "exp": current_time + timedelta(days=30),  # 30 day expiration
            "iat": int(current_time.timestamp()),  # Issued at time (as integer to avoid precision issues)
            "nbf": int(current_time.timestamp())   # Not before time (as integer to avoid precision issues)
        }

        token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm="HS256")

        # Return success response with token
        return AuthResponse(
            success=True,
            data={
                "token": token,
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "name": user.get("name")
                }
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        return AuthResponse(
            success=False,
            error={"message": str(e)},
            data=None
        )


@router.post("/forgot-password", response_model=AuthResponse)
async def forgot_password(request: ForgotPasswordRequest):
    """Handle forgot password request - generates reset token and sends email"""
    try:
        # Check if user exists
        if request.email not in mock_users:
            # Don't reveal if email exists or not for security reasons
            return AuthResponse(
                success=True,
                data={"message": "If an account exists for this email, a password reset link has been sent"},
                error=None
            )

        # Generate a password reset token
        reset_token = str(uuid.uuid4())
        expiry_time = datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour

        password_reset_tokens[reset_token] = {
            "email": request.email,
            "expires_at": expiry_time
        }

        # Save the updated tokens to file
        save_password_reset_tokens(password_reset_tokens)

        # Send password reset email
        email_sent = EmailService.send_password_reset_email(request.email, reset_token)

        if not email_sent:
            # Even if email fails, return success to not reveal if user exists
            return AuthResponse(
                success=True,
                data={"message": "If an account exists for this email, a password reset link has been sent"},
                error=None
            )

        return AuthResponse(
            success=True,
            data={"message": "If an account exists for this email, a password reset link has been sent"},
            error=None
        )
    except NameError as ne:
        # Specifically catch NameError which suggests a variable isn't defined
        return AuthResponse(
            success=False,
            error={"message": f"NameError: {str(ne)} - This may indicate an import or scope issue"},
            data=None
        )
    except Exception as e:
        return AuthResponse(
            success=False,
            error={"message": str(e)},
            data=None
        )


@router.post("/reset-password", response_model=AuthResponse)
async def reset_password(request: ResetPasswordRequest):
    """Reset password directly using email - validates email exists and updates password"""
    try:
        # Check if user exists
        if request.email not in mock_users:
            # For security, we shouldn't reveal if the email exists or not
            # So we'll return success even if the email doesn't exist
            # But in this case, we'll return an error as the requirement states to validate email exists
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email does not exist"
            )

        # Update the user's password with hashed version and update timestamp
        if request.email in mock_users:
            mock_users[request.email]["password"] = hash_password(request.new_password)
            mock_users[request.email]["password_updated_at"] = datetime.utcnow()

            # Save the updated users to file
            save_mock_users(mock_users)

        return AuthResponse(
            success=True,
            data={"message": "Password reset successfully"},
            error=None
        )
    except HTTPException:
        raise
    except Exception as e:
        return AuthResponse(
            success=False,
            error={"message": str(e)},
            data=None
        )


@router.post("/logout", response_model=AuthResponse)
async def logout():
    """Mock logout endpoint - clears session but does not delete user data"""
    try:
        # In a real implementation, we would invalidate the token
        # For this mock implementation, we just return success
        # The important thing is that we DON'T delete user data here
        return AuthResponse(
            success=True,
            data={"message": "Logged out successfully"},
            error=None
        )
    except Exception as e:
        return AuthResponse(
            success=False,
            error={"message": str(e)},
            data=None
        )