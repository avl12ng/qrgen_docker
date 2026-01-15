#!/bin/bash

# Configuration
NETWORK_NAME="qrgen-network"
GEN_IMAGE="qr-gen"
TESTER_IMAGE="qr-tester"

echo "--- Starting Global Rebuild Process ---"

# 1. Load environment variables correctly
if [ -f .env ]; then
    set -a
    source .env
    set +a
    echo "--- Configuration loaded from .env ---"
else
    echo "ERROR: .env file not found."
    exit 1
fi

# 2. Network Setup
if ! docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
    echo "Creating Docker network: ${NETWORK_NAME}..."
    docker network create "$NETWORK_NAME"
fi

# 3. Cleanup existing containers
echo "Cleaning up existing containers..."
docker rm -f qrgen qrgen-tester >/dev/null 2>&1

# 4. Build & Run: QR GENERATOR
echo "Building Generator image..."
docker build -t ${GEN_IMAGE} .

docker run -d \
    --name qrgen \
    --network ${NETWORK_NAME} \
    --env-file .env \
    -p ${PORT_GEN}:${PORT_GEN} \
    ${GEN_IMAGE}

# 5. Build & Run: API TESTER
if [ -d "tester" ]; then
    echo "Building and Launching Tester..."
    docker build -t ${TESTER_IMAGE} ./tester
    docker run -d \
        --name qrgen-tester \
        --network ${NETWORK_NAME} \
        -p ${PORT_TESTER}:80 \
        -e QR_API_URL=${QR_API_URL} \
        -e QR_API_TOKEN=${API_TOKEN} \
        ${TESTER_IMAGE}
else
    echo "INFO: 'tester' directory not found, skipping tester deployment."
fi

echo "--- Process Finished ---"
echo "Generator UI: http://localhost:${PORT_GEN}"
echo "API Tester UI: http://localhost:${PORT_TESTER}"
