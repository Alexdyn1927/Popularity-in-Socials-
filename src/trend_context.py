from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

@dataclass
class TrendMetadata:
    """
    Represents metadata for a specific trend in the cryptocurrency market.
    
    Attributes:
        name (str): Name of the trend (e.g., cryptocurrency, topic)
        score (float): Relevance score of the trend (0-100)
        timestamp (datetime): Time when the trend was identified
        additional_info (Dict[str, Any]): Additional contextual information
    """
    name: str
    score: float
    timestamp: datetime
    additional_info: Optional[Dict[str, Any]] = None

class ITrendSource(ABC):
    """
    Abstract base class defining the interface for trend data sources.
    Provides a standardized way to fetch and process trend information.
    """
    
    @abstractmethod
    def fetch_trends(self, limit: Optional[int] = None) -> List[TrendMetadata]:
        """
        Fetch current trending topics or cryptocurrencies.
        
        Args:
            limit (Optional[int]): Maximum number of trends to retrieve
        
        Returns:
            List[TrendMetadata]: A list of trending topics with their metadata
        
        Raises:
            ConnectionError: If there's an issue connecting to the trend source
            ValueError: If the data cannot be processed
        """
        pass
    
    @abstractmethod
    def score_trend(self, trend: TrendMetadata) -> float:
        """
        Calculate the relevance score for a given trend.
        
        Args:
            trend (TrendMetadata): The trend to be scored
        
        Returns:
            float: A score representing the trend's relevance (0-100)
        """
        pass
    
    def filter_trends(self, 
                      trends: List[TrendMetadata], 
                      min_score: float = 50.0) -> List[TrendMetadata]:
        """
        Filter trends based on a minimum relevance score.
        
        Args:
            trends (List[TrendMetadata]): List of trends to filter
            min_score (float, optional): Minimum score for inclusion. Defaults to 50.0
        
        Returns:
            List[TrendMetadata]: Filtered list of trends meeting the score threshold
        """
        return [trend for trend in trends if trend.score >= min_score]

class TrendContext:
    """
    Manages and provides context for cryptocurrency market trends.
    Aggregates trends from multiple sources and provides contextual analysis.
    """
    
    def __init__(self, sources: List[ITrendSource]):
        """
        Initialize TrendContext with multiple trend sources.
        
        Args:
            sources (List[ITrendSource]): List of trend sources to use
        """
        self._sources = sources
        self._current_trends: List[TrendMetadata] = []
    
    def update_trends(self, min_score: float = 50.0) -> List[TrendMetadata]:
        """
        Update trends from all registered sources.
        
        Args:
            min_score (float, optional): Minimum score for trend inclusion. Defaults to 50.0
        
        Returns:
            List[TrendMetadata]: Filtered and scored trends
        """
        self._current_trends = []
        for source in self._sources:
            try:
                source_trends = source.fetch_trends()
                # Score and filter trends
                scored_trends = [
                    TrendMetadata(
                        name=trend.name, 
                        score=source.score_trend(trend), 
                        timestamp=trend.timestamp,
                        additional_info=trend.additional_info
                    ) for trend in source_trends
                ]
                self._current_trends.extend(
                    source.filter_trends(scored_trends, min_score)
                )
            except Exception as e:
                # Log the error, but continue processing other sources
                print(f"Error fetching trends from {source.__class__.__name__}: {e}")
        
        # Sort trends by score in descending order
        return sorted(self._current_trends, key=lambda x: x.score, reverse=True)
    
    @property
    def trends(self) -> List[TrendMetadata]:
        """
        Get the current trends.
        
        Returns:
            List[TrendMetadata]: Current trends
        """
        return self._current_trends