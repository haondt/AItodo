# Docker Setup for AI-Powered Todo List Manager

This document provides instructions for running the AI-powered Todo List Manager using Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- X.AI API Key (for AI task processing)

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create environment file**

   Copy the example environment file and update it with your actual values:

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file and add your X.AI API key and other configuration values.

3. **Build and start the containers**

   ```bash
   docker-compose up -d
   ```

   This will start two containers:
   - `web`: The Flask application
   - `db`: PostgreSQL database

4. **Access the application**

   Open your browser and navigate to:
   ```
   http://localhost:8080
   ```

## Database Configuration

The application uses PostgreSQL for data storage. The database connection is automatically established using the following environment variables:

- `POSTGRES_USER`: Database username (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: postgres)
- `POSTGRES_DB`: Database name (default: todo_db)

The application will automatically create the necessary database tables on startup.

## Troubleshooting

- **Database Connection Issues**: 
  - Ensure the database container is running with `docker-compose ps`
  - Check database logs with `docker-compose logs -f db`
  - Verify the database connection string in the web service environment variables

- **API Key Issues**: 
  - Verify your X.AI API key is correctly set in the `.env` file

- **Container Logs**: 
  - View application logs with `docker-compose logs -f web`
  - View database logs with `docker-compose logs -f db`

## Stopping the Application

To stop the containers:

```bash
docker-compose down
```

To stop the containers and remove volumes (this will delete all data):

```bash
docker-compose down -v
``` 