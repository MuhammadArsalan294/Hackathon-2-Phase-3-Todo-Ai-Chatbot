import sys
import os
from pathlib import Path

# Add the backend directory to the Python path to allow imports from models
backend_dir = Path(__file__).parent.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from typing import Dict, Any, List
from sqlmodel import Session
from datetime import datetime
import json

from ..models.message import Message
from .conversation_service import conversation_service
from models.task import TaskCreate
from .sync_task_service import SyncTaskService


class ChatService:
    def __init__(self):
        # Simple service without external dependencies
        pass

    def process_message(self, conversation_id: int, user_id: str, message: str, db_session: Session) -> Dict[str, Any]:
        """
        Process a user message and return a response
        """
        # Save the user message to the database
        user_message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=message
        )
        db_session.add(user_message)
        db_session.commit()
        db_session.refresh(user_message)  # Refresh to get the ID

        # Generate response based on message content
        response_content, tool_calls = self._generate_response_with_tool_calls(message, user_id, db_session)

        # Save the assistant message to the database
        assistant_message = Message(
            conversation_id=conversation_id,
            user_id="assistant",
            role="assistant",
            content=response_content
        )
        db_session.add(assistant_message)
        db_session.commit()
        db_session.refresh(assistant_message)  # Refresh to get the ID

        return {
            "response": response_content,
            "tool_calls": tool_calls,
            "conversation_id": conversation_id
        }

    def _generate_response(self, message: str, user_id: str, db_session: Session) -> str:
        """
        Generate response based on user message
        """
        msg = message.lower().strip()

        # Task creation responses
        if any(keyword in msg for keyword in ["add task", "create task", "new task", "add a task"]):
            # Extract task title from the message
            task_title = self._extract_task_title(message)

            if task_title:
                try:
                    # Create actual task in database
                    task_data = TaskCreate(title=task_title, completed=False)
                    task_service = SyncTaskService(db_session)
                    created_task = task_service.create_task(task_data, user_id)

                    return f"Added task: {created_task.title}. You can now manage your tasks using natural language!"
                except Exception as e:
                    return f"Failed to create task: {str(e)}. Please try rephrasing your request."
            else:
                return "I couldn't understand what task you want to add. Please be more specific, like 'Add a task to buy groceries'."

        # Task listing responses
        elif any(keyword in msg for keyword in ["show tasks", "list tasks", "my tasks", "show me tasks"]):
            try:
                # Get actual tasks from database
                task_service = SyncTaskService(db_session)
                tasks = task_service.get_tasks_by_user(user_id)

                if tasks:
                    task_list = "\n".join([f"• {task.title} ({'completed' if task.completed else 'pending'})" for task in tasks])
                    return f"Here are your tasks:\n{task_list}\nYou can update or complete any task by mentioning it!"
                else:
                    return "You don't have any tasks yet. You can add tasks by saying 'Add a task to ...'"
            except Exception as e:
                return f"Could not retrieve tasks: {str(e)}. Try adding a new task instead."

        # Task completion responses
        elif any(keyword in msg for keyword in ["complete", "done", "finish", "mark done"]):
            task_num = [int(s) for s in msg.split() if s.isdigit()]
            if task_num:
                try:
                    task_service = SyncTaskService(db_session)
                    # Get all user tasks to map position to actual ID
                    all_tasks = task_service.get_tasks_by_user(user_id)

                    # Check if the requested task number is within the range of tasks
                    if 1 <= task_num[0] <= len(all_tasks):
                        # Get the actual task by position (task_num[0] is 1-indexed)
                        target_task = all_tasks[task_num[0] - 1]  # Convert to 0-indexed

                        # Update the task completion status
                        updated_task = task_service.update_task_completion(target_task.id, True, user_id)
                        return f"Great! I've marked task '{updated_task.title}' as completed. Good job!"
                    else:
                        return f"You don't have a task #{task_num[0]}. You have {len(all_tasks)} tasks. Use 'Show my tasks' to see them."
                except Exception as e:
                    return f"Could not complete task #{task_num[0]}: {str(e)}. Please check if the task exists."
            else:
                return "Which task would you like to mark as complete? Please specify the task number."

        # Update task responses
        elif any(keyword in msg for keyword in ["update", "change", "edit"]):
            task_num = [int(s) for s in msg.split() if s.isdigit()]
            if task_num:
                try:
                    task_service = SyncTaskService(db_session)
                    # Get all user tasks to map position to actual ID
                    all_tasks = task_service.get_tasks_by_user(user_id)

                    # Check if the requested task number is within the range of tasks
                    if 1 <= task_num[0] <= len(all_tasks):
                        # Get the actual task by position (task_num[0] is 1-indexed)
                        target_task = all_tasks[task_num[0] - 1]  # Convert to 0-indexed

                        # Extract potential new title or description from the message
                        # This is a simplified approach - in a real implementation, you'd want more sophisticated parsing
                        words = msg.split()
                        title_idx = -1
                        desc_idx = -1

                        # Look for keywords indicating title or description change
                        for i, word in enumerate(words):
                            if word in ["to", "as"]:
                                if i > 0 and words[i-1] in ["title", "name"]:
                                    title_idx = i + 1
                                elif i > 0 and words[i-1] in ["description", "desc"]:
                                    desc_idx = i + 1
                                elif title_idx == -1 and desc_idx == -1:
                                    # If no specific field mentioned, assume it's the title
                                    title_idx = i + 1
                                    break

                        from models.task import TaskUpdate
                        update_data = TaskUpdate()

                        # If we found a potential title update
                        if title_idx != -1 and title_idx < len(words):
                            new_title = " ".join(words[title_idx:]).strip()
                            if new_title and not new_title.startswith("task"):  # Avoid capturing "task #X"
                                update_data.title = new_title

                        if update_data.title or update_data.description:
                            updated_task = task_service.update_task(target_task.id, update_data, user_id)
                            return f"Updated task #{task_num[0]}: '{updated_task.title}'."
                        else:
                            return "I need more details to update your task. Please specify what changes to make, for example: 'Update task 1 to new title'."
                    else:
                        return f"You don't have a task #{task_num[0]}. You have {len(all_tasks)} tasks. Use 'Show my tasks' to see them."
                except Exception as e:
                    return f"Could not update task #{task_num[0]}: {str(e)}. Please check if the task exists."
            else:
                return "Which task would you like to update? Please specify the task number and details."

        # Delete task responses
        elif any(keyword in msg for keyword in ["delete", "remove"]):
            task_num = [int(s) for s in msg.split() if s.isdigit()]
            if task_num:
                try:
                    task_service = SyncTaskService(db_session)
                    # Get all user tasks to map position to actual ID
                    all_tasks = task_service.get_tasks_by_user(user_id)

                    # Check if the requested task number is within the range of tasks
                    if 1 <= task_num[0] <= len(all_tasks):
                        # Get the actual task by position (task_num[0] is 1-indexed)
                        target_task = all_tasks[task_num[0] - 1]  # Convert to 0-indexed

                        # Delete the task
                        deletion_result = task_service.delete_task(target_task.id, user_id)
                        if deletion_result:
                            return f"Successfully deleted task '{target_task.title}'. Task has been removed from your list."
                    else:
                        return f"You don't have a task #{task_num[0]}. You have {len(all_tasks)} tasks. Use 'Show my tasks' to see them."
                except Exception as e:
                    return f"Could not delete task #{task_num[0]}: {str(e)}. Please check if the task exists."
            else:
                return "Which task would you like to delete? Please specify the task number."

        # Greeting responses
        elif any(greeting in msg for greeting in ["hello", "hi", "hey", "aoa", "assalam", "hye"]):
            return "Assalam o Alaikum! I'm your Todo Assistant. You can ask me to add, list, update, delete, or complete tasks. For example: 'Add a task to buy groceries', 'Show me my tasks', 'Complete task 1', 'Delete task 2', 'Update task 3 to new title'. Just chat with me naturally!"

        # Identity queries
        elif "who am i" in msg or "my name" in msg or "my email" in msg or "logged in as" in msg:
            return f"You are logged in as user ID: {user_id}. I'm here to help you manage your tasks!"

        # Casual conversation responses
        elif any(greeting in msg for greeting in ["hello", "hi", "hey", "hye", "aoa", "assalam"]) or any(positive in msg for positive in ["how are you", "how are u", "how r u", "how do you do", "kaise ho", "kya haal hai", "fine", "good", "great", "nice", "well"]):
            if any(greeting in msg for greeting in ["hello", "hi", "hey", "hye", "aoa", "assalam"]):
                return "Hello! How can I help you today? You can ask me to manage your tasks or just chat with me."
            elif any(positive in msg for positive in ["how are you", "how are u", "how r u", "how do you do", "kaise ho", "kya haal hai"]):
                return "I'm doing great, thank you for asking! How can I assist you with your tasks today?"
            elif any(positive in msg for positive in ["fine", "good", "great", "nice", "well"]):
                return "That's wonderful to hear! Would you like to add or manage any tasks today?"

        # Default response
        else:
            return f"I understood: '{message}'. I'm your Todo Assistant. You can ask me to add, list, update, delete, or complete tasks. For example: 'Add a task to buy groceries', 'Show me my tasks', 'Complete task 1', 'Delete task 2', 'Update task 3 to new title'. Just chat with me naturally!"

    def _generate_response_with_tool_calls(self, message: str, user_id: str, db_session: Session) -> tuple[str, List[Dict[str, Any]]]:
        """
        Generate response and track any tool calls made during processing
        """
        msg = message.lower().strip()
        tool_calls = []

        # Task creation responses
        if any(keyword in msg for keyword in ["add task", "create task", "new task", "add a task"]):
            # Extract task title from the message
            task_title = self._extract_task_title(message)

            if task_title:
                try:
                    # Create actual task in database
                    task_data = TaskCreate(title=task_title, completed=False)
                    task_service = SyncTaskService(db_session)
                    created_task = task_service.create_task(task_data, user_id)

                    # Add tool call for task creation
                    tool_calls.append({
                        "name": "create_task",
                        "arguments": {
                            "title": created_task.title,
                            "id": created_task.id
                        }
                    })

                    return f"Added task: {created_task.title}. You can now manage your tasks using natural language!", tool_calls
                except Exception as e:
                    return f"Failed to create task: {str(e)}. Please try rephrasing your request.", tool_calls
            else:
                return "I couldn't understand what task you want to add. Please be more specific, like 'Add a task to buy groceries'.", tool_calls

        # Task listing responses
        elif any(keyword in msg for keyword in ["show tasks", "list tasks", "my tasks", "show me tasks"]):
            try:
                # Get actual tasks from database
                task_service = SyncTaskService(db_session)
                tasks = task_service.get_tasks_by_user(user_id)

                if tasks:
                    task_list = "\n".join([f"• {task.title} ({'completed' if task.completed else 'pending'})" for task in tasks])
                    return f"Here are your tasks:\n{task_list}\nYou can update or complete any task by mentioning it!", tool_calls
                else:
                    return "You don't have any tasks yet. You can add tasks by saying 'Add a task to ...'", tool_calls
            except Exception as e:
                return f"Could not retrieve tasks: {str(e)}. Try adding a new task instead.", tool_calls

        # Task completion responses
        elif any(keyword in msg for keyword in ["complete", "done", "finish", "mark done"]):
            task_num = [int(s) for s in msg.split() if s.isdigit()]
            if task_num:
                try:
                    task_service = SyncTaskService(db_session)
                    # Get all user tasks to map position to actual ID
                    all_tasks = task_service.get_tasks_by_user(user_id)

                    # Check if the requested task number is within the range of tasks
                    if 1 <= task_num[0] <= len(all_tasks):
                        # Get the actual task by position (task_num[0] is 1-indexed)
                        target_task = all_tasks[task_num[0] - 1]  # Convert to 0-indexed

                        # Update the task completion status
                        updated_task = task_service.update_task_completion(target_task.id, True, user_id)

                        # Add tool call for task completion
                        tool_calls.append({
                            "name": "update_task",
                            "arguments": {
                                "id": updated_task.id,
                                "completed": True,
                                "title": updated_task.title
                            }
                        })

                        return f"Great! I've marked task '{updated_task.title}' as completed. Good job!", tool_calls
                    else:
                        return f"You don't have a task #{task_num[0]}. You have {len(all_tasks)} tasks. Use 'Show my tasks' to see them.", tool_calls
                except Exception as e:
                    return f"Could not complete task #{task_num[0]}: {str(e)}. Please check if the task exists.", tool_calls
            else:
                return "Which task would you like to mark as complete? Please specify the task number.", tool_calls

        # Update task responses
        elif any(keyword in msg for keyword in ["update", "change", "edit"]):
            task_num = [int(s) for s in msg.split() if s.isdigit()]
            if task_num:
                try:
                    task_service = SyncTaskService(db_session)
                    # Get all user tasks to map position to actual ID
                    all_tasks = task_service.get_tasks_by_user(user_id)

                    # Check if the requested task number is within the range of tasks
                    if 1 <= task_num[0] <= len(all_tasks):
                        # Get the actual task by position (task_num[0] is 1-indexed)
                        target_task = all_tasks[task_num[0] - 1]  # Convert to 0-indexed

                        # Extract potential new title or description from the message
                        # This is a simplified approach - in a real implementation, you'd want more sophisticated parsing
                        words = msg.split()
                        title_idx = -1
                        desc_idx = -1

                        # Look for keywords indicating title or description change
                        for i, word in enumerate(words):
                            if word in ["to", "as"]:
                                if i > 0 and words[i-1] in ["title", "name"]:
                                    title_idx = i + 1
                                elif i > 0 and words[i-1] in ["description", "desc"]:
                                    desc_idx = i + 1
                                elif title_idx == -1 and desc_idx == -1:
                                    # If no specific field mentioned, assume it's the title
                                    title_idx = i + 1
                                    break

                        from models.task import TaskUpdate
                        update_data = TaskUpdate()

                        # If we found a potential title update
                        if title_idx != -1 and title_idx < len(words):
                            new_title = " ".join(words[title_idx:]).strip()
                            if new_title and not new_title.startswith("task"):  # Avoid capturing "task #X"
                                update_data.title = new_title

                        if update_data.title or update_data.description:
                            updated_task = task_service.update_task(target_task.id, update_data, user_id)

                            # Add tool call for task update
                            tool_calls.append({
                                "name": "update_task",
                                "arguments": {
                                    "id": updated_task.id,
                                    "title": updated_task.title,
                                    "description": updated_task.description
                                }
                            })

                            return f"Updated task #{task_num[0]}: '{updated_task.title}'.", tool_calls
                        else:
                            return "I need more details to update your task. Please specify what changes to make, for example: 'Update task 1 to new title'.", tool_calls
                    else:
                        return f"You don't have a task #{task_num[0]}. You have {len(all_tasks)} tasks. Use 'Show my tasks' to see them.", tool_calls
                except Exception as e:
                    return f"Could not update task #{task_num[0]}: {str(e)}. Please check if the task exists.", tool_calls
            else:
                return "Which task would you like to update? Please specify the task number and details.", tool_calls

        # Delete task responses
        elif any(keyword in msg for keyword in ["delete", "remove"]):
            task_num = [int(s) for s in msg.split() if s.isdigit()]
            if task_num:
                try:
                    task_service = SyncTaskService(db_session)
                    # Get all user tasks to map position to actual ID
                    all_tasks = task_service.get_tasks_by_user(user_id)

                    # Check if the requested task number is within the range of tasks
                    if 1 <= task_num[0] <= len(all_tasks):
                        # Get the actual task by position (task_num[0] is 1-indexed)
                        target_task = all_tasks[task_num[0] - 1]  # Convert to 0-indexed

                        # Delete the task
                        deletion_result = task_service.delete_task(target_task.id, user_id)
                        if deletion_result:
                            # Add tool call for task deletion
                            tool_calls.append({
                                "name": "delete_task",
                                "arguments": {
                                    "id": target_task.id,
                                    "title": target_task.title
                                }
                            })

                            return f"Successfully deleted task '{target_task.title}'. Task has been removed from your list.", tool_calls
                    else:
                        return f"You don't have a task #{task_num[0]}. You have {len(all_tasks)} tasks. Use 'Show my tasks' to see them.", tool_calls
                except Exception as e:
                    return f"Could not delete task #{task_num[0]}: {str(e)}. Please check if the task exists.", tool_calls
            else:
                return "Which task would you like to delete? Please specify the task number.", tool_calls

        # Greeting responses
        elif any(greeting in msg for greeting in ["hello", "hi", "hey", "aoa", "assalam", "hye"]):
            return "Assalam o Alaikum! I'm your Todo Assistant. You can ask me to add, list, update, delete, or complete tasks. For example: 'Add a task to buy groceries', 'Show me my tasks', 'Complete task 1', 'Delete task 2', 'Update task 3 to new title'. Just chat with me naturally!", tool_calls

        # Identity queries
        elif "who am i" in msg or "my name" in msg or "my email" in msg or "logged in as" in msg:
            return f"You are logged in as user ID: {user_id}. I'm here to help you manage your tasks!", tool_calls

        # Casual conversation responses
        elif any(greeting in msg for greeting in ["hello", "hi", "hey", "hye", "aoa", "assalam"]) or any(positive in msg for positive in ["how are you", "how are u", "how r u", "how do you do", "kaise ho", "kya haal hai", "fine", "good", "great", "nice", "well"]):
            if any(greeting in msg for greeting in ["hello", "hi", "hey", "hye", "aoa", "assalam"]):
                return "Hello! How can I help you today? You can ask me to manage your tasks or just chat with me.", tool_calls
            elif any(positive in msg for positive in ["how are you", "how are u", "how r u", "how do you do", "kaise ho", "kya haal hai"]):
                return "I'm doing great, thank you for asking! How can I assist you with your tasks today?", tool_calls
            elif any(positive in msg for positive in ["fine", "good", "great", "nice", "well"]):
                return "That's wonderful to hear! Would you like to add or manage any tasks today?", tool_calls

        # Default response
        else:
            return f"I understood: '{message}'. I'm your Todo Assistant. You can ask me to add, list, update, delete, or complete tasks. For example: 'Add a task to buy groceries', 'Show me my tasks', 'Complete task 1', 'Delete task 2', 'Update task 3 to new title'. Just chat with me naturally!", tool_calls

    def _extract_task_title(self, message: str) -> str:
        """
        Extract task title from user message
        """
        msg_original = message.strip()
        msg_lower = msg_original.lower()

        # Common patterns for adding tasks
        patterns = [
            ("add task to ", len("add task to ")),
            ("add a task to ", len("add a task to ")),
            ("add task ", len("add task ")),
            ("create task to ", len("create task to ")),
            ("create a task to ", len("create a task to ")),
            ("create task ", len("create task ")),
            ("new task to ", len("new task to ")),
            ("new task ", len("new task "))
        ]

        for pattern, pattern_len in patterns:
            if pattern in msg_lower:
                # Find the position of the pattern in the original message
                pos = msg_lower.find(pattern)
                if pos != -1:
                    # Extract everything after the pattern from the original message to preserve capitalization
                    extracted = msg_original[pos + pattern_len:].strip()
                    # Take only the first sentence or up to a reasonable length
                    if '.' in extracted:
                        extracted = extracted.split('.')[0].strip()
                    # Limit length to prevent overly long titles
                    return extracted[:255] if extracted else ""

        # If no pattern matched, try to extract something meaningful from original message
        # Remove common words that might not be part of the task
        if "add" in msg_lower or "create" in msg_lower:
            # Look for the part after common verbs in the original message
            original_parts = msg_original.split()
            lower_parts = msg_lower.split()

            if "to" in lower_parts:
                idx = lower_parts.index("to")
                if idx < len(original_parts) - 1:
                    extracted = " ".join(original_parts[idx + 1:]).strip()
                    if extracted and extracted.lower() != "the":
                        return extracted[:255]

        return ""


chat_service = ChatService()