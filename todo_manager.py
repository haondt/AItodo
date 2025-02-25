from datetime import datetime
from models import Task, db

class TodoManager:
    def get_active_tasks(self, user_id):
        """Return active tasks (not deleted and not completed) sorted by due date"""
        try:
            tasks = Task.query.filter(
                Task.user_id == user_id,
                Task.is_deleted == False,
                Task.progress < 100
            ).order_by(Task.due_date.asc()).all()
            return [self._task_to_dict(task) for task in tasks]
        except Exception as e:
            print(f"Error getting active tasks: {str(e)}")
            return []

    def get_all_tasks(self, user_id):
        """Return all tasks including completed and deleted ones"""
        try:
            tasks = Task.query.filter_by(user_id=user_id).all()
            return [self._task_to_dict(task) for task in tasks]
        except Exception:
            return []

    def add_task(self, title, estimated_time, due_date, user_id):
        """Add a new task"""
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            due_date = datetime.now().strftime('%Y-%m-%d')

        task = Task(
            title=title,
            estimated_time=estimated_time or "30 minutes",
            due_date=due_date,
            progress=0,
            user_id=user_id
        )
        db.session.add(task)
        db.session.commit()
        return self._task_to_dict(task)

    def update_task_progress(self, task_id, progress, user_id):
        """Update task progress"""
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            raise ValueError("Task not found")

        task.progress = max(0, min(100, int(progress)))
        db.session.commit()

    def delete_task(self, task_id, user_id):
        """Mark task as deleted"""
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if task:
            task.is_deleted = True
            db.session.commit()

    def update_tasks(self, tasks_data, user_id):
        """Update tasks based on AI response"""
        for task_data in tasks_data:
            # Check if this is a deletion request
            if task_data.get('action') == 'delete':
                self.delete_task(task_data.get('id'), user_id)
                continue

            # Handle task creation/update
            task_id = task_data.get('id')
            if task_id:
                task = Task.query.filter_by(id=task_id, user_id=user_id).first()
                if task:
                    task.title = task_data.get('title', task.title)
                    task.estimated_time = task_data.get('estimated_time', task.estimated_time)
                    task.due_date = task_data.get('due_date', task.due_date)
                    task.progress = min(100, max(0, int(task_data.get('progress', task.progress))))
            else:
                self.add_task(
                    task_data['title'],
                    task_data.get('estimated_time', '30 minutes'),
                    task_data.get('due_date', datetime.now().strftime('%Y-%m-%d')),
                    user_id
                )

        db.session.commit()

    def _task_to_dict(self, task):
        """Convert Task model to dictionary"""
        return {
            'id': task.id,
            'title': task.title,
            'estimated_time': task.estimated_time,
            'due_date': task.due_date,
            'progress': task.progress,
            'is_deleted': task.is_deleted
        }