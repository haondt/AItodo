import os
import logging
from flask import Flask, render_template, request, jsonify
from todo_manager import TodoManager
from xai_client import XAIClient

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Initialize managers
todo_manager = TodoManager()
xai_client = XAIClient()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', tasks=todo_manager.get_all_tasks())

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    return jsonify(todo_manager.get_all_tasks())

@app.route('/api/tasks', methods=['POST'])
def process_command():
    """Process natural language command using xAI"""
    try:
        command = request.json.get('command', '')
        current_tasks = todo_manager.get_all_tasks()
        
        # Process command with xAI
        response = xai_client.process_command(command, current_tasks)
        
        # Update tasks based on AI response
        todo_manager.update_tasks(response['tasks'])
        
        return jsonify({
            'success': True,
            'tasks': todo_manager.get_all_tasks(),
            'message': response.get('message', 'Command processed successfully')
        })
    except Exception as e:
        logger.error(f"Error processing command: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tasks/<task_id>/progress', methods=['PUT'])
def update_progress(task_id):
    """Update task progress"""
    try:
        progress = request.json.get('progress', 0)
        todo_manager.update_task_progress(task_id, progress)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
