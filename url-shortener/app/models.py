"""Thread-safe in-memory data models for URL shortener service"""

import threading
from datetime import datetime
from typing import Dict, Optional, NamedTuple
from dataclasses import dataclass


@dataclass
class URLMapping:
    """Data class representing a URL mapping with metadata"""
    original_url: str
    short_code: str
    click_count: int
    created_at: datetime
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'original_url': self.original_url,
            'short_code': self.short_code,
            'click_count': self.click_count,
            'created_at': self.created_at.isoformat()
        }


class ThreadSafeURLStore:
    """Thread-safe in-memory storage for URL mappings"""
    
    def __init__(self):
        """Initialize the thread-safe URL store"""
        self._mappings: Dict[str, URLMapping] = {}  # short_code -> URLMapping
        self._reverse_mappings: Dict[str, str] = {}  # original_url -> short_code
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def store_mapping(self, short_code: str, original_url: str) -> URLMapping:
        """Store a new URL mapping.
        
        Args:
            short_code: The generated short code
            original_url: The original URL to map
            
        Returns:
            URLMapping object that was stored
            
        Raises:
            ValueError: If short_code already exists
        """
        with self._lock:
            if short_code in self._mappings:
                raise ValueError(f"Short code '{short_code}' already exists")
            
            mapping = URLMapping(
                original_url=original_url,
                short_code=short_code,
                click_count=0,
                created_at=datetime.utcnow()
            )
            
            self._mappings[short_code] = mapping
            self._reverse_mappings[original_url] = short_code
            
            return mapping
    
    def get_mapping(self, short_code: str) -> Optional[URLMapping]:
        """Get URL mapping by short code.
        
        Args:
            short_code: The short code to look up
            
        Returns:
            URLMapping if found, None otherwise
        """
        with self._lock:
            return self._mappings.get(short_code)
    
    def increment_click_count(self, short_code: str) -> bool:
        """Increment click count for a short code.
        
        Args:
            short_code: The short code to increment
            
        Returns:
            True if incremented successfully, False if short_code not found
        """
        with self._lock:
            if short_code in self._mappings:
                self._mappings[short_code].click_count += 1
                return True
            return False
    
    def exists(self, short_code: str) -> bool:
        """Check if a short code exists.
        
        Args:
            short_code: The short code to check
            
        Returns:
            True if exists, False otherwise
        """
        with self._lock:
            return short_code in self._mappings
    
    def url_already_shortened(self, original_url: str) -> Optional[str]:
        """Check if a URL has already been shortened.
        
        Args:
            original_url: The original URL to check
            
        Returns:
            Existing short code if URL was already shortened, None otherwise
        """
        with self._lock:
            return self._reverse_mappings.get(original_url)
    
    def get_stats(self) -> Dict:
        """Get overall statistics about the URL store.
        
        Returns:
            Dictionary with statistics
        """
        with self._lock:
            total_urls = len(self._mappings)
            total_clicks = sum(mapping.click_count for mapping in self._mappings.values())
            
            return {
                'total_urls': total_urls,
                'total_clicks': total_clicks,
                'average_clicks': total_clicks / total_urls if total_urls > 0 else 0
            }
    
    def clear(self) -> None:
        """Clear all mappings (useful for testing)."""
        with self._lock:
            self._mappings.clear()
            self._reverse_mappings.clear()


# Global thread-safe URL store instance
url_store = ThreadSafeURLStore()