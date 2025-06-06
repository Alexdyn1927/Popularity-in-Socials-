import pytest
from datetime import datetime
from src.trend_context_interface import (
    TrendContextInjectionInterface, 
    TrendContext, 
    TrendCategory
)

class MockTrendContextInjector(TrendContextInjectionInterface):
    """A mock implementation for testing the trend context interface."""
    
    def __init__(self, predefined_trends=None):
        self.predefined_trends = predefined_trends or [
            TrendContext(
                category=TrendCategory.PRICE_MOVEMENT,
                relevance_score=75.5,
                keywords=["Bitcoin", "Bull Market"],
                source="MockSource",
                timestamp=datetime.now()
            ),
            TrendContext(
                category=TrendCategory.TECHNOLOGY_INNOVATION,
                relevance_score=65.2,
                keywords=["Ethereum", "Layer 2"],
                source="MockSource",
                timestamp=datetime.now()
            )
        ]
    
    def fetch_trends(self, limit=None):
        return self.predefined_trends[:limit] if limit else self.predefined_trends
    
    def score_trend_relevance(self, trend):
        return trend.relevance_score
    
    def filter_trends(self, trends, categories=None, min_relevance=50.0):
        filtered_trends = [
            trend for trend in trends
            if (categories is None or trend.category in categories) and
               trend.relevance_score >= min_relevance
        ]
        return sorted(filtered_trends, key=lambda x: x.relevance_score, reverse=True)

def test_trend_context_creation():
    """Test creating a TrendContext with valid data."""
    trend = TrendContext(
        category=TrendCategory.MARKET_SENTIMENT,
        relevance_score=80.0,
        keywords=["Bullish", "Crypto"],
        source="TestSource",
        timestamp=datetime.now()
    )
    
    assert trend.category == TrendCategory.MARKET_SENTIMENT
    assert trend.relevance_score == 80.0
    assert trend.keywords == ["Bullish", "Crypto"]

def test_trend_context_injector_fetch_trends():
    """Test fetching trends from the mock injector."""
    injector = MockTrendContextInjector()
    trends = injector.fetch_trends()
    
    assert len(trends) == 2
    assert all(isinstance(trend, TrendContext) for trend in trends)

def test_trend_context_injector_limit_trends():
    """Test limiting the number of trends fetched."""
    injector = MockTrendContextInjector()
    trends = injector.fetch_trends(limit=1)
    
    assert len(trends) == 1

def test_trend_context_score_relevance():
    """Test scoring trend relevance."""
    injector = MockTrendContextInjector()
    trend = injector.fetch_trends()[0]
    
    score = injector.score_trend_relevance(trend)
    assert score == trend.relevance_score

def test_trend_context_filter_trends():
    """Test filtering trends by category and relevance."""
    injector = MockTrendContextInjector()
    all_trends = injector.fetch_trends()
    
    # Filter by category
    tech_trends = injector.filter_trends(
        all_trends, 
        categories=[TrendCategory.TECHNOLOGY_INNOVATION]
    )
    assert len(tech_trends) == 1
    assert tech_trends[0].category == TrendCategory.TECHNOLOGY_INNOVATION
    
    # Filter by minimum relevance
    high_relevance_trends = injector.filter_trends(
        all_trends, 
        min_relevance=70.0
    )
    assert len(high_relevance_trends) == 1
    assert high_relevance_trends[0].relevance_score >= 70.0

def test_trend_context_categories():
    """Verify all trend categories are defined."""
    categories = list(TrendCategory)
    assert len(categories) > 0
    assert all(isinstance(cat, TrendCategory) for cat in categories)