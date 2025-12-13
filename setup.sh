#!/bin/bash

# Pizza Bot Setup Script

echo "Pizza Bot Setup Initiated..."

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

echo "Docker and Docker Compose found."

# Environment Configuration
if [ ! -f .env ]; then
    echo ".env file not found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo ".env created. Please update it with your GROQ_API_KEY."
    else
        echo ".env.example not found. Cannot create configuration."
        exit 1
    fi
else
    echo ".env file already exists."
fi

# Build and Run
echo "Building and starting containers..."
docker-compose up --build

echo "Setup complete! Access the application at http://localhost:3000"
