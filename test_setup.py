#!/usr/bin/env python3
"""
Test script to verify the Coast Guard Award Generator setup
"""

import sys
import os

def test_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False

def test_imports():
    """Test if all required packages can be imported"""
    print("\n📦 Testing package imports...")
    
    packages = [
        ("flask", "Flask"),
        ("flask_cors", "Flask-CORS"),
        ("openai", "OpenAI"),
        ("docx", "python-docx"),
        ("dotenv", "python-dotenv")
    ]
    
    all_good = True
    for module, name in packages:
        try:
            __import__(module)
            print(f"✅ {name} - OK")
        except ImportError:
            print(f"❌ {name} - Not installed")
            all_good = False
    
    return all_good

def test_env_file():
    """Check if .env file exists and has required keys"""
    print("\n🔐 Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Run: cp .env.example .env")
        print("   Then add your OpenAI API key")
        return False
    
    print("✅ .env file found")
    
    # Load and check for API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ OpenAI API key not configured")
        print("   Edit .env and add your actual API key")
        return False
    
    print("✅ OpenAI API key configured")
    return True

def test_directories():
    """Check if required directories exist"""
    print("\n📁 Checking directories...")
    
    dirs = ['src', 'src/static', 'src/templates', 'src/award_engine', 'logs']
    all_good = True
    
    for dir_path in dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path} - OK")
        else:
            print(f"❌ {dir_path} - Missing")
            all_good = False
    
    return all_good

def test_app_import():
    """Test if the app can be imported"""
    print("\n🚀 Testing application import...")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from src import app
        print("✅ Application modules load successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import application: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Coast Guard Award Generator - Setup Test")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_directories,
        test_imports,
        test_env_file,
        test_app_import
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All tests passed! You're ready to run the application.")
        print("\nTo start the app, run:")
        print("  ./deploy_local.sh")
        print("\nOr manually:")
        print("  source venv/bin/activate")
        print("  python src/app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Create .env file: cp .env.example .env")
        print("3. Add your OpenAI API key to .env")
    
    return all(results)

if __name__ == "__main__":
    sys.exit(0 if main() else 1)