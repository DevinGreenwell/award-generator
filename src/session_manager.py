"""
Session manager for handling large session data using file storage.
"""

import os
import json
import uuid
import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)


class FileSessionManager:
    """Manages session data using file storage to avoid cookie size limits."""
    
    def __init__(self, session_dir: str = "sessions", max_age_hours: int = 24):
        self.session_dir = session_dir
        self.max_age_hours = max_age_hours
        
        # Create session directory if it doesn't exist
        os.makedirs(self.session_dir, exist_ok=True)
        
        # Clean up old sessions on init
        self.cleanup_old_sessions()
    
    def _get_session_path(self, session_id: str) -> str:
        """Get the file path for a session."""
        # Hash the session ID for security
        safe_id = hashlib.sha256(session_id.encode()).hexdigest()
        return os.path.join(self.session_dir, f"{safe_id}.json")
    
    def create_session(self) -> str:
        """Create a new session and return its ID."""
        session_id = str(uuid.uuid4())
        session_data = {
            'created_at': time.time(),
            'last_accessed': time.time(),
            'data': {}
        }
        
        path = self._get_session_path(session_id)
        with open(path, 'w') as f:
            json.dump(session_data, f)
        
        logger.info(f"Created new session: {session_id}")
        return session_id
    
    def get_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data by ID."""
        if not session_id:
            return None
        
        path = self._get_session_path(session_id)
        if not os.path.exists(path):
            return None
        
        try:
            with open(path, 'r') as f:
                session_data = json.load(f)
            
            # Update last accessed time
            session_data['last_accessed'] = time.time()
            with open(path, 'w') as f:
                json.dump(session_data, f)
            
            return session_data['data']
        except Exception as e:
            logger.error(f"Error reading session {session_id}: {e}")
            return None
    
    def update_session_data(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Update session data."""
        if not session_id:
            return False
        
        path = self._get_session_path(session_id)
        
        try:
            # Read existing session or create new one
            if os.path.exists(path):
                with open(path, 'r') as f:
                    session_data = json.load(f)
            else:
                session_data = {
                    'created_at': time.time(),
                    'data': {}
                }
            
            # Update data
            session_data['last_accessed'] = time.time()
            session_data['data'].update(data)
            
            # Write back
            with open(path, 'w') as f:
                json.dump(session_data, f)
            
            return True
        except Exception as e:
            logger.error(f"Error updating session {session_id}: {e}")
            return False
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if not session_id:
            return False
        
        path = self._get_session_path(session_id)
        if os.path.exists(path):
            try:
                os.remove(path)
                logger.info(f"Deleted session: {session_id}")
                return True
            except Exception as e:
                logger.error(f"Error deleting session {session_id}: {e}")
        
        return False
    
    def cleanup_old_sessions(self):
        """Remove sessions older than max_age_hours."""
        cutoff_time = time.time() - (self.max_age_hours * 3600)
        cleaned = 0
        
        for filename in os.listdir(self.session_dir):
            if not filename.endswith('.json'):
                continue
            
            path = os.path.join(self.session_dir, filename)
            try:
                with open(path, 'r') as f:
                    session_data = json.load(f)
                
                if session_data.get('last_accessed', 0) < cutoff_time:
                    os.remove(path)
                    cleaned += 1
            except Exception as e:
                logger.error(f"Error cleaning up session file {filename}: {e}")
        
        if cleaned > 0:
            logger.info(f"Cleaned up {cleaned} old sessions")
    
    def get_session_size(self, session_id: str) -> int:
        """Get the size of session data in bytes."""
        if not session_id:
            return 0
        
        path = self._get_session_path(session_id)
        if os.path.exists(path):
            return os.path.getsize(path)
        return 0


# Global session manager instance
session_manager = FileSessionManager()


def get_or_create_session_id(flask_session) -> str:
    """Get existing session ID or create a new one."""
    session_id = flask_session.get('sid')
    if not session_id:
        session_id = session_manager.create_session()
        flask_session['sid'] = session_id
        flask_session.permanent = True
    return session_id


def store_session_data(flask_session, key: str, value: Any) -> bool:
    """Store data in file-based session."""
    session_id = get_or_create_session_id(flask_session)
    data = session_manager.get_session_data(session_id) or {}
    data[key] = value
    return session_manager.update_session_data(session_id, data)


def get_session_data(flask_session, key: str = None) -> Any:
    """Get data from file-based session."""
    session_id = flask_session.get('sid')
    if not session_id:
        return None
    
    data = session_manager.get_session_data(session_id)
    if data is None:
        return None
    
    if key:
        return data.get(key)
    return data


def clear_session_data(flask_session) -> bool:
    """Clear all session data."""
    session_id = flask_session.get('sid')
    if session_id:
        success = session_manager.delete_session(session_id)
        flask_session.pop('sid', None)
        return success
    return True