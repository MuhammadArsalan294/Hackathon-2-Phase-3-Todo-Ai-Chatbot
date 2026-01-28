from fastapi import HTTPException, status
from typing import Optional


class APIError(HTTPException):
    """Custom API error class with standard error codes"""

    def __init__(self, error_code: str, detail: str, status_code: int = 400):
        super().__init__(
            status_code=status_code,
            detail={
                "detail": detail,
                "error_code": error_code
            }
        )


class AuthenticationError(APIError):
    """Error raised when authentication fails"""

    def __init__(self, detail: str = "Authentication required"):
        super().__init__(
            error_code="AUTHENTICATION_REQUIRED",
            detail=detail,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class ResourceNotFoundError(APIError):
    """Error raised when a resource is not found"""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            error_code="RESOURCE_NOT_FOUND",
            detail=detail,
            status_code=status.HTTP_404_NOT_FOUND
        )


class ValidationError(APIError):
    """Error raised when validation fails"""

    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            error_code="VALIDATION_ERROR",
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class InternalError(APIError):
    """Error raised when an internal server error occurs"""

    def __init__(self, detail: str = "Internal server error"):
        super().__init__(
            error_code="INTERNAL_ERROR",
            detail=detail,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )