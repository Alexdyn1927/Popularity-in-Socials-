"""
Trend Context Module for Intelligent Content Generation

This module provides functionality to integrate trend data into content generation,
scoring and prioritizing trends for contextually relevant output.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

@dataclass
class TrendContext:
    """
    Represents a trend's context and relevance metrics.
    
    Attributes:
        keyword (str): The trending keyword or topic
        relevance_score (float): Numerical score indicating trend importance
        volume (int): Search or engagement volume
        timestamp (Optional[str]): Timestamp of trend data
    """
    keyword: str
    relevance_score: float
    volume: int
    timestamp: Optional[str] = None

class TrendContextProcessor:
    """
    Processes and scores trend data for content generation context.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize TrendContextProcessor.
        
        Args:
            logger (Optional[logging.Logger]): Custom logger for tracking operations
        """
        self.logger = logger or logging.getLogger(__name__)
    
    def process_trend_data(self, trend_data: Dict) -> List[TrendContext]:
        """
        Transform raw trend data into structured TrendContext objects.
        
        Args:
            trend_data (Dict): Raw trend data from trend sourcing
        
        Returns:
            List[TrendContext]: Processed and scored trend contexts
        """
        try:
            trend_contexts = []
            for keyword, data in trend_data.items():
                volume = max(data.values()) if data else 0
                relevance_score = self._calculate_relevance_score(volume)
                
                trend_contexts.append(TrendContext(
                    keyword=keyword,
                    relevance_score=relevance_score,
                    volume=volume
                ))
            
            return sorted(trend_contexts, key=lambda x: x.relevance_score, reverse=True)
        except Exception as e:
            self.logger.error(f"Error processing trend data: {e}")
            return []
    
    def _calculate_relevance_score(self, volume: int) -> float:
        """
        Calculate a relevance score based on trend volume.
        
        Args:
            volume (int): Trend volume
        
        Returns:
            float: Normalized relevance score between 0 and 1
        """
        # Simple logarithmic scaling to normalize relevance
        import math
        return min(1.0, math.log(volume + 1) / 10)