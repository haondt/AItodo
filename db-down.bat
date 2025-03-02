@echo off
echo Stopping PostgreSQL database...

docker-compose -f docker-compose.dev.yml down

echo PostgreSQL database stopped. 