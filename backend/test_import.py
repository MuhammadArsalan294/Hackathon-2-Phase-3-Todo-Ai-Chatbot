#!/usr/bin/env python3
"""
Test script to check imports
"""

print("Testing imports...")

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

    print("\n3. Testing middleware...")
    from middleware.logging import LoggingMiddleware
    print("   ✓ Logging middleware imported successfully")

    print("\n4. Testing chat components...")
    from backend.src.api.chat_router import router as chat_router
    print("   ✓ Chat router imported successfully")

    from backend.src.models.conversation import Conversation
    print("   ✓ Conversation model imported successfully")

    from backend.src.services.conversation_service import conversation_service
    print("   ✓ Conversation service imported successfully")

    from backend.src.services.chat_service import chat_service
    print("   ✓ Chat service imported successfully")

    print("\n✓ All imports successful! No import errors found.")

except Exception as e:
    print(f"\n✗ Import error: {e}")
    import traceback
    traceback.print_exc()