from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Todo Backend API", version="1.0.0")

# CORS middleware - allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Allow all headers including Authorization
)

@app.get("/")
def read_root():
    return {"message": "Todo Backend API - Chatbot feature temporarily disabled"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Simple auth endpoint for testing
@app.post("/api/auth/signin")
def signin():
    return {"message": "Sign in successful", "token": "dummy_token_for_testing"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)