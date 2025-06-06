"""
Tests for Content Generation Module
"""

import pytest
import logging
from src.content_generation import ContentGenerator
from src.trend_sourcing import TrendSourcing
from src.trend_context import TrendContextProcessor

@pytest.fixture
def content_generator():
    """Fixture to create a ContentGenerator instance."""
    return ContentGenerator(
        trend_sourcer=TrendSourcing(),
        trend_processor=TrendContextProcessor(),
        logger=logging.getLogger(__name__)
    )

def test_content_generation_basic(content_generator):
    """Test basic content generation with keywords."""
    result = content_generator.generate_content(['Bitcoin', 'Ethereum'])
    
    assert 'content' in result
    assert 'trends_used' in result
    assert len(result['trends_used']) > 0
    assert result['content'] is not None

def test_content_generation_empty_keywords(content_generator):
    """Test content generation with empty keywords."""
    result = content_generator.generate_content([])
    
    assert 'content' in result
    assert 'trends_used' in result
    assert len(result['trends_used']) == 0
    assert "No trending topics" in result['content']

def test_content_generation_multiple_content_types(content_generator):
    """Test different content generation types."""
    keywords = ['Bitcoin', 'Ethereum', 'Blockchain']
    
    article_result = content_generator.generate_content(keywords, content_type='article')
    summary_result = content_generator.generate_content(keywords, content_type='summary')
    
    assert 'Exploring top crypto trends' in article_result['content']
    assert 'Summary of' in summary_result['content']

def test_trend_context_processing(content_generator):
    """Test trend context processing and scoring."""
    trend_contexts = content_generator.trend_processor.process_trend_data({
        'Bitcoin': {1: 50, 2: 75},
        'Ethereum': {1: 30, 2: 45}
    })
    
    assert len(trend_contexts) == 2
    assert trend_contexts[0].keyword in ['Bitcoin', 'Ethereum']
    assert all(0 <= ctx.relevance_score <= 1 for ctx in trend_contexts)