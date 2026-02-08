#!/usr/bin/env python3
"""
Test script to verify backend functionality
"""
import asyncio
import httpx
from main import app
from fastapi.testclient import TestClient

def test_backend_sync():
    """Test backend using TestClient"""
    print("Testing backend with TestClient...")

    try:
        client = TestClient(app)

        # Test root endpoint
        response = client.get("/")
        print(f"Root endpoint status: {response.status_code}")
        print(f"Root endpoint response: {response.json()}")

        # Test health endpoint
        response = client.get("/health")
        print(f"Health endpoint status: {response.status_code}")
        print(f"Health endpoint response: {response.json()}")

        print("✅ Backend is working correctly!")
        return True

    except Exception as e:
        print(f"❌ Error testing backend: {str(e)}")
        return False

async def test_backend_async():
    """Test backend using httpx async client"""
    print("\nTesting backend with async client...")

    try:
        async with httpx.AsyncClient(app=app, base_url="http://testserver") as client:
            # Test root endpoint
            response = await client.get("/")
            print(f"Async root endpoint status: {response.status_code}")
            print(f"Async root endpoint response: {response.json()}")

            # Test health endpoint
            response = await client.get("/health")
            print(f"Async health endpoint status: {response.status_code}")
            print(f"Async health endpoint response: {response.json()}")

            print("✅ Async backend is working correctly!")
            return True

    except Exception as e:
        print(f"❌ Error testing async backend: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing backend functionality...\n")

    # Test sync
    sync_result = test_backend_sync()

    # Test async
    async_result = asyncio.run(test_backend_async())

    if sync_result and async_result:
        print("\n🎉 All backend tests passed! Backend is functioning correctly.")
    else:
        print("\n⚠️  Some tests failed.")