#!/bin/bash

echo "Starting backend services..."
cd backend
docker compose up -d

echo "Starting API gateway..."
cd ..
cd api_gateway
docker compose up -d

echo "Starting Production Connection..."
cd ..
ngrok http 8003



