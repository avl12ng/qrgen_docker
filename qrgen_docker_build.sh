#!/bin/bash

# Configuration
IMAGE_NAME="qrgen-app"
CONTAINER_NAME="qrgen"
PORT="5050"

echo "--- Starting Rebuild Process ---"

# 0. Check if .env exists (CRITICAL)
if [ ! -f .env ]; then
    echo "ERROR: .env file not found! Please create it first."
    exit 1
fi

# 1. Stop and remove existing container
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "Stopping and removing existing container..."
    docker rm -f ${CONTAINER_NAME}
fi

# 2. Build the image
echo "Building image..."
docker build -t ${IMAGE_NAME} .

# 3. Run the container
echo "Launching container..."
docker run -d \
    -p ${PORT}:${PORT} \
    --name ${CONTAINER_NAME} \
    --env-file .env \
    ${IMAGE_NAME}

# 4. Verification
sleep 2 # Wait for Flask to initialize
if [ "$(docker inspect -f '{{.State.Running}}' ${CONTAINER_NAME})" == "true" ]; then
    echo "--- Rebuild Complete! ---"
    echo "App is running at http://localhost:${PORT}"
else
    echo "--- ERROR: Container failed to start ---"
    docker logs ${CONTAINER_NAME}
fi
