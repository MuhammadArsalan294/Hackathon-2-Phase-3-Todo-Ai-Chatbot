#!/usr/bin/env python3
"""
Script to start the backend server with proper Neon database configuration
"""
import uvicorn
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("Starting backend server with Neon database connection...")
    print("Server will be available at http://localhost:8000")
    print("Database: Neon PostgreSQL (configured in .env)")

    # Run the main app from main.py
    from main import app

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)