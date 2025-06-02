import sys
import os

# Import the Flask app directly
from app import app

# This is the entry point for the deployment service
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
