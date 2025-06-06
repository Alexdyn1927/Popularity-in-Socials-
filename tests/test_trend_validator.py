import pytest
from datetime import datetime, timedelta
from src.trend_validator import TrendContextValidator

def test_validate_topic_success():
    """Test successful topic validation."""
    topic = "Bitcoin Price Surge"
    validated = TrendContextValidator._validate_topic(topic)
    assert validated == "Bitcoin Price Surge"

def test_validate_topic_with_html():
    """Test topic validation strips HTML tags."""
    topic = "<script>alert('xss')</script>Bitcoin Trends"
    validated = TrendContextValidator._validate_topic(topic)
    assert validated == "Bitcoin Trends"

def test_validate_topic_empty():
    """Test topic validation raises error for empty topics."""
    with pytest.raises(ValueError):
        TrendContextValidator._validate_topic("")

def test_validate_relevance_score():
    """Test relevance score validation."""
    scores = [
        (50, 50),     # Normal case
        (120, 100),   # Clamping high value
        (-10, 0),     # Clamping low value
    ]
    
    for input_score, expected in scores:
        assert TrendContextValidator._validate_relevance_score(input_score) == expected

def test_validate_timestamp_default():
    """Test default timestamp generation."""
    now = datetime.utcnow()
    timestamp = TrendContextValidator._validate_timestamp(None)
    parsed_timestamp = datetime.fromisoformat(timestamp)
    
    assert parsed_timestamp > now
    assert parsed_timestamp <= now + timedelta(seconds=1)

def test_validate_timestamp_valid():
    """Test valid timestamp validation."""
    now = datetime.utcnow()
    timestamp_str = now.isoformat()
    validated = TrendContextValidator._validate_timestamp(timestamp_str)
    
    assert isinstance(validated, str)
    assert datetime.fromisoformat(validated)

def test_validate_timestamp_future():
    """Test future timestamp validation."""
    future_time = datetime.utcnow() + timedelta(days=2)
    with pytest.raises(ValueError):
        TrendContextValidator._validate_timestamp(future_time)

def test_validate_sources():
    """Test sources validation."""
    sources = [
        "https://example.com",
        "http://bitcoin.org",
        "invalid-url",
        123  # Non-string input
    ]
    
    validated = TrendContextValidator._validate_sources(sources)
    assert len(validated) == 2
    assert all(source.startswith(('http://', 'https://')) for source in validated)

def test_validate_trend_context_full():
    """Test full trend context validation."""
    trend_data = {
        'topic': 'Ethereum Market Analysis',
        'relevance_score': 85,
        'timestamp': datetime.utcnow().isoformat(),
        'sources': ['https://example.com', 'https://crypto.news']
    }
    
    validated = TrendContextValidator.validate_trend_context(trend_data)
    
    assert 'topic' in validated
    assert 'relevance_score' in validated
    assert 'timestamp' in validated
    assert 'sources' in validated
    assert validated['topic'] == 'Ethereum Market Analysis'