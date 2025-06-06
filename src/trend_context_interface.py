from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import List, Dict, Optional, Any

class TrendCategory(Enum):
    """Enumeration of cryptocurrency trend categories."""
    PRICE_MOVEMENT = auto()
    TECHNOLOGY_INNOVATION = auto()
    REGULATORY_NEWS = auto()
    MARKET_SENTIMENT = auto()
    ADOPTION_TREND = auto()

@dataclass
class TrendContext:
    """
    Data class representing a comprehensive trend context for cryptocurrency content.
    
    Attributes:
        category (TrendCategory): The broad category of the trend
        relevance_score (float): Numerical score indicating trend importance (0-100)
        keywords (List[str]): Significant keywords associated with the trend
        source (str): Origin of the trend data
        timestamp (datetime): When the trend was captured
        additional_metadata (Dict[str, Any]): Flexible metadata storage
    """
    category: TrendCategory
    relevance_score: float
    keywords: List[str]
    source: str
    timestamp: datetime
    additional_metadata: Optional[Dict[str, Any]] = None

class TrendContextInjectionInterface(ABC):
    """
    Abstract base class defining the interface for trend context injection.
    
    This interface provides a standardized method for retrieving and processing
    cryptocurrency trend contexts for intelligent content generation.
    """
    
    @abstractmethod
    def fetch_trends(self, limit: Optional[int] = None) -> List[TrendContext]:
        """
        Fetch current cryptocurrency trends.
        
        Args:
            limit (Optional[int]): Maximum number of trends to retrieve. 
                                   Defaults to None (retrieve all available trends)
        
        Returns:
            List[TrendContext]: A list of trend contexts sorted by relevance
        
        Raises:
            ConnectionError: If unable to fetch trends from sources
            ValueError: If invalid parameters are provided
        """
        pass
    
    @abstractmethod
    def score_trend_relevance(self, trend: TrendContext) -> float:
        """
        Calculate the relevance score for a given trend.
        
        Args:
            trend (TrendContext): The trend to score
        
        Returns:
            float: A numerical score representing trend relevance (0-100)
        """
        pass
    
    @abstractmethod
    def filter_trends(
        self, 
        trends: List[TrendContext], 
        categories: Optional[List[TrendCategory]] = None,
        min_relevance: float = 50.0
    ) -> List[TrendContext]:
        """
        Filter trends based on categories and minimum relevance score.
        
        Args:
            trends (List[TrendContext]): List of trends to filter
            categories (Optional[List[TrendCategory]]): Categories to include
            min_relevance (float): Minimum relevance score to retain a trend
        
        Returns:
            List[TrendContext]: Filtered list of trends
        """
        pass