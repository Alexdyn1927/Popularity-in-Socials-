"""
Unit tests for Trend Context Validation and Sanitization.
"""
import pytest
from src.trend_validation.sanitizer import TrendContextSanitizer

def test_sanitize_string():
    """Test string sanitization methods."""
    # Test HTML tag removal
    assert TrendContextSanitizer.sanitize_string('<b>Hello</b> World') == 'Hello World'
    
    # Test HTML entity decoding
    assert TrendContextSanitizer.sanitize_string('&lt;script&gt;') == '<script>'
    
    # Test control character removal
    assert TrendContextSanitizer.sanitize_string('Hello\x00World') == 'HelloWorld'
    
    # Test whitespace trimming
    assert TrendContextSanitizer.sanitize_string('  Test  ') == 'Test'

def test_validate_trend_context():
    """Test trend context validation and sanitization."""
    sample_context = {
        'name': '<b>Bitcoin</b> Trend',
        'volume': 1000,
        'sentiment': 'Bullish &amp; Strong',
        'keywords': ['crypto', '<script>alert()</script>'],
        'extra_field': 'Ignored',
        'description': 'Cryptocurrency market leader'
    }
    
    validated = TrendContextSanitizer.validate_trend_context(sample_context)
    
    assert validated == {
        'name': 'Bitcoin Trend',
        'volume': 1000,
        'sentiment': 'Bullish & Strong',
        'keywords': ['crypto'],
        'description': 'Cryptocurrency market leader'
    }

def test_extract_keywords():
    """Test keyword extraction and sanitization."""
    context = {
        'name': 'Bitcoin Crypto Revolution',
        'keywords': ['blockchain', '<script>hack</script>'],
        'description': 'Decentralized finance platform'
    }
    
    keywords = TrendContextSanitizer.extract_keywords(context)
    
    assert set(keywords) == {'bitcoin', 'crypto', 'revolution', 'blockchain', 'decentralized', 'finance', 'platform'}
    assert len(keywords) <= 10

def test_invalid_input_handling():
    """Test handling of invalid input types."""
    assert TrendContextSanitizer.sanitize_string(None) == ''
    assert TrendContextSanitizer.validate_trend_context(None) == {}
    assert TrendContextSanitizer.extract_keywords(None) == []