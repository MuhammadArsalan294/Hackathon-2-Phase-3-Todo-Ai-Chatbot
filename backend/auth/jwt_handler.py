import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from config.settings import settings


def decode_token(token: str) -> dict:
    """
    Decode and verify JWT token from Better Auth
    """
    try:
        # Decode the token using the secret
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]  # Better Auth typically uses HS256 for symmetric encryption
        )

        # Check if token is expired
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Check if token was issued before password change (if password_updated_at is in token)
        password_updated_at = payload.get("password_updated_at")
        if password_updated_at:
            token_issue_time = payload.get("iat", datetime.utcnow().timestamp())  # Use issued at time if available
            if token_issue_time < password_updated_at:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token is invalid because password has been changed",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_token_and_get_user_id(token: str) -> str:
    """
    Verify JWT token and extract user_id
    Better Auth typically stores user ID in 'userId', 'sub', 'id', or 'user_id' claim
    """
    payload = decode_token(token)

    # Extract user_id from token - Better Auth uses various claim names
    user_id = (
        payload.get("userId") or
        payload.get("user_id") or
        payload.get("sub") or
        payload.get("id") or
        payload.get("email")  # fallback to email if no user_id found
    )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: user_id not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return str(user_id)