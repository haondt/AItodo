import os
from flask import Flask
from extensions import db, login_manager

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# configure the database
is_prod = os.environ.get('REPL_SLUG', None) is not None
if is_prod:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/todo")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/todo.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the app with the extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

with app.app_context():
    # Import models here to ensure they're registered with SQLAlchemy
    from models import User, Task
    db.create_all()