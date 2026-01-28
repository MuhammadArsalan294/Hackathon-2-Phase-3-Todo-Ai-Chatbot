#!/usr/bin/env python
"""
Debug script to test the forgot password functionality specifically
"""

import asyncio
from routes.auth import ForgotPasswordRequest, forgot_password, mock_users
import uuid
from datetime import datetime, timedelta

# Add a test user to mock_users
test_email = "test@example.com"
user_id = str(uuid.uuid4())
mock_users[test_email] = {
    "id": user_id,
    "email": test_email,
    "name": "Test User",
    "created_at": datetime.utcnow(),
    "password": "hashed_password_here",  # Would normally be hashed
    "password_updated_at": datetime.utcnow()
}

print("Added test user:", test_email)
print("Current mock_users:", mock_users)

# Create a request object
request_data = ForgotPasswordRequest(email=test_email)
print("Created request:", request_data)

# Call the forgot_password function
async def test_forgot_password():
    try:
        result = await forgot_password(request_data)
        print("Result:", result)
        return result
    except Exception as e:
        print("Error calling forgot_password:", e)
        import traceback
        traceback.print_exc()
        return None

# Run the async function
result = asyncio.run(test_forgot_password())

# Check if password reset tokens were created
from routes.auth import password_reset_tokens
print("Password reset tokens after call:", password_reset_tokens)