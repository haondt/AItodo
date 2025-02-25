import uuid
from datetime import datetime

class TodoManager:
    def __init__(self):
        self.tasks = {}

    def get_all_tasks(self):
        """Return all tasks sorted by due date"""
        try:
            sorted_tasks = sorted(
                self.tasks.values(),
                key=lambda x: datetime.strptime(x.get('due_date', '9999-12-31'), '%Y-%m-%d')
            )
            return sorted_tasks
        except Exception:
            # If sorting fails, return unsorted tasks
            return list(self.tasks.values())

    def add_task(self, title, estimated_time, due_date):
        """Add a new task"""
        # Validate and set default date if needed
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            due_date = datetime.now().strftime('%Y-%m-%d')

        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'title': title,
            'estimated_time': estimated_time or "30 minutes",
            'due_date': due_date,
            'progress': 0
        }
        self.tasks[task_id] = task
        return task

    def update_task_progress(self, task_id, progress):
        """Update task progress"""
        if task_id not in self.tasks:
            raise ValueError("Task not found")

        progress = max(0, min(100, int(progress)))
        self.tasks[task_id]['progress'] = progress

    def update_tasks(self, tasks):
        """Update tasks based on AI response"""
        for task in tasks:
            # Ensure required fields exist
            task['title'] = task.get('title', 'Untitled Task')
            task['estimated_time'] = task.get('estimated_time', '30 minutes')
            task['due_date'] = task.get('due_date', datetime.now().strftime('%Y-%m-%d'))
            task['progress'] = min(100, max(0, int(task.get('progress', 0))))

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