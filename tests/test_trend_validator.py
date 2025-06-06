import pytest
from src.trend_validator import TrendContextValidator

class TestTrendContextValidator:
    def test_sanitize_text_basic(self):
        """Test basic text sanitization"""
        assert TrendContextValidator.sanitize_text("  Hello World!  ") == "Hello World!"
        assert TrendContextValidator.sanitize_text(None) == ""
    
    def test_sanitize_text_html_removal(self):
        """Test removal of HTML tags"""
        assert TrendContextValidator.sanitize_text("<script>alert('test')</script>Hello") == "Hello"
    
    def test_validate_trend_context_valid_input(self):
        """Test validation of a valid trend context"""
        valid_context = {
            'topic': 'Bitcoin Price Surge',
            'relevance_score': 85.5,
            'description': 'Cryptocurrency market movement',
            'source': 'CoinDesk',
            'timestamp': '2023-06-15'
        }
        
        validated = TrendContextValidator.validate_trend_context(valid_context)
        assert validated['topic'] == 'Bitcoin Price Surge'
        assert validated['relevance_score'] == 85.50
    
    def test_validate_trend_context_missing_required_keys(self):
        """Test validation fails for missing required keys"""
        invalid_contexts = [
            {},
            {'topic': 'Test'},
            {'relevance_score': 50}
        ]
        
        for context in invalid_contexts:
            with pytest.raises(ValueError):
                TrendContextValidator.validate_trend_context(context)
    
    def test_validate_trend_context_invalid_score(self):
        """Test validation fails for invalid relevance scores"""
        invalid_scores = [
            {'topic': 'Test Topic', 'relevance_score': -1},
            {'topic': 'Test Topic', 'relevance_score': 101},
            {'topic': 'Test Topic', 'relevance_score': 'not a number'}
        ]
        
        for context in invalid_scores:
            with pytest.raises(ValueError):
                TrendContextValidator.validate_trend_context(context)
    
    def test_validate_trend_context_topic_validation(self):
        """Test topic validation"""
        # Empty topic
        with pytest.raises(ValueError):
            TrendContextValidator.validate_trend_context({
                'topic': '',
                'relevance_score': 50
            })
        
        # Topic too long
        with pytest.raises(ValueError):
            TrendContextValidator.validate_trend_context({
                'topic': 'A' * 201,
                'relevance_score': 50
            })
    
    def test_is_valid_trend_context(self):
        """Test the is_valid_trend_context method"""
        valid_context = {
            'topic': 'Ethereum Update',
            'relevance_score': 75
        }
        
        invalid_context = {
            'topic': '',
            'relevance_score': 150
        }
        
        assert TrendContextValidator.is_valid_trend_context(valid_context) is True
        assert TrendContextValidator.is_valid_trend_context(invalid_context) is False