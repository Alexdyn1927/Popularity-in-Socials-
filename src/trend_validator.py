from typing import Dict, Any, List
import re
from datetime import datetime, timedelta

class TrendContextValidator:
    """
    Validates and sanitizes trend context data for cryptocurrency content generation.
    
    Provides comprehensive validation and sanitization of trend-related inputs
    to ensure data integrity, prevent injection, and normalize trend information.
    """
    
    @staticmethod
    def validate_trend_context(trend_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates and sanitizes a complete trend context dictionary.
        
        Args:
            trend_data (Dict[str, Any]): Raw trend context data
        
        Returns:
            Dict[str, Any]: Validated and sanitized trend context
        
        Raises:
            ValueError: If trend data fails validation
        """
        if not isinstance(trend_data, dict):
            raise ValueError("Trend data must be a dictionary")
        
        # Validate and sanitize each key component
        validated_data = {
            'topic': TrendContextValidator._validate_topic(trend_data.get('topic', '')),
            'relevance_score': TrendContextValidator._validate_relevance_score(trend_data.get('relevance_score', 0)),
            'timestamp': TrendContextValidator._validate_timestamp(trend_data.get('timestamp')),
            'sources': TrendContextValidator._validate_sources(trend_data.get('sources', [])),
        }
        
        return validated_data
    
    @staticmethod
    def _validate_topic(topic: str) -> str:
        """
        Validate and sanitize trend topic.
        
        Args:
            topic (str): Raw topic string
        
        Returns:
            str: Sanitized topic
        """
        if not isinstance(topic, str):
            raise ValueError("Topic must be a string")
        
        # Remove any potential HTML or script tags
        sanitized_topic = re.sub(r'<[^>]+>', '', topic)
        
        # Limit topic length and remove excessive whitespace
        sanitized_topic = ' '.join(sanitized_topic.split())[:200]
        
        if not sanitized_topic:
            raise ValueError("Topic cannot be empty after sanitization")
        
        return sanitized_topic
    
    @staticmethod
    def _validate_relevance_score(score: float) -> float:
        """
        Validate trend relevance score.
        
        Args:
            score (float): Raw relevance score
        
        Returns:
            float: Validated score
        """
        try:
            score = float(score)
        except (TypeError, ValueError):
            raise ValueError("Relevance score must be a number")
        
        # Clamp score between 0 and 100
        return max(0, min(100, score))
    
    @staticmethod
    def _validate_timestamp(timestamp: Any) -> str:
        """
        Validate and normalize timestamp.
        
        Args:
            timestamp (Any): Raw timestamp input
        
        Returns:
            str: ISO 8601 formatted timestamp
        """
        if timestamp is None:
            return datetime.utcnow().isoformat()
        
        try:
            # Convert to datetime if it's not already
            if not isinstance(timestamp, datetime):
                timestamp = datetime.fromisoformat(str(timestamp))
            
            # Prevent future timestamps or timestamps too far in the past
            now = datetime.utcnow()
            if timestamp > now or timestamp < (now - timedelta(days=365)):
                raise ValueError("Timestamp out of acceptable range")
            
            return timestamp.isoformat()
        except (TypeError, ValueError):
            raise ValueError("Invalid timestamp format")
    
    @staticmethod
    def _validate_sources(sources: List[str]) -> List[str]:
        """
        Validate and sanitize trend sources.
        
        Args:
            sources (List[str]): Raw sources list
        
        Returns:
            List[str]: Validated and sanitized sources
        """
        if not isinstance(sources, list):
            raise ValueError("Sources must be a list")
        
        # URL validation regex
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        validated_sources = []
        for source in sources:
            if not isinstance(source, str):
                continue
            
            # Sanitize and validate source URL
            source = source.strip()
            if url_pattern.match(source):
                validated_sources.append(source)
        
        return validated_sources[:5]  # Limit to 5 sources