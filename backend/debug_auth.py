#!/usr/bin/env python
"""
Debug script to check for issues with the auth module
"""

from routes import auth

print("Import successful")

# Check if mock_users is accessible
try:
    print("mock_users:", auth.mock_users)
    print("Number of users:", len(auth.mock_users))
except Exception as e:
    print("Error accessing mock_users:", e)

# Check if password_reset_tokens is accessible
try:
    print("password_reset_tokens:", auth.password_reset_tokens)
    print("Number of tokens:", len(auth.password_reset_tokens))
except Exception as e:
    print("Error accessing password_reset_tokens:", e)

# Test the forgot password function separately
print("\nTesting forgot password function...")
try:
    from pydantic import BaseModel
    from routes.auth import ForgotPasswordRequest

    # Create a mock request object
    request_data = ForgotPasswordRequest(email="test@example.com")
    print("ForgotPasswordRequest created successfully")

    # Try to access the function
    from routes.auth import forgot_password
    print("forgot_password function accessed successfully")

except Exception as e:
    print("Error with forgot_password setup:", e)
    import traceback
    traceback.print_exc()