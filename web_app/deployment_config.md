# Coast Guard Award Writing Tool - Deployment Configuration

## Overview
This document outlines the deployment configuration for the Coast Guard Award Writing Tool web application. The application will be deployed as a Flask web application using Gunicorn as the WSGI server.

## Requirements
- Python 3.9+
- Flask
- Gunicorn
- OpenAI Python client

## Directory Structure
```
coast_guard_award_tool/
├── web_app/
│   ├── app.py                 # Main Flask application
│   ├── openai_client.py       # OpenAI API integration
│   ├── award_engine.py        # Award recommendation engine
│   ├── requirements.txt       # Python dependencies
│   ├── static/                # Static assets
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   └── app.js
│   │   └── img/
│   │       └── placeholder_logo.png
│   └── templates/             # HTML templates
│       └── index.html
└── src/                       # Required for deployment
    └── main.py                # Entry point for deployment
```

## Deployment Files

### requirements.txt
```
flask==2.3.2
gunicorn==21.2.0
openai==0.27.8
python-dotenv==1.0.0
```

### src/main.py
```python
import sys
import os

# Add the web_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'web_app'))

# Import the Flask app
from app import app

# This is the entry point for the deployment service
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
```

## Environment Variables
The following environment variables should be set in the deployment environment:
- `OPENAI_API_KEY`: API key for OpenAI
- `FLASK_SECRET_KEY`: Secret key for Flask session encryption
- `PORT`: Port to run the application on (default: 8080)

## Deployment Steps
1. Create the deployment directory structure
2. Copy all application files to the appropriate locations
3. Create the requirements.txt file
4. Create the src/main.py entry point
5. Deploy the application using the deployment tool
6. Verify the application is accessible at the provided URL

## Post-Deployment Verification
After deployment, verify the following:
1. The application loads correctly at the provided URL
2. The chat interface functions properly
3. Award recommendations can be generated
4. Session management works as expected
5. The application is responsive on different devices

## Monitoring and Maintenance
- Monitor application logs for errors
- Check OpenAI API usage and limits
- Update the application as needed with new features or bug fixes
