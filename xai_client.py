import os
import json
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
            You are a task management AI assistant. Process the user's command and return a JSON response with:
            1. Updated task list
            2. A message explaining what was done
            Each task should have: id (if existing), title, estimated_time, due_date, and progress.
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
            
            if not isinstance(result.get('tasks'), list):
                raise ValueError("Invalid response format from AI")

            return result

        except Exception as e:
            raise Exception(f"Error processing command with xAI: {str(e)}")
