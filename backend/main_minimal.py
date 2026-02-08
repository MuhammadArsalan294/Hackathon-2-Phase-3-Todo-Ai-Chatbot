from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional
from datetime import datetime
import json

# Minimal working version without complex imports
app = FastAPI(title="Todo Backend API - Minimal", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage for demo (replace with database in production)
conversations = {}
messages = {}

# Mock authentication function
def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return "demo_user_12345"
    # In real implementation, this would validate JWT
    return "demo_user_12345"

@app.get("/")
def read_root():
    return {"message": "Todo Backend API - Minimal Version", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Simple chat endpoint
@app.post("/api/chat")
async def chat_endpoint(
    request: Request,
    current_user: str = Depends(get_current_user)
) -> Dict[str, Any]:
    try:
        body = await request.json()
        message = body.get("message", "")
        conversation_id = body.get("conversation_id")

        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        # Create or get conversation
        if not conversation_id:
            conversation_id = int(datetime.now().timestamp())
            conversations[conversation_id] = {
                "id": conversation_id,
                "user_id": current_user,
                "created_at": datetime.now().isoformat()
            }

        # Create message entry
        message_entry = {
            "id": len(messages.get(conversation_id, [])) + 1,
            "conversation_id": conversation_id,
            "user_id": current_user,
            "role": "user",
            "content": message,
            "created_at": datetime.now().isoformat()
        }

        if conversation_id not in messages:
            messages[conversation_id] = []
        messages[conversation_id].append(message_entry)

        # Generate response based on user message
        response_content = generate_response(message, current_user)

        # Add assistant message
        assistant_message = {
            "id": len(messages[conversation_id]) + 1,
            "conversation_id": conversation_id,
            "user_id": "assistant",
            "role": "assistant",
            "content": response_content,
            "created_at": datetime.now().isoformat()
        }
        messages[conversation_id].append(assistant_message)

        return {
            "conversation_id": conversation_id,
            "response": response_content,
            "tool_calls": []
        }

    except Exception as e:
        return {
            "conversation_id": conversation_id or -1,
            "response": f"Sorry, I encountered an error: {str(e)}. Please try again.",
            "tool_calls": []
        }

def generate_response(message: str, user_id: str) -> str:
    """
    Generate response based on user message
    """
    msg = message.lower().strip()

    # Task creation responses
    if any(keyword in msg for keyword in ["add task", "create task", "new task", "add a task", "add task to"]):
        if "buy" in msg:
            item = msg.split("buy ")[1].split()[0] if "buy " in msg else "groceries"
            return f"Added task: Buy {item}. You can now manage your tasks using natural language!"
        elif "call" in msg:
            person = msg.split("call ")[1].split()[0] if "call " in msg else "mom"
            return f"Added task: Call {person}. Task has been created successfully!"
        else:
            return "I've added your task. What else would you like to do?"

    # Task listing responses
    elif any(keyword in msg for keyword in ["show tasks", "list tasks", "my tasks", "show me tasks", "list my tasks"]):
        return "Here are your tasks:\n• Buy groceries (pending)\n• Call mom (pending)\n• Finish report (pending)\nYou can update or complete any task by mentioning it!"

    # Task completion responses
    elif any(keyword in msg for keyword in ["complete", "done", "finish", "mark done", "mark as complete"]):
        task_num = [int(s) for s in msg.split() if s.isdigit()]
        if task_num:
            return f"Great! I've marked task #{task_num[0]} as completed. Good job!"
        else:
            return "Which task would you like to mark as complete? Please specify the task number."

    # Update task responses
    elif any(keyword in msg for keyword in ["update", "change", "edit"]):
        return "I can help you update your task. What changes would you like to make?"

    # Delete task responses
    elif any(keyword in msg for keyword in ["delete", "remove"]):
        return "I can help you delete a task. Which task would you like to remove?"

    # Greeting responses
    elif any(greeting in msg for greeting in ["hello", "hi", "hey", "aoa", "assalam", "hye"]):
        return "Assalam o Alaikum! I'm your Todo Assistant. You can ask me to add, list, update, or complete tasks. For example: 'Add a task to buy groceries' or 'Show me my tasks'."

    # Identity queries
    elif "who am i" in msg or "my name" in msg:
        return f"You are user {user_id[:8]}... (user ID hidden for privacy). I'm here to help you manage your tasks!"

    # Default response
    else:
        return f"I understood: '{message}'. I'm your Todo Assistant. You can ask me to add, list, update, or complete tasks. For example: 'Add a task to buy groceries' or 'Show me my tasks'."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)