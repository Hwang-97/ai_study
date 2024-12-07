#!/bin/bash

# Usage: ./run.sh <project_name> <port>
# Default values
PROJECT_NAME=${1:-study}
PORT=${2:-8000}

# Navigate to the project directory
cd "$(dirname "$0")/$PROJECT_NAME" || { echo "Project directory not found!"; exit 1; }

# Activate virtual environment (if any)
if [ -f "../venv/bin/activate" ]; then
    source ../venv/bin/activate
fi

# Run the Django server on the specified port
python manage.py runserver localhost:$PORT
