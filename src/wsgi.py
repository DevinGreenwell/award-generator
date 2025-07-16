"""
WSGI entry point for the Coast Guard Award Generator application.
This file handles proper path setup for deployment environments.
"""

import os
import sys
from pathlib import Path

# Get the directory containing this file
current_dir = Path(__file__).parent.absolute()

# Add both the project root and src directory to Python path
project_root = current_dir.parent
src_dir = current_dir

# Add to Python path if not already there
for path in [str(project_root), str(src_dir)]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Set environment variable to help other modules find the src directory
os.environ['APP_SRC_DIR'] = str(src_dir)

# Now import the Flask app
try:
    from app import app
except ImportError:
    try:
        from src.app import app
    except ImportError as e:
        print(f"Failed to import app module")
        print(f"Current directory: {os.getcwd()}")
        print(f"Python path: {sys.path}")
        print(f"src_dir contents: {list(src_dir.iterdir()) if src_dir.exists() else 'Does not exist'}")
        raise

# This is what gunicorn will use
application = app

if __name__ == "__main__":
    # For local testing
    app.run(debug=True, host='0.0.0.0', port=5000)