#!/bin/bash
# Test the application locally with gunicorn configuration

echo "Testing Coast Guard Award Generator with O4 model and gunicorn..."
echo "================================================"

# Load environment variables
source .env

# Kill any existing processes on port 5000
echo "Killing any existing processes on port 5000..."
lsof -ti:5000 | xargs kill -9 2>/dev/null || true

# Start gunicorn with configuration
echo "Starting gunicorn with increased timeout for O4 model..."
python -m gunicorn --config gunicorn_config.py --chdir src wsgi:application