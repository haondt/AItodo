.PHONY: setup venv db-up db-down run clean help

# Default Python executable
PYTHON := python3
# Default port
PORT := 8080
# Virtual environment directory
VENV := .venv
# Requirements file
REQUIREMENTS := requirements.txt

help:
	@echo "Available commands:"
	@echo "  make setup      - Create virtual environment and install dependencies"
	@echo "  make venv       - Activate virtual environment (use 'source $(VENV)/bin/activate' instead on Unix/Mac)"
	@echo "  make db-up      - Start PostgreSQL database in Docker"
	@echo "  make db-down    - Stop PostgreSQL database"
	@echo "  make run        - Run the Flask application"
	@echo "  make clean      - Remove virtual environment and generated files"

setup: $(REQUIREMENTS)
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install pip-tools
	$(VENV)/bin/pip-compile pyproject.toml -o $(REQUIREMENTS)
	$(VENV)/bin/pip install -r $(REQUIREMENTS)
	@echo "Setup complete. Activate the virtual environment with:"
	@echo "  Windows: $(VENV)\\Scripts\\activate"
	@echo "  Unix/Mac: source $(VENV)/bin/activate"

$(REQUIREMENTS): pyproject.toml
	@if [ ! -f $(REQUIREMENTS) ]; then \
		echo "Generating $(REQUIREMENTS) from pyproject.toml"; \
		$(PYTHON) -m pip install pip-tools; \
		$(PYTHON) -m piptools compile pyproject.toml -o $(REQUIREMENTS); \
	fi

venv:
	@echo "To activate the virtual environment, use:"
	@echo "  Windows: $(VENV)\\Scripts\\activate"
	@echo "  Unix/Mac: source $(VENV)/bin/activate"
	@echo "You cannot use 'make venv' directly to activate the environment."

db-up:
	docker-compose -f docker-compose.dev.yml up -d
	@echo "PostgreSQL is running on localhost:5432"
	@echo "Connection string: postgresql://postgres:postgres@localhost:5432/todo_db"

db-down:
	docker-compose -f docker-compose.dev.yml down

run:
	@echo "Make sure your virtual environment is activated and .env file is configured"
	@echo "Starting Flask application on port $(PORT)..."
	FLASK_APP=main.py FLASK_ENV=development $(VENV)/bin/python -c "from app import app, db; from models import User, Task, Category; app.app_context().push(); db.create_all()"
	FLASK_APP=main.py FLASK_ENV=development $(VENV)/bin/flask run --host=0.0.0.0 --port=$(PORT)

clean:
	rm -rf $(VENV)
	rm -f $(REQUIREMENTS)
	@echo "Cleaned up virtual environment and generated files" 