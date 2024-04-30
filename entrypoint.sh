#!/bin/bash

# Get the number of CPU cores on the host machine
NUM_CORES=$(nproc)

# Check if TEMPLATE_SERVER_WORKERS exceeds the number of CPU cores
if [ $TEMPLATE_SERVER_WORKERS -gt $NUM_CORES ]; then
    echo "Updating TEMPLATE_SERVER_WORKERS to match the number of CPU cores: $NUM_CORES"
    TEMPLATE_SERVER_WORKERS=$NUM_CORES
else
    echo "TEMPLATE_SERVER_WORKERS is within the limit. Using the value from .env: $TEMPLATE_SERVER_WORKERS"
fi

# Export the updated TEMPLATE_SERVER_WORKERS value
export TEMPLATE_SERVER_WORKERS=$TEMPLATE_SERVER_WORKERS

exec "$@"
