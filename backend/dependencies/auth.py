from fastapi import Depends, HTTPException, status, Request
from typing import Dict, Optional
from auth.jwt_handler import verify_token_and_get_user_id


async def get_current_user(request: Request) -> str:
    """
    Get current user from JWT token in Authorization header
    Returns user_id extracted from the token
    """
    # Extract Authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Handle different Authorization header formats
    if auth_header.startswith("Bearer "):
        token = auth_header[len("Bearer "):]
    elif auth_header.startswith("bearer "):
        token = auth_header[len("bearer "):]
    else:
        # Some implementations might just send the token without "Bearer" prefix
        token = auth_header

    # Verify token and extract user_id
    try:
        user_id = verify_token_and_get_user_id(token)
        return user_id
    except HTTPException:
        # Re-raise HTTP exceptions (like 401)
        raise
    except Exception as e:
        # Handle any other token verification errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Alias for easier use in route dependencies
CurrentUser = Depends(get_current_user)