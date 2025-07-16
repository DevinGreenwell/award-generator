#!/bin/bash

# Coast Guard Award Generator - Local Deployment Script

echo "🚢 Coast Guard Award Generator - Local Deployment"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment found"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "⚠️  No .env file found. Creating from .env.example..."
        cp .env.example .env
        echo "❗ IMPORTANT: Please edit .env and add your OpenAI API key"
        echo "   Open .env in a text editor and replace 'your_openai_api_key_here' with your actual key"
        echo ""
        read -p "Press Enter after you've added your API key to continue..."
    else
        echo "❌ No .env or .env.example file found"
        exit 1
    fi
fi

# Create logs directory if it doesn't exist
if [ ! -d "logs" ]; then
    echo "📁 Creating logs directory..."
    mkdir -p logs
fi

# Create sessions directory if needed
if [ ! -d "sessions" ]; then
    echo "📁 Creating sessions directory..."
    mkdir -p sessions
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Starting the application..."
echo "================================================"
echo "🌐 The application will be available at: http://localhost:5000"
echo "📝 Logs will be saved to: logs/app.log"
echo "🛑 Press Ctrl+C to stop the server"
echo "================================================"
echo ""

# Run the application
python3 src/app.py