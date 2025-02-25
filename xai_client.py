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
            # Prepare the system message with task management instructions
            system_message = """
            You are a task management AI assistant. Process the user's command and return a JSON response.
            For each task, include these fields:
            - id (if existing task)
            - title (string)
            - estimated_time (string like "30 minutes" or "2 hours")
            - due_date (YYYY-MM-DD format)
            - progress (number 0-100)
            - action (optional, set to "delete" for deletion requests)

            When a user asks to delete a task, set action="delete" and include the task id.

            Example response format for task creation:
            {
                "tasks": [{
                    "title": "Buy groceries",
                    "estimated_time": "30 minutes",
                    "due_date": "2025-02-25",
                    "progress": 0
                }],
                "message": "Added task to buy groceries"
            }

            Example response for task deletion:
            {
                "tasks": [{
                    "id": 123,
                    "action": "delete"
                }],
                "message": "Deleted the task"
            }
            """

            # Create the API request
            response = self.client.chat.completions.create(
                model="grok-2-1212",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Current tasks: {json.dumps(current_tasks)}\nCommand: {command}"}
                ],
                response_format={"type": "json_object"}
            )

            # Parse and validate the response
            result = json.loads(response.choices[0].message.content)

            # For non-deletion tasks, ensure proper date formatting and defaults
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