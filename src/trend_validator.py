import re
from typing import Dict, Any, Optional
import logging

class TrendContextValidator:
    """
    A comprehensive validator for cryptocurrency trend context data.
    
    This class provides robust validation and sanitization methods 
    to ensure data integrity and security in trend-related inputs.
    """
    
    @staticmethod
    def sanitize_text(text: Optional[str]) -> str:
        """
        Sanitize text input by removing potentially harmful characters
        and trimming excessive whitespace.
        
        Args:
            text (Optional[str]): Input text to sanitize
        
        Returns:
            str: Sanitized text
        """
        if text is None:
            return ""
        
        # Remove potentially dangerous HTML/script tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def validate_trend_context(context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize a trend context dictionary.
        
        Args:
            context (Dict[str, Any]): Trend context dictionary to validate
        
        Returns:
            Dict[str, Any]: Validated and sanitized trend context
        
        Raises:
            ValueError: If the context is invalid or contains dangerous inputs
        """
        if not isinstance(context, dict):
            raise ValueError("Trend context must be a dictionary")
        
        # Define required and optional keys with their validation rules
        required_keys = ['topic', 'relevance_score']
        optional_keys = ['description', 'source', 'timestamp']
        
        # Check for required keys
        for key in required_keys:
            if key not in context:
                raise ValueError(f"Missing required key: {key}")
        
        # Validate and sanitize each key
        validated_context = {}
        
        # Validate topic
        topic = TrendContextValidator.sanitize_text(context.get('topic', ''))
        if not topic or len(topic) > 200:
            raise ValueError("Invalid topic: must be non-empty and less than 200 characters")
        validated_context['topic'] = topic
        
        # Validate relevance score
        try:
            score = float(context.get('relevance_score', 0))
            if score < 0 or score > 100:
                raise ValueError
            validated_context['relevance_score'] = round(score, 2)
        except (TypeError, ValueError):
            raise ValueError("Relevance score must be a number between 0 and 100")
        
        # Optional keys with sanitization
        for key in optional_keys:
            if key in context:
                value = context[key]
                if key in ['description', 'source']:
                    sanitized_value = TrendContextValidator.sanitize_text(value)
                    if sanitized_value:
                        validated_context[key] = sanitized_value
                elif key == 'timestamp':
                    # Basic timestamp validation (could be expanded)
                    try:
                        validated_context[key] = str(value)
                    except Exception:
                        logging.warning(f"Invalid timestamp: {value}")
        
        return validated_context
    
    @staticmethod
    def is_valid_trend_context(context: Dict[str, Any]) -> bool:
        """
        Check if a trend context is valid without raising exceptions.
        
        Args:
            context (Dict[str, Any]): Trend context to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            TrendContextValidator.validate_trend_context(context)
            return True
        except ValueError:
            return False