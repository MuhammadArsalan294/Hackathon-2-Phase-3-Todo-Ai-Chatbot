#!/usr/bin/env python3
"""
Debug script to check imports
"""

import sys
import traceback

def test_imports():
    print("Testing imports step by step...")

    try:
        print("1. Testing basic imports...")
        from fastapi import FastAPI
        print("   ✓ FastAPI imported successfully")

        from sqlmodel import Session
        print("   ✓ SQLModel imported successfully")

        print("\n2. Testing backend modules...")
        from routes import tasks
        print("   ✓ Tasks route imported successfully")

        from routes import auth
        print("   ✓ Auth route imported successfully")

        from middleware.logging import LoggingMiddleware
        print("   ✓ Logging middleware imported successfully")

        print("\n3. Testing chat components...")
        # Test the problematic import
        from backend.src.api.chat_router import router as chat_router
        print("   ✓ Chat router imported successfully")

        from backend.src.models.conversation import Conversation
        print("   ✓ Conversation model imported successfully")

        from backend.src.services.conversation_service import conversation_service
        print("   ✓ Conversation service imported successfully")

        from backend.src.services.chat_service import chat_service
        print("   ✓ Chat service imported successfully")

        print("\n4. Testing auth dependency...")
        from backend.dependencies.auth import get_current_user
        print("   ✓ Auth dependency imported successfully")

        print("\n5. Testing db dependency...")
        from backend.db import get_session
        print("   ✓ DB dependency imported successfully")

        print("\n✓ All imports successful! No import errors found.")
        return True

    except ImportError as e:
        print(f"\n✗ Import error: {e}")
        print("Full traceback:")
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        print("Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n🎉 All imports working! Backend should start successfully.")
    else:
        print("\n💥 There are import issues that need to be fixed.")