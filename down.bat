@echo off

echo Stopping backend services...
cd backend
docker compose down -v

echo Stopping API gateway services...
cd ..\api_gateway
docker compose down -v

echo Stopping frontend development server...
taskkill /F /IM node.exe

echo All services have been stopped.
