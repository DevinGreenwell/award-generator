#!/usr/bin/env python3
"""
Simple script to run the Coast Guard Award Generator locally
"""

import subprocess
import sys
import time
import webbrowser
import os

def main():
    print("🚢 Coast Guard Award Generator - Local Runner")
    print("=" * 50)
    
    # Change to the project directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Activate virtual environment and run the app
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate.bat && "
    else:
        activate_cmd = "source venv/bin/activate && "
    
    print("Starting the application...")
    print("The app will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Wait a moment then open browser
    time.sleep(2)
    webbrowser.open("http://localhost:5000")
    
    # Run the app
    try:
        subprocess.run(f"{activate_cmd}python src/app.py", shell=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")

if __name__ == "__main__":
    main()