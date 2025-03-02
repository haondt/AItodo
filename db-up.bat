@echo off
echo Starting PostgreSQL database in Docker...

docker-compose -f docker-compose.dev.yml up -d

echo PostgreSQL is running on localhost:5432
echo Connection string: postgresql://postgres:postgres@localhost:5432/todo_db 