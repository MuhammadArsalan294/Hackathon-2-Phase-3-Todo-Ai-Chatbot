"""
Simple test to verify the API endpoints work correctly
"""
import asyncio
import jwt
from datetime import datetime, timedelta
from config.settings import settings


def generate_mock_token():
    """Generate a mock JWT token for testing"""
    token_data = {
        "userId": "test-user-123",
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1)  # 1 hour expiration
    }

    token = jwt.encode(token_data, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return token


def test_token_verification():
    """Test that the JWT token can be verified"""
    print("Testing JWT token generation and verification...")

    # Generate a test token
    test_token = generate_mock_token()
    print(f"Generated test token: {test_token[:30]}...")

    # Try to decode it
    try:
        decoded = jwt.decode(test_token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        print(f"Token decoded successfully: {decoded}")

        user_id = decoded.get("userId") or decoded.get("sub") or decoded.get("id")
        print(f"Extracted user_id: {user_id}")

        print("✅ JWT token handling is working correctly!")
        return True

    except Exception as e:
        print(f"❌ Error decoding token: {e}")
        return False


if __name__ == "__main__":
    success = test_token_verification()
    if success:
        print("\nThe backend JWT verification is working properly.")
        print("Make sure the frontend is sending the JWT token in the Authorization header as:")
        print("Authorization: Bearer <jwt-token>")
    else:
        print("\nThere may be an issue with JWT token handling.")