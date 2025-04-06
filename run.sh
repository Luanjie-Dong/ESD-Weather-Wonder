#!/bin/bash

echo "Starting backend services..."
cd backend
docker compose up -d

echo "Starting API gateway..."
cd ..
cd api_gateway
docker compose up -d

echo "Starting frontend..."
cd ..
cd frontend
npm run dev

#http://localhost:13000/d/mY9p7dQmz/weather-wonder-kong?orgId=1&from=now-15m&to=now&timezone=browser&var-service=$__all&var-instance=$__all&var-route=$__all&var-upstream=$__all&var-DS_PROMETHEUS=eei25xxfe6sjkb
