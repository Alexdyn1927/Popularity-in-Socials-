import pytest
from datetime import datetime, timedelta
from src.trend_context import ITrendSource, TrendMetadata, TrendContext

class MockTrendSource(ITrendSource):
    """
    Mock implementation of ITrendSource for testing
    """
    def __init__(self, trends=None):
        self._trends = trends or [
            TrendMetadata(
                name="Bitcoin", 
                score=0, 
                timestamp=datetime.now(),
                additional_info={"volume": 1000000}
            ),
            TrendMetadata(
                name="Ethereum", 
                score=0, 
                timestamp=datetime.now(),
                additional_info={"volume": 500000}
            )
        ]
    
    def fetch_trends(self, limit=None):
        return self._trends[:limit] if limit else self._trends
    
    def score_trend(self, trend):
        # Simple scoring based on additional info volume
        volume = trend.additional_info.get('volume', 0)
        return min(100, volume / 10000)

def test_trend_metadata_creation():
    """Test creating TrendMetadata"""
    now = datetime.now()
    trend = TrendMetadata(
        name="Bitcoin", 
        score=85.5, 
        timestamp=now,
        additional_info={"volume": 1000000}
    )
    
    assert trend.name == "Bitcoin"
    assert trend.score == 85.5
    assert trend.timestamp == now
    assert trend.additional_info == {"volume": 1000000}

def test_trend_source_interface():
    """Test MockTrendSource implementation"""
    source = MockTrendSource()
    
    # Test fetch_trends
    trends = source.fetch_trends()
    assert len(trends) == 2
    assert all(isinstance(trend, TrendMetadata) for trend in trends)
    
    # Test scoring
    first_trend = trends[0]
    score = source.score_trend(first_trend)
    assert 0 <= score <= 100

def test_trend_context_initialization():
    """Test TrendContext initialization and trend update"""
    sources = [MockTrendSource(), MockTrendSource()]
    context = TrendContext(sources)
    
    # Update trends
    updated_trends = context.update_trends(min_score=10)
    
    assert len(updated_trends) > 0
    assert all(trend.score >= 10 for trend in updated_trends)
    assert context.trends == updated_trends

def test_trend_context_filtering():
    """Test trend filtering by minimum score"""
    sources = [MockTrendSource()]
    context = TrendContext(sources)
    
    # Test high score filter
    high_score_trends = context.update_trends(min_score=50)
    assert all(trend.score >= 50 for trend in high_score_trends)
    
    # Test low score filter
    low_score_trends = context.update_trends(min_score=10)
    assert all(trend.score >= 10 for trend in low_score_trends)

def test_trend_context_sorting():
    """Test trends are sorted by score in descending order"""
    sources = [MockTrendSource()]
    context = TrendContext(sources)
    
    updated_trends = context.update_trends()
    
    # Verify sorted by score (descending)
    for i in range(1, len(updated_trends)):
        assert updated_trends[i-1].score >= updated_trends[i].score