"""
Configuration management for the Coast Guard Award Generator.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src"
STATIC_DIR = SRC_DIR / "static"
TEMPLATES_DIR = SRC_DIR / "templates"

# Application settings
class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini-2024-07-18')
    OPENAI_MAX_RETRIES = int(os.getenv('OPENAI_MAX_RETRIES', '3'))
    OPENAI_RETRY_DELAY = int(os.getenv('OPENAI_RETRY_DELAY', '1'))
    
    # Session settings
    SESSION_TYPE = os.getenv('SESSION_TYPE', 'filesystem')
    SESSION_FILE_DIR = os.getenv('SESSION_FILE_DIR', str(BASE_DIR / 'sessions'))
    PERMANENT_SESSION_LIFETIME = int(os.getenv('SESSION_LIFETIME', '86400'))  # 24 hours
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.getenv('LOG_FILE', str(BASE_DIR / 'logs' / 'app.log'))
    
    # Export settings
    EXPORT_TEMP_DIR = os.getenv('EXPORT_TEMP_DIR', str(BASE_DIR / 'temp'))
    MAX_EXPORT_SIZE = int(os.getenv('MAX_EXPORT_SIZE', '10485760'))  # 10MB
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', '10485760'))  # 10MB
    
    # Security settings
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY environment variable is required")
        
        if errors:
            raise ValueError(f"Configuration errors: {'; '.join(errors)}")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


# Select configuration based on environment
env = os.getenv('FLASK_ENV', 'development')
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': DevelopmentConfig  # Use development config for testing
}

current_config = config_map.get(env, DevelopmentConfig)


def setup_logging():
    """Set up logging configuration."""
    # Create logs directory if it doesn't exist
    log_dir = Path(current_config.LOG_FILE).parent
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, current_config.LOG_LEVEL),
        format=current_config.LOG_FORMAT,
        handlers=[
            logging.FileHandler(current_config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    # Set specific loggers
    logging.getLogger('werkzeug').setLevel(logging.WARNING)  # Reduce Flask noise
    logging.getLogger('urllib3').setLevel(logging.WARNING)   # Reduce HTTP noise
    
    return logging.getLogger(__name__)