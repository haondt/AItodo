import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from todo_manager import TodoManager
from xai_client import XAIClient
from app import app, db # Assuming app and db are defined elsewhere, likely in __init__.py
from auth import auth # Assuming auth blueprint is defined elsewhere

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Register blueprints
app.register_blueprint(auth)

# Initialize managers
todo_manager = TodoManager()
xai_client = XAIClient()

@app.route('/')
@login_required
def index():
    """Render the main page"""
    return render_template('index.html', tasks=todo_manager.get_active_tasks(current_user.id))

@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    """Get all active tasks"""
    return jsonify(todo_manager.get_active_tasks(current_user.id))

@app.route('/api/tasks', methods=['POST'])
@login_required
def process_command():
    """Process natural language command using xAI"""
    try:
        command = request.json.get('command', '')
        current_tasks = todo_manager.get_all_tasks(current_user.id)

        # Process command with xAI
        response = xai_client.process_command(command, current_tasks)

        # Update tasks based on AI response
        todo_manager.update_tasks(response['tasks'], current_user.id)

        return jsonify({
            'success': True,
            'tasks': todo_manager.get_active_tasks(current_user.id),
            'message': response.get('message', 'Command processed successfully')
        })
    except Exception as e:
        logger.error(f"Error processing command: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    try:
        todo_manager.delete_task(task_id, current_user.id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/tasks/<task_id>/progress', methods=['PUT'])
@login_required
def update_progress(task_id):
    """Update task progress"""
    try:
        progress = request.json.get('progress', 0)
        todo_manager.update_task_progress(task_id, progress, current_user.id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)