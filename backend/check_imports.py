#!/usr/bin/env python
"""
Script to check imports and diagnose the auth issue
"""

print("Checking imports...")

try:
    from routes.auth import mock_users, password_reset_tokens
    print("SUCCESS: Successfully imported mock_users and password_reset_tokens from routes.auth")
    print(f"mock_users: {mock_users}")
    print(f"password_reset_tokens: {password_reset_tokens}")
except Exception as e:
    print(f"ERROR: Error importing from routes.auth: {e}")

try:
    from services.email_service import EmailService
    print("SUCCESS: Successfully imported EmailService from services.email_service")
except Exception as e:
    print(f"ERROR: Error importing EmailService: {e}")

try:
    from config.settings import settings
    print("SUCCESS: Successfully imported settings")
    print(f"FRONTEND_URL: {settings.FRONTEND_URL}")
except Exception as e:
    print(f"ERROR: Error importing settings: {e}")

try:
    # Test the specific function that's failing
    import asyncio
    from routes.auth import ForgotPasswordRequest

    async def test():
        request = ForgotPasswordRequest(email="test@example.com")
        print(f"Created request: {request}")

        # Add a test user first
        from routes.auth import mock_users
        mock_users["test@example.com"] = {
            "id": "test-id",
            "email": "test@example.com",
            "name": "Test User",
            "password": "hashed",
            "created_at": __import__('datetime').datetime.now(),
            "password_updated_at": __import__('datetime').datetime.now()
        }

        from routes.auth import forgot_password
        result = await forgot_password(request)
        print(f"Forgot password result: {result}")

    print("Testing forgot_password function...")
    asyncio.run(test())
    print("SUCCESS: Forgot password function test completed")
except Exception as e:
    print(f"ERROR: Error testing forgot_password function: {e}")
    import traceback
    traceback.print_exc()