import os
import json
from datetime import datetime
from openai import OpenAI

class XAIClient:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.x.ai/v1",
            api_key=os.environ.get("XAI_API_KEY")
        )

    def process_command(self, command, current_tasks):
        """Process natural language command using xAI"""
        try:
            # Prepare the system message with task management instructions.  The edited code extends the system message to include instructions for handling categories.
            system_message = """
            You are a task management AI assistant. Process the user's command and return a JSON response.
            For each task, include these fields:
            - id (if existing task)
            - title (string)
            - estimated_time (string like "30 minutes" or "2 hours")
            - due_date (YYYY-MM-DD format)
            - progress (number 0-100)
            - action (optional, set to "delete" for deletion requests)
            - category (optional, string name of the category)

            When a user asks to delete a task, set action="delete" and include the task id.
            When a user mentions a category, include it in the task data.
            If a user wants to group tasks, assign them to the same category.

            Example response format for task creation with category:
            {
                "tasks": [{
                    "title": "Buy groceries",
                    "estimated_time": "30 minutes",
                    "due_date": "2025-02-25",
                    "progress": 0,
                    "category": "Shopping"
                }],
                "message": "Added task to buy groceries in Shopping category"
            }

            Example response for task deletion:
            {
                "tasks": [{
                    "id": 123,
                    "action": "delete"
                }],
                "message": "Deleted the task"
            }

            Example response for updating task category:
            {
                "tasks": [{
                    "id": 123,
                    "category": "Work"
                }],
                "message": "Moved task to Work category"
            }
            """

            # Create the API request. This part remains unchanged.
            response = self.client.chat.completions.create(
                model="grok-2-1212",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Current tasks: {json.dumps(current_tasks)}\nCommand: {command}"}
                ],
                response_format={"type": "json_object"}
            )

            # Parse and validate the response. This part remains unchanged.
            result = json.loads(response.choices[0].message.content)

            # For non-deletion tasks, ensure proper date formatting and defaults. This part remains largely unchanged, but the code now also handles categories.
            today = datetime.now().strftime('%Y-%m-%d')
            for task in result.get('tasks', []):
                if task.get('action') != 'delete':
                    if 'due_date' not in task or not task['due_date']:
                        task['due_date'] = today
                    try:
                        datetime.strptime(task['due_date'], '%Y-%m-%d')
                    except ValueError:
                        task['due_date'] = today

                    if 'progress' not in task:
                        task['progress'] = 0
                    task['progress'] = int(task['progress'])

                    if 'estimated_time' not in task or not task['estimated_time']:
                        task['estimated_time'] = "30 minutes"

            return result

        except Exception as e:
            raise Exception(f"Error processing command with xAI: {str(e)}")