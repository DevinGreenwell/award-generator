#!/usr/bin/env python
"""
Startup script for the Coast Guard Award Generator application.
This ensures proper path configuration for deployment.
"""

import os
import sys
from pathlib import Path

# Get the directory containing this file (project root)
project_root = Path(__file__).parent.absolute()
src_dir = project_root / 'src'

# Add both directories to Python path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_dir))

# Change to src directory
os.chdir(str(src_dir))

# Import and run the application
from src.wsgi import application

if __name__ == "__main__":
    # Get port from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    application.run(host='0.0.0.0', port=port, debug=False)