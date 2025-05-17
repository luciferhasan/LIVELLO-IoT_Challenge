#!/bin/bash

echo "🛑 Stopping and removing containers, volumes, and orphans...[Incase]"
docker-compose down -v --remove-orphans

echo "🔨 Rebuilding containers without cache..."
docker-compose build --no-cache

echo "🚀 Starting containers in detached mode..."
docker-compose up -d

echo "✅ All services are up and running!"
