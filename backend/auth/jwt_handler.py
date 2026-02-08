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
        # Decode the token using the secret with leeway to handle clock skew
        # Temporarily disable automatic verification to handle it manually
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"],  # Better Auth typically uses HS256 for symmetric encryption
            options={"verify_signature": True, "verify_exp": False, "verify_nbf": False, "verify_iat": False},  # Manual verification
        )

        # Manually check expiration with leeway
        exp = payload.get("exp")
        if exp:
            # Add leeway to current time when comparing
            current_time_with_leeway = datetime.utcnow() - timedelta(seconds=10)
            if datetime.fromtimestamp(exp) < current_time_with_leeway:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        # Manually check not-before with leeway
        nbf = payload.get("nbf")
        if nbf:
            # Subtract leeway from current time when comparing
            current_time_with_leeway = datetime.utcnow() + timedelta(seconds=10)
            if datetime.fromtimestamp(nbf) > current_time_with_leeway:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token is not yet valid",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        # Manually check issued-at with leeway
        iat = payload.get("iat")
        if iat:
            # Subtract leeway from current time when comparing
            current_time_with_leeway = datetime.utcnow() + timedelta(seconds=10)
            if datetime.fromtimestamp(iat) > current_time_with_leeway:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token is not yet valid (iat)",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        # Check if token was issued before password change (if password_updated_at is in token)
        password_updated_at = payload.get("password_updated_at")
        if password_updated_at:
            token_issue_time = payload.get("iat", datetime.utcnow().timestamp())  # Use issued at time if available
            # Ensure both values are floats for comparison
            token_issue_time = float(token_issue_time) if token_issue_time else datetime.utcnow().timestamp()
            password_updated_at = float(password_updated_at) if password_updated_at else 0
            
            # Add a small tolerance (1 second) to account for timing differences during token creation
            if token_issue_time < (password_updated_at - 1.0):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token is invalid because password has been changed",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        return payload

    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation error: {str(e)}",
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