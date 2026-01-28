from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_forgot_password_flow():
    """
    Test the complete forgot password flow:
    1. Register a user
    2. Request password reset
    3. Reset password with token
    4. Verify can sign in with new password
    """

    # First, register a test user
    signup_response = client.post("/api/auth/signup", json={
        "email": "testuser@example.com",
        "password": "SecurePass123!",
        "name": "Test User"
    })

    assert signup_response.status_code == 200
    signup_data = signup_response.json()
    assert signup_data["success"] is True

    # Test forgot password request
    forgot_response = client.post("/api/auth/forgot-password", json={
        "email": "testuser@example.com"
    })

    assert forgot_response.status_code == 200
    forgot_data = forgot_response.json()
    assert forgot_data["success"] is True

    # Since we're using mock tokens in the current implementation,
    # we'll simulate getting a token from the mock storage
    # In a real scenario, this would come from the email
    from routes.auth import password_reset_tokens
    reset_token = list(password_reset_tokens.keys())[0]  # Get the first token

    # Reset the password using the token
    reset_response = client.post("/api/auth/reset-password", json={
        "token": reset_token,
        "new_password": "NewSecurePass456!"
    })

    assert reset_response.status_code == 200
    reset_data = reset_response.json()
    assert reset_data["success"] is True

    # Verify the user can now sign in with the new password
    signin_response = client.post("/api/auth/signin", json={
        "email": "testuser@example.com",
        "password": "NewSecurePass456!"
    })

    assert signin_response.status_code == 200
    signin_data = signin_response.json()
    assert signin_data["success"] is True
    assert "token" in signin_data["data"]

    print("✅ Forgot password flow test passed!")

if __name__ == "__main__":
    test_forgot_password_flow()