from datetime import datetime
from models import Task, Category, db

class TodoManager:
    def get_active_tasks(self, user_id):
        """Return active tasks (not deleted and not completed) sorted by due date"""
        try:
            # Get tasks without the join first to debug
            tasks = Task.query.filter(
                Task.user_id == user_id,
                Task.is_deleted == False  # Show only non-deleted tasks
            ).order_by(Task.due_date.asc()).all()

            # Log the tasks for debugging
            print(f"Found {len(tasks)} active tasks")
            for task in tasks:
                print(f"Task: {task.title}, Due: {task.due_date}, Is_deleted: {task.is_deleted}")

            task_dicts = [self._task_to_dict(task) for task in tasks]
            print("Converted tasks to dict:", task_dicts)
            return task_dicts
        except Exception as e:
            print(f"Error getting active tasks: {str(e)}")
            db.session.rollback()
            return []

    def get_all_tasks(self, user_id):
        """Return all tasks including completed and deleted ones"""
        try:
            tasks = Task.query.filter_by(user_id=user_id).all()
            return [self._task_to_dict(task) for task in tasks]
        except Exception as e:
            print(f"Error getting all tasks: {str(e)}")
            db.session.rollback()
            return []

    def get_categories(self, user_id):
        """Get all categories for a user"""
        try:
            categories = Category.query.filter_by(user_id=user_id).all()
            return [self._category_to_dict(category) for category in categories]
        except Exception as e:
            print(f"Error getting categories: {str(e)}")
            db.session.rollback()
            return []

    def add_category(self, name, color, user_id):
        """Add a new category"""
        try:
            category = Category(name=name, color=color, user_id=user_id)
            db.session.add(category)
            db.session.commit()
            return self._category_to_dict(category)
        except Exception as e:
            print(f"Error adding category: {str(e)}")
            db.session.rollback()
            return None

    def add_task(self, title, estimated_time, due_date, user_id, category_id=None):
        """Add a new task"""
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            due_date = datetime.now().strftime('%Y-%m-%d')

        try:
            task = Task(
                title=title,
                estimated_time=estimated_time or "30 minutes",
                due_date=due_date,
                progress=0,
                user_id=user_id,
                category_id=category_id
            )
            db.session.add(task)
            db.session.commit()
            return self._task_to_dict(task)
        except Exception as e:
            print(f"Error adding task: {str(e)}")
            db.session.rollback()
            return None

    def update_task_progress(self, task_id, progress, user_id):
        """Update task progress"""
        try:
            task = Task.query.filter_by(id=task_id, user_id=user_id).first()
            if not task:
                raise ValueError("Task not found")

            task.progress = max(0, min(100, int(progress)))
            db.session.commit()
        except Exception as e:
            print(f"Error updating task progress: {str(e)}")
            db.session.rollback()
            raise

    def delete_task(self, task_id, user_id):
        """Mark task as deleted"""
        try:
            task = Task.query.filter_by(id=task_id, user_id=user_id).first()
            if task:
                task.is_deleted = True
                db.session.commit()
        except Exception as e:
            print(f"Error deleting task: {str(e)}")
            db.session.rollback()
            raise

    def update_tasks(self, tasks_data, user_id):
        """Update tasks based on AI response"""
        try:
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

                        if 'category' in task_data:
                            # Get or create category within the same transaction
                            category = Category.query.filter_by(
                                name=task_data['category'],
                                user_id=user_id
                            ).first()
                            if not category:
                                category = Category(
                                    name=task_data['category'],
                                    user_id=user_id
                                )
                                db.session.add(category)
                                db.session.flush()  # Ensure category has an ID
                            task.category_id = category.id
                else:
                    # Handle category for new task
                    category_id = None
                    if 'category' in task_data:
                        # Get or create category within the same transaction
                        category = Category.query.filter_by(
                            name=task_data['category'],
                            user_id=user_id
                        ).first()
                        if not category:
                            category = Category(
                                name=task_data['category'],
                                user_id=user_id
                            )
                            db.session.add(category)
                            db.session.flush()  # Ensure category has an ID
                        category_id = category.id

                    self.add_task(
                        task_data['title'],
                        task_data.get('estimated_time', '30 minutes'),
                        task_data.get('due_date', datetime.now().strftime('%Y-%m-%d')),
                        user_id,
                        category_id
                    )

            db.session.commit()
        except Exception as e:
            print(f"Error updating tasks: {str(e)}")
            db.session.rollback()
            raise

    def _task_to_dict(self, task):
        """Convert Task model to dictionary"""
        try:
            return {
                'id': task.id,
                'title': task.title,
                'estimated_time': task.estimated_time,
                'due_date': task.due_date,
                'progress': task.progress,
                'is_deleted': task.is_deleted,
                'category': self._category_to_dict(task.category) if task.category else None
            }
        except Exception as e:
            print(f"Error converting task to dict: {str(e)}")
            return None

    def _category_to_dict(self, category):
        """Convert Category model to dictionary"""
        if not category:
            return None
        try:
            return {
                'id': category.id,
                'name': category.name,
                'color': category.color
            }
        except Exception as e:
            print(f"Error converting category to dict: {str(e)}")
            return None