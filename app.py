import os
from flask import Flask
from extensions import db, login_manager

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# configure the database
database_url = os.environ.get("SQLALCHEMY_DATABASE_URI")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    # Use connection pooling for PostgreSQL
    if database_url.startswith('postgresql'):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_size": 5,
            "pool_recycle": 300,
            "pool_pre_ping": True,
        }
else:
    raise ValueError("SQLALCHEMY_DATABASE_URI environment variable is required")

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