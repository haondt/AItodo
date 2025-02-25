from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
    categories = db.relationship('Category', backref='user', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), default='#6c757d')  # Default to Bootstrap secondary color
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tasks = db.relationship('Task', backref='category', lazy=True)

class Task(db.Model):
    __tablename__ = 'tasks'  # Explicitly set table name
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    estimated_time = db.Column(db.String(50))
    due_date = db.Column(db.String(10))
    progress = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)