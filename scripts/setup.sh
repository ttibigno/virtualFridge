#!/usr/bin/env bash
set -euo pipefail
ENV_FILE=".env"
ENV_EXAMPLE=".env.example"
if ! docker -v; then
    echo "Error, Docker Engine is not installed in the system"
    exit 1
fi
if ! docker compose version; then
    echo "Error, Docker Compose is not installed in the system"
    exit 1
fi
if [ ! -f "$ENV_FILE" ]; then
    cp "$ENV_EXAMPLE" "$ENV_FILE"
    echo "Generated .env file from .env.example base"
else
    echo "Loaded environmental values from .env"
fi