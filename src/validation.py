"""
Input validation schemas for the Coast Guard Award Generator.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import re


class ValidationError(Exception):
    """Custom validation error."""
    pass


class BaseValidator:
    """Base validator class."""
    
    @staticmethod
    def validate_required(data: Dict, field: str, field_type: type = str) -> Any:
        """Validate a required field exists and has correct type."""
        if field not in data:
            raise ValidationError(f"Required field '{field}' is missing")
        
        value = data[field]
        if not isinstance(value, field_type):
            raise ValidationError(f"Field '{field}' must be of type {field_type.__name__}")
        
        if field_type == str and not value.strip():
            raise ValidationError(f"Field '{field}' cannot be empty")
        
        return value
    
    @staticmethod
    def validate_optional(data: Dict, field: str, field_type: type = str, 
                         default: Any = None) -> Any:
        """Validate an optional field if present."""
        if field not in data:
            return default
        
        value = data[field]
        if value is None:
            return default
        
        if not isinstance(value, field_type):
            raise ValidationError(f"Field '{field}' must be of type {field_type.__name__}")
        
        return value


class AwardeeInfoValidator(BaseValidator):
    """Validator for awardee information."""
    
    @classmethod
    def validate(cls, data: Dict) -> Dict:
        """Validate awardee information."""
        cleaned = {}
        
        # Required fields
        cleaned['name'] = cls.validate_required(data, 'name')
        cleaned['rank'] = cls.validate_required(data, 'rank')
        
        # Optional fields
        cleaned['unit'] = cls.validate_optional(data, 'unit', default='')
        cleaned['position'] = cls.validate_optional(data, 'position', default='')
        cleaned['service_number'] = cls.validate_optional(data, 'service_number', default='')
        
        # Date validation
        date_start = cls.validate_optional(data, 'date_start')
        date_end = cls.validate_optional(data, 'date_end')
        
        if date_start and date_end:
            try:
                start = datetime.fromisoformat(date_start)
                end = datetime.fromisoformat(date_end)
                if start > end:
                    raise ValidationError("Start date must be before end date")
                cleaned['date_start'] = date_start
                cleaned['date_end'] = date_end
            except ValueError:
                raise ValidationError("Invalid date format. Use YYYY-MM-DD")
        
        # Name validation (basic)
        if not re.match(r'^[a-zA-Z\s\-\.\']+$', cleaned['name']):
            raise ValidationError("Name contains invalid characters")
        
        # Rank validation (ensure it's not just numbers)
        if cleaned['rank'].isdigit():
            raise ValidationError("Rank must include text, not just numbers")
        
        return cleaned


class AchievementDataValidator(BaseValidator):
    """Validator for achievement data."""
    
    @classmethod
    def validate(cls, data: Dict) -> Dict:
        """Validate achievement data."""
        cleaned = {}
        
        # List fields
        list_fields = [
            'achievements', 'impacts', 'leadership_details', 'innovation_details',
            'challenges', 'valor_indicators', 'quantifiable_metrics', 'awards_received',
            'collaboration', 'training_provided', 'above_beyond_indicators',
            'emergency_response'
        ]
        
        for field in list_fields:
            value = cls.validate_optional(data, field, list, default=[])
            # Ensure all items in list are strings
            cleaned[field] = [str(item).strip() for item in value if str(item).strip()]
        
        # String fields
        cleaned['scope'] = cls.validate_optional(data, 'scope', default='Not specified')
        cleaned['time_period'] = cls.validate_optional(data, 'time_period', default='Not specified')
        cleaned['justification'] = cls.validate_optional(data, 'justification', 
                                                        default='Based on provided accomplishments')
        
        # Validate at least some achievements exist
        if not any(cleaned[field] for field in ['achievements', 'impacts']):
            raise ValidationError("At least one achievement or impact must be provided")
        
        return cleaned


class MessageValidator(BaseValidator):
    """Validator for chat messages."""
    
    @classmethod
    def validate(cls, data: Dict) -> Dict:
        """Validate chat message."""
        cleaned = {}
        
        cleaned['message'] = cls.validate_required(data, 'message')
        
        # Limit message length
        if len(cleaned['message']) > 5000:
            raise ValidationError("Message is too long (max 5000 characters)")
        
        # Optional workflow state
        cleaned['workflow_state'] = cls.validate_optional(
            data, 'workflow_state', default='input'
        )
        
        return cleaned


class ExportRequestValidator(BaseValidator):
    """Validator for export requests."""
    
    ALLOWED_FORMATS = ['docx', 'json', 'txt']
    
    @classmethod
    def validate(cls, data: Dict) -> Dict:
        """Validate export request."""
        cleaned = {}
        
        # Format validation
        format_type = cls.validate_optional(data, 'format', default='docx')
        if format_type not in cls.ALLOWED_FORMATS:
            raise ValidationError(f"Invalid export format. Allowed: {cls.ALLOWED_FORMATS}")
        cleaned['format'] = format_type
        
        # Optional awardee info
        if 'awardee_info' in data:
            cleaned['awardee_info'] = AwardeeInfoValidator.validate(data['awardee_info'])
        else:
            cleaned['awardee_info'] = {}
        
        return cleaned


class SessionDataValidator(BaseValidator):
    """Validator for session data."""
    
    @classmethod
    def validate(cls, data: Dict) -> Dict:
        """Validate session data."""
        cleaned = {}
        
        # Session identification
        cleaned['session_id'] = cls.validate_optional(data, 'session_id', default='')
        cleaned['session_name'] = cls.validate_optional(data, 'session_name', default='Unnamed Session')
        
        # Limit session name length
        if len(cleaned['session_name']) > 100:
            raise ValidationError("Session name is too long (max 100 characters)")
        
        # Optional awardee info
        if 'awardee_info' in data:
            cleaned['awardee_info'] = AwardeeInfoValidator.validate(data['awardee_info'])
        
        # Messages validation (basic)
        if 'messages' in data:
            if not isinstance(data['messages'], list):
                raise ValidationError("Messages must be a list")
            cleaned['messages'] = data['messages']
        
        return cleaned