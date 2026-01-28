from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import API routes
from routes import tasks
from routes import auth
from middleware.logging import LoggingMiddleware

app = FastAPI(title="Todo Backend API", version="1.0.0")

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# CORS middleware - allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Allow all headers including Authorization
)

# Include API routes
# Note: tasks.router has its own routes, adding "/api/tasks" makes routes like "/api/tasks/"
app.include_router(tasks.router, prefix="/api/tasks")
# Note: auth.router has prefix="/auth", so with prefix="/api" it becomes "/api/auth"
app.include_router(auth.router, prefix="/api", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Todo Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}