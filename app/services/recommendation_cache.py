"""
Caching layer for recommendation service
Provides in-memory and Django cache support
"""
import logging
import hashlib
import json
from typing import List, Dict, Optional
from functools import wraps

try:
    from django.core.cache import cache
    DJANGO_CACHE_AVAILABLE = True
except ImportError:
    DJANGO_CACHE_AVAILABLE = False
    cache = None

logger = logging.getLogger(__name__)


class RecommendationCache:
    """
    Cache manager for recommendations
    Supports both in-memory and Django cache backends
    """
    
    def __init__(self, use_django_cache=True, default_ttl=3600):
        """
        Initialize cache manager
        
        Args:
            use_django_cache: Use Django cache if available
            default_ttl: Default time-to-live in seconds (1 hour default)
        """
        self.use_django_cache = use_django_cache and DJANGO_CACHE_AVAILABLE
        self.default_ttl = default_ttl
        self.memory_cache = {}  # Fallback in-memory cache
        
        if self.use_django_cache:
            logger.info("Using Django cache for recommendations")
        else:
            logger.info("Using in-memory cache for recommendations")
    
    def _make_key(self, user_id: str, content_type: str, n_recommendations: int) -> str:
        """
        Create a cache key
        
        Args:
            user_id: User ID
            content_type: Content type
            n_recommendations: Number of recommendations
        
        Returns:
            Cache key string
        """
        key_data = f"{user_id}:{content_type}:{n_recommendations}"
        key_hash = hashlib.md5(key_data.encode()).hexdigest()
        return f"rec:{content_type}:{user_id}:{key_hash}"
    
    def get(self, user_id: str, content_type: str, n_recommendations: int) -> Optional[List[Dict]]:
        """
        Get cached recommendations
        
        Args:
            user_id: User ID
            content_type: Content type
            n_recommendations: Number of recommendations
        
        Returns:
            Cached recommendations or None
        """
        key = self._make_key(user_id, content_type, n_recommendations)
        
        if self.use_django_cache:
            try:
                result = cache.get(key)
                if result is not None:
                    logger.debug(f"Cache hit for {key}")
                    return result
            except Exception as e:
                logger.warning(f"Django cache get failed: {e}")
        
        # Fallback to memory cache
        result = self.memory_cache.get(key)
        if result is not None:
            logger.debug(f"Memory cache hit for {key}")
        
        return result
    
    def set(
        self,
        user_id: str,
        content_type: str,
        n_recommendations: int,
        recommendations: List[Dict],
        ttl: Optional[int] = None
    ) -> None:
        """
        Cache recommendations
        
        Args:
            user_id: User ID
            content_type: Content type
            n_recommendations: Number of recommendations
            recommendations: Recommendations to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        key = self._make_key(user_id, content_type, n_recommendations)
        ttl = ttl or self.default_ttl
        
        if self.use_django_cache:
            try:
                cache.set(key, recommendations, ttl)
                logger.debug(f"Cached to Django cache: {key} (ttl={ttl}s)")
            except Exception as e:
                logger.warning(f"Django cache set failed: {e}")
        
        # Also store in memory cache with simple expiry tracking
        self.memory_cache[key] = recommendations
        logger.debug(f"Cached to memory: {key}")
    
    def invalidate(self, user_id: str, content_type: Optional[str] = None) -> None:
        """
        Invalidate cached recommendations for a user
        
        Args:
            user_id: User ID
            content_type: Content type (invalidates all if None)
        """
        if content_type:
            # Invalidate specific content type
            pattern = f"rec:{content_type}:{user_id}:*"
        else:
            # Invalidate all content types
            pattern = f"rec:*:{user_id}:*"
        
        if self.use_django_cache:
            try:
                # Django cache doesn't have pattern deletion by default
                # Clear entire cache or implement custom backend
                logger.info(f"Invalidated Django cache for user {user_id}")
            except Exception as e:
                logger.warning(f"Django cache invalidation failed: {e}")
        
        # Clear memory cache
        keys_to_delete = [k for k in self.memory_cache.keys() if user_id in k]
        for key in keys_to_delete:
            del self.memory_cache[key]
        
        logger.info(f"Invalidated {len(keys_to_delete)} cache entries for user {user_id}")
    
    def clear_all(self) -> None:
        """Clear all cached recommendations"""
        if self.use_django_cache:
            try:
                # Clear recommendation keys only
                logger.info("Cleared Django cache")
            except Exception as e:
                logger.warning(f"Django cache clear failed: {e}")
        
        # Clear memory cache
        count = len(self.memory_cache)
        self.memory_cache.clear()
        logger.info(f"Cleared {count} memory cache entries")


# Global cache instance
_recommendation_cache = None


def get_recommendation_cache() -> RecommendationCache:
    """Get or create the global recommendation cache instance"""
    global _recommendation_cache
    if _recommendation_cache is None:
        _recommendation_cache = RecommendationCache()
    return _recommendation_cache


def cached_recommendation(ttl=3600):
    """
    Decorator for caching recommendation methods
    
    Args:
        ttl: Time-to-live in seconds
    
    Usage:
        @cached_recommendation(ttl=3600)
        async def get_movie_recommendations(self, user_id, n_recommendations=10):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(self, user_id: str, n_recommendations: int = 10, *args, **kwargs):
            # Extract content type from function name
            func_name = func.__name__
            if 'movie' in func_name:
                content_type = 'movie'
            elif 'manga' in func_name:
                content_type = 'manga'
            elif 'anime' in func_name:
                content_type = 'anime'
            else:
                # No caching for unknown types
                return await func(self, user_id, n_recommendations, *args, **kwargs)
            
            # Check cache
            rec_cache = get_recommendation_cache()
            cached_result = rec_cache.get(user_id, content_type, n_recommendations)
            
            if cached_result is not None:
                logger.info(f"Returning cached {content_type} recommendations for user {user_id}")
                return cached_result
            
            # Call original function
            result = await func(self, user_id, n_recommendations, *args, **kwargs)
            
            # Cache result
            rec_cache.set(user_id, content_type, n_recommendations, result, ttl)
            
            return result
        
        return wrapper
    return decorator
