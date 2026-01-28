from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
import logging


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging requests, particularly authentication events
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log incoming request
        logging.info(f"Incoming request: {request.method} {request.url}")

        try:
            response = await call_next(request)
        except Exception as e:
            # Log authentication or other errors
            logging.error(f"Request failed: {request.method} {request.url} - Error: {str(e)}")
            raise

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logging.info(f"Response: {response.status_code} - Process time: {process_time:.4f}s")

        # Specifically log authentication-related events
        if hasattr(request.state, 'user_id'):
            logging.info(f"Authenticated user: {request.state.user_id}")

        if response.status_code == 401:
            logging.warning(f"Unauthorized access attempt: {request.method} {request.url}")

        response.headers["X-Process-Time"] = str(process_time)
        return response


# Initialize logger
logging.basicConfig(level=logging.INFO)