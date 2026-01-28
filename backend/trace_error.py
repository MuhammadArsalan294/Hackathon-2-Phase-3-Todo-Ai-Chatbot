#!/usr/bin/env python
"""
Trace the error in the forgot password functionality
"""

import sys
import traceback
from contextlib import redirect_stderr
from io import StringIO

# Capture any import errors
stderr_capture = StringIO()
with redirect_stderr(stderr_capture):
    try:
        from services.email_service import EmailService
        print("EmailService imported successfully")
    except Exception as e:
        print(f"Error importing EmailService: {e}")
        print(f"Stderr during import: {stderr_capture.getvalue()}")

# Test the specific call that's failing
try:
    # Simulate the exact call that's failing in the API
    print("\nTesting EmailService.send_password_reset_email call...")

    # Create a mock user first
    from routes import auth
    import uuid
    from datetime import datetime

    test_email = "test@example.com"
    user_id = str(uuid.uuid4())
    auth.mock_users[test_email] = {
        "id": user_id,
        "email": test_email,
        "name": "Test User",
        "created_at": datetime.now(),
        "password": "hashed_password_here",
        "password_updated_at": datetime.now()
    }

    # Generate a reset token
    reset_token = str(uuid.uuid4())

    # This is the call that's failing
    result = EmailService.send_password_reset_email(test_email, reset_token)
    print(f"EmailService.send_password_reset_email returned: {result}")

except Exception as e:
    print(f"Error in EmailService call: {e}")
    print("Full traceback:")
    traceback.print_exc()

# Now test the forgot password function directly
import asyncio
from routes.auth import ForgotPasswordRequest

async def test_forgot_password_directly():
    request_data = ForgotPasswordRequest(email="test@example.com")

    try:
        from routes.auth import forgot_password
        result = await forgot_password(request_data)
        print(f"Direct forgot_password call result: {result}")
    except Exception as e:
        print(f"Error in direct forgot_password call: {e}")
        print("Full traceback:")
        traceback.print_exc()

print("\nTesting forgot_password function directly...")
asyncio.run(test_forgot_password_directly())