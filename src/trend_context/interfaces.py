from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum, auto

class TrendCategory(Enum):
    PRICE_MOVEMENT = auto()
    MARKET_SENTIMENT = auto()
    TECHNOLOGY_UPDATE = auto()
    REGULATORY_NEWS = auto()
    SOCIAL_MEDIA_BUZZ = auto()

@dataclass
class TrendContext:
    """
    Represents a comprehensive trend context for cryptocurrency content generation.
    
    Attributes:
        category (TrendCategory): The broad category of the trend
        score (float): Relevance/importance score of the trend (0-100)
        keywords (List[str]): Associated keywords for content generation
        metadata (Dict[str, Any]): Additional contextual information
    """
    category: TrendCategory
    score: float
    keywords: List[str]
    metadata: Dict[str, Any] = None

class TrendContextInjectionInterface(ABC):
    """
    Abstract base class defining the interface for trend context injection.
    Provides methods for sourcing, processing, and scoring cryptocurrency trends.
    """
    
    @abstractmethod
    def source_trends(self) -> List[TrendContext]:
        """
        Source and retrieve current cryptocurrency trends.
        
        Returns:
            List[TrendContext]: A list of discovered trend contexts
        
        Raises:
            TrendSourceError: If trend sourcing fails
        """
        pass
    
    @abstractmethod
    def filter_trends(
        self, 
        trends: List[TrendContext], 
        min_score: float = 50.0, 
        categories: Optional[List[TrendCategory]] = None
    ) -> List[TrendContext]:
        """
        Filter trends based on score and optional categories.
        
        Args:
            trends (List[TrendContext]): Input list of trends
            min_score (float, optional): Minimum trend score to include. Defaults to 50.0
            categories (Optional[List[TrendCategory]], optional): Categories to filter. Defaults to None.
        
        Returns:
            List[TrendContext]: Filtered list of trends
        """
        pass
    
    @abstractmethod
    def inject_context(
        self, 
        trend: TrendContext, 
        content_template: str
    ) -> str:
        """
        Inject trend context into a content template.
        
        Args:
            trend (TrendContext): The trend context to inject
            content_template (str): Template string for content generation
        
        Returns:
            str: Content with trend context injected
        """
        pass

class TrendSourceError(Exception):
    """
    Custom exception for trend sourcing failures.
    """
    pass

class TrendContextValidationError(Exception):
    """
    Custom exception for trend context validation failures.
    """
    pass