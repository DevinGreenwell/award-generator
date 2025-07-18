# Coast Guard Award Generator - Local Deployment Guide

## Quick Start

The application has been successfully configured and is ready to run!

### Option 1: Using the Python Runner (Recommended)
```bash
python run_local.py
```
This will automatically:
- Start the Flask server
- Open your web browser to http://localhost:5000
- Display the application

### Option 2: Using the Deployment Script
```bash
./deploy_local.sh
```

### Option 3: Manual Start
```bash
source venv/bin/activate
python src/app.py
```
Then open http://localhost:5000 in your browser.

## Testing the Application

1. **Access the Application**
   - Open http://localhost:5000 in your web browser
   - You should see the Coast Guard Award Generator interface

2. **Test Basic Functionality**
   - Fill in awardee information (Name, Rank, Unit)
   - Enter some achievements in the chat interface
   - Click "Generate Recommendation" to get an award recommendation
   - Try the "Export Word Document" feature

## Troubleshooting

### Port Already in Use
If you get an error about port 5000 being in use:
```bash
# Find what's using port 5000
lsof -i :5000

# Kill the process (replace PID with actual process ID)
kill -9 PID
```

### Dependencies Issues
If you encounter dependency errors:
```bash
# Clean install
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### OpenAI API Key Issues
Make sure your `.env` file contains a valid OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```

## Application Features

1. **Chat Interface**: Describe achievements and accomplishments
2. **Award Analysis**: Automatically determines appropriate award level
3. **Improvement Suggestions**: Get specific feedback to strengthen the recommendation
4. **Document Export**: Generate professional Word documents
5. **Session Management**: Clear session to start fresh

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Next Steps

1. Test all features to ensure they work correctly
2. Review the generated award recommendations
3. Export a sample Word document
4. Provide feedback on any issues or improvements needed

The application is now fully functional with:
- ✅ Modular code structure
- ✅ Enhanced error handling
- ✅ Input validation
- ✅ Comprehensive logging
- ✅ Retry logic for API calls
- ✅ Professional document export
- ✅ Clean, maintainable codebase

## Cloud Deployment (Railway, Heroku, etc.)

The application has been configured to work with cloud deployment platforms. The import paths have been fixed to work in both local and deployed environments.

### Railway Deployment

1. The app includes a `railway.json` configuration file
2. The `Procfile` has been updated to use the proper startup command
3. A `wsgi.py` file handles proper path configuration

### Key Files for Deployment

- `src/wsgi.py` - WSGI entry point with path configuration
- `Procfile` - Defines the web process command
- `railway.json` - Railway-specific configuration
- `start.py` - Alternative startup script if needed

### Environment Variables Required

Make sure to set these in your deployment platform:
- `OPENAI_API_KEY` - Your OpenAI API key
- `SECRET_KEY` - A secure secret key for Flask sessions
- `PORT` - Usually set automatically by the platform

The import path fixes ensure the app works correctly whether it's:
- Run locally from the project root
- Run from within the src directory  
- Deployed to `/app/src/` in a container
- Started via gunicorn with different working directories