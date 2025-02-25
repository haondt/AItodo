import uuid
from datetime import datetime

class TodoManager:
    def __init__(self):
        self.tasks = {}

    def get_all_tasks(self):
        """Return all tasks sorted by due date"""
        sorted_tasks = sorted(
            self.tasks.values(),
            key=lambda x: datetime.strptime(x['due_date'], '%Y-%m-%d')
        )
        return sorted_tasks

    def add_task(self, title, estimated_time, due_date):
        """Add a new task"""
        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'title': title,
            'estimated_time': estimated_time,
            'due_date': due_date,
            'progress': 0
        }
        self.tasks[task_id] = task
        return task

    def update_task_progress(self, task_id, progress):
        """Update task progress"""
        if task_id not in self.tasks:
            raise ValueError("Task not found")
        
        progress = max(0, min(100, progress))
        self.tasks[task_id]['progress'] = progress

    def update_tasks(self, tasks):
        """Update tasks based on AI response"""
        for task in tasks:
            if 'id' in task and task['id'] in self.tasks:
                # Update existing task
                self.tasks[task['id']].update(task)
            else:
                # Add new task
                self.add_task(
                    task['title'],
                    task['estimated_time'],
                    task['due_date']
                )
