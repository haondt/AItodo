import os
import json
from datetime import datetime, timedelta
from openai import OpenAI

class XAIClient:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.x.ai/v1",
            api_key=os.environ.get("XAI_API_KEY", "default_key")
        )

    def process_command(self, command, current_tasks):
        """Process natural language command using xAI"""
        try:
            # Prepare the system message with task management instructions
            system_message = """
            You are a task management AI assistant. Process the user's command and return a JSON response.
            Always include these fields for each task:
            - id (if existing task)
            - title (string)
            - estimated_time (string like "30 minutes" or "2 hours")
            - due_date (YYYY-MM-DD format, use today's date if not specified)
            - progress (number 0-100)

            Example response format:
            {
                "tasks": [{
                    "title": "Buy groceries",
                    "estimated_time": "30 minutes",
                    "due_date": "2025-02-25",
                    "progress": 0
                }],
                "message": "Added task to buy groceries"
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

            # Ensure each task has a valid date
            today = datetime.now().strftime('%Y-%m-%d')
            for task in result.get('tasks', []):
                if 'due_date' not in task or not task['due_date'] or task['due_date'] == 'Not specified':
                    task['due_date'] = today
                try:
                    # Validate date format
                    datetime.strptime(task['due_date'], '%Y-%m-%d')
                except ValueError:
                    task['due_date'] = today

                # Ensure progress is a number
                if 'progress' not in task:
                    task['progress'] = 0
                task['progress'] = int(task['progress'])

                # Ensure estimated_time exists
                if 'estimated_time' not in task or not task['estimated_time']:
                    task['estimated_time'] = "30 minutes"

            return result

        except Exception as e:
            raise Exception(f"Error processing command with xAI: {str(e)}")