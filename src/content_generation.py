"""
Content Generation Module with Trend Context Integration

Generates contextually relevant cryptocurrency content
using trend insights and advanced language processing.
"""

from typing import List, Optional, Dict
import logging
from src.trend_context import TrendContext, TrendContextProcessor
from src.trend_sourcing import TrendSourcing

class ContentGenerator:
    """
    Advanced content generation system that incorporates trend context.
    """
    
    def __init__(
        self, 
        trend_sourcer: Optional[TrendSourcing] = None,
        trend_processor: Optional[TrendContextProcessor] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize ContentGenerator with optional dependencies.
        
        Args:
            trend_sourcer (Optional[TrendSourcing]): Trend sourcing service
            trend_processor (Optional[TrendContextProcessor]): Trend context processor
            logger (Optional[logging.Logger]): Custom logger
        """
        self.trend_sourcer = trend_sourcer or TrendSourcing()
        self.trend_processor = trend_processor or TrendContextProcessor()
        self.logger = logger or logging.getLogger(__name__)
    
    def generate_content(
        self, 
        keywords: List[str],
        content_type: str = 'article',
        max_trends: int = 3
    ) -> Dict[str, str]:
        """
        Generate content using trend-infused context.
        
        Args:
            keywords (List[str]): Base keywords for content generation
            content_type (str): Type of content to generate
            max_trends (int): Maximum number of trends to incorporate
        
        Returns:
            Dict[str, str]: Generated content with metadata
        """
        try:
            # Source trends
            trend_data = self.trend_sourcer.get_google_trends(keywords)
            
            # Process trend context
            trend_contexts = self.trend_processor.process_trend_data(trend_data)
            top_trends = trend_contexts[:max_trends]
            
            # Content generation logic (simplified for demonstration)
            content = self._generate_content_from_trends(top_trends, content_type)
            
            return {
                'content': content,
                'trends_used': [trend.keyword for trend in top_trends]
            }
        
        except Exception as e:
            self.logger.error(f"Content generation error: {e}")
            return {'content': '', 'trends_used': []}
    
    def _generate_content_from_trends(
        self, 
        trends: List[TrendContext], 
        content_type: str
    ) -> str:
        """
        Generate content based on trend contexts.
        
        Args:
            trends (List[TrendContext]): Processed trend contexts
            content_type (str): Type of content to generate
        
        Returns:
            str: Generated content
        """
        # Simplified content generation - would be replaced with advanced NLP
        if not trends:
            return "No trending topics available for content generation."
        
        trend_keywords = [trend.keyword for trend in trends]
        base_content = f"Exploring top crypto trends: {', '.join(trend_keywords)}"
        
        if content_type == 'article':
            return f"{base_content}\n\nFull article generation requires advanced NLP processing."
        elif content_type == 'summary':
            return f"Summary of {len(trend_keywords)} top crypto trends."
        
        return base_content