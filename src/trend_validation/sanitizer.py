"""
Trend Context Sanitization Module

Provides methods for cleaning and validating trend context data.
"""
import re
from typing import Dict, Any, List
import html
import unicodedata

class TrendContextSanitizer:
    """
    Sanitizes and validates trend context data to ensure data integrity
    and prevent potential security risks.
    """

    @staticmethod
    def sanitize_string(value: str) -> str:
        """
        Sanitize a string by:
        1. Removing HTML/XML tags
        2. Decoding HTML entities
        3. Removing control characters
        4. Normalizing unicode
        5. Trimming whitespace

        Args:
            value (str): Input string to sanitize

        Returns:
            str: Sanitized string
        """
        if not isinstance(value, str):
            return ""

        # Remove HTML/XML tags
        value = re.sub(r'<[^>]+>', '', value)
        
        # Decode HTML entities
        value = html.unescape(value)
        
        # Remove control characters
        value = re.sub(r'[\x00-\x1F\x7F]', '', value)
        
        # Normalize unicode
        value = unicodedata.normalize('NFKD', value)
        
        # Remove non-printable characters
        value = ''.join(char for char in value if char.isprintable())
        
        return value.strip()

    @staticmethod
    def validate_trend_context(trend_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and sanitize trend context data.

        Args:
            trend_context (Dict[str, Any]): Raw trend context data

        Returns:
            Dict[str, Any]: Validated and sanitized trend context
        """
        if not isinstance(trend_context, dict):
            return {}

        sanitized_context = {}
        allowed_keys = ['name', 'volume', 'sentiment', 'keywords', 'description']

        for key, value in trend_context.items():
            # Filter only allowed keys
            if key not in allowed_keys:
                continue

            # Handle different value types
            if isinstance(value, str):
                sanitized_context[key] = TrendContextSanitizer.sanitize_string(value)
            elif isinstance(value, (int, float)):
                sanitized_context[key] = value
            elif isinstance(value, list):
                sanitized_context[key] = [
                    TrendContextSanitizer.sanitize_string(str(item)) 
                    for item in value if item is not None
                ]
            else:
                sanitized_context[key] = str(value)

        return sanitized_context

    @staticmethod
    def extract_keywords(context: Dict[str, Any], max_keywords: int = 10) -> List[str]:
        """
        Extract and sanitize keywords from trend context.

        Args:
            context (Dict[str, Any]): Trend context dictionary
            max_keywords (int, optional): Maximum number of keywords. Defaults to 10.

        Returns:
            List[str]: Sanitized keywords
        """
        # Validate inputs
        if not isinstance(context, dict) or max_keywords <= 0:
            return []

        # Try multiple possible keyword sources
        keyword_sources = [
            context.get('keywords', []),
            context.get('name', '').split(),
            context.get('description', '').split()
        ]

        # Flatten and sanitize keywords
        keywords = []
        for source in keyword_sources:
            if isinstance(source, str):
                source = source.split()
            
            keywords.extend([
                TrendContextSanitizer.sanitize_string(str(kw)).lower() 
                for kw in source 
                if kw and len(TrendContextSanitizer.sanitize_string(str(kw))) > 1
            ])

        # Remove duplicates and truncate
        unique_keywords = list(dict.fromkeys(keywords))
        return unique_keywords[:max_keywords]