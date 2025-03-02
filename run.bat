@echo off
echo Make sure your virtual environment is activated and .env file is configured

:: Activate virtual environment if not already activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call .venv\Scripts\activate
)

:: Set environment variables
set FLASK_APP=main.py
set FLASK_ENV=development

:: Create database tables
echo Creating database tables...
python3 -c "from app import app, db; from models import User, Task, Category; app.app_context().push(); db.create_all()"

:: Run the application
echo Starting Flask application on port 8080...
flask run --host=0.0.0.0 --port=8080 