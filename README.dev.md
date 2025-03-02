# Development Setup for AI-Powered Todo List Manager

This document provides instructions for setting up a development environment for the AI-powered Todo List Manager. This setup uses Docker for PostgreSQL and a local Python virtual environment for the application.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.11 or higher
- Make (optional, but recommended)
- X.AI API Key (for AI task processing)

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create environment file

Copy the example development environment file and update it with your actual values:

```bash
cp .env.dev .env
```

Edit the `.env` file and add your X.AI API key.

### 3. Set up the development environment

Using Make (recommended):

```bash
make setup
```

This will:
- Create a Python virtual environment in `.venv`
- Generate requirements.txt from pyproject.toml
- Install all dependencies

Without Make:

```bash
python -m venv .venv
.venv/bin/pip install pip-tools
.venv/bin/pip-compile pyproject.toml -o requirements.txt
.venv/bin/pip install -r requirements.txt
```

### 4. Activate the virtual environment

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 5. Start the PostgreSQL database

Using Make:

```bash
make db-up
```

Without Make:

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### 6. Run the application

Using Make:

```bash
make run
```

Without Make:

```bash
# Create database tables
FLASK_APP=main.py FLASK_ENV=development python -c "from app import app, db; from models import User, Task, Category; app.app_context().push(); db.create_all()"

# Run the application
FLASK_APP=main.py FLASK_ENV=development flask run --host=0.0.0.0 --port=8080
```

### 7. Access the application

Open your browser and navigate to:
```
http://localhost:8080
```

## Development Workflow

1. Make changes to the code
2. The Flask development server will automatically reload when you save changes
3. If you modify database models, you may need to restart the application

## Stopping the Services

### Stop the PostgreSQL database

Using Make:

```bash
make db-down
```

Without Make:

```bash
docker-compose -f docker-compose.dev.yml down
```

### Deactivate the virtual environment

```bash
deactivate
```

## Cleaning Up

To remove the virtual environment and generated files:

```bash
make clean
```

## Troubleshooting

- **Database Connection Issues**: 
  - Ensure the database container is running with `docker ps`
  - Check database logs with `docker-compose -f docker-compose.dev.yml logs db`
  - Verify the database connection string in your .env file

- **API Key Issues**: 
  - Verify your X.AI API key is correctly set in the `.env` file

- **Virtual Environment Issues**:
  - If you're having issues with the virtual environment, try removing it and recreating it:
    ```bash
    make clean
    make setup
    ``` 