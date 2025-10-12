import logging
from typing import List, Dict, Optional
from ai.recommendation_engine import get_recommendation_engine
from app.services.recommendation_data_service import RecommendationDataService
from app.services.recommendation_cache import cached_recommendation

logger = logging.getLogger(__name__)


class RecommendationService:
    """
    Service for generating personalized recommendations
    Integrates LightFM collaborative filtering for movies and manga
    """
    
    def __init__(self):
        self.engine = get_recommendation_engine()
        self.data_service = RecommendationDataService()
    
    @cached_recommendation(ttl=3600)  # Cache for 1 hour
    async def get_movie_recommendations(
        self,
        user_id: str,
        n_recommendations: int = 10
    ) -> List[Dict]:
        """
        Get movie recommendations for a user
        
        Args:
            user_id: User ID to get recommendations for
            n_recommendations: Number of recommendations to return
        
        Returns:
            List of movie recommendation dictionaries
        """
        logger.info(f"Getting movie recommendations for user {user_id}")
        
        try:
            # Get recommendations from engine
            recommendations = self.engine.get_recommendations(
                user_id=user_id,
                content_type='movie',
                n_recommendations=n_recommendations
            )
            
            # Enrich with movie details
            enriched_recommendations = []
            for movie_id, score in recommendations:
                movie_details = await self.data_service.get_movie_by_id(movie_id)
                if movie_details:
                    movie_details['recommendation_score'] = score
                    enriched_recommendations.append(movie_details)
            
            return enriched_recommendations
        
        except Exception as e:
            logger.error(f"Error getting movie recommendations: {e}")
            # Fallback to popular movies
            return await self.data_service.get_popular_movies(n_recommendations)
    
    @cached_recommendation(ttl=3600)  # Cache for 1 hour
    async def get_manga_recommendations(
        self,
        user_id: str,
        n_recommendations: int = 10
    ) -> List[Dict]:
        """
        Get manga recommendations for a user
        
        Args:
            user_id: User ID to get recommendations for
            n_recommendations: Number of recommendations to return
        
        Returns:
            List of manga recommendation dictionaries
        """
        logger.info(f"Getting manga recommendations for user {user_id}")
        
        try:
            # Get recommendations from engine
            recommendations = self.engine.get_recommendations(
                user_id=user_id,
                content_type='manga',
                n_recommendations=n_recommendations
            )
            
            # Enrich with manga details
            enriched_recommendations = []
            for manga_id, score in recommendations:
                manga_details = await self.data_service.get_manga_by_id(manga_id)
                if manga_details:
                    manga_details['recommendation_score'] = score
                    enriched_recommendations.append(manga_details)
            
            return enriched_recommendations
        
        except Exception as e:
            logger.error(f"Error getting manga recommendations: {e}")
            # Fallback to popular manga
            return await self.data_service.get_popular_manga(n_recommendations)
    
    @cached_recommendation(ttl=3600)  # Cache for 1 hour
    async def get_anime_recommendations(
        self,
        user_id: str,
        n_recommendations: int = 10
    ) -> List[Dict]:
        """
        Get anime recommendations for a user
        
        Args:
            user_id: User ID to get recommendations for
            n_recommendations: Number of recommendations to return
        
        Returns:
            List of anime recommendation dictionaries
        """
        logger.info(f"Getting anime recommendations for user {user_id}")
        
        try:
            # Get recommendations from engine
            recommendations = self.engine.get_recommendations(
                user_id=user_id,
                content_type='anime',
                n_recommendations=n_recommendations
            )
            
            # Enrich with anime details
            enriched_recommendations = []
            for anime_id, score in recommendations:
                anime_details = await self.data_service.get_anime_by_id(anime_id)
                if anime_details:
                    anime_details['recommendation_score'] = score
                    enriched_recommendations.append(anime_details)
            
            return enriched_recommendations
        
        except Exception as e:
            logger.error(f"Error getting anime recommendations: {e}")
            return []
    
    async def train_movie_model(self) -> bool:
        """
        Train the movie recommendation model
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Training movie recommendation model")
        
        try:
            # Get all movie interactions
            interactions = await self.data_service.get_movie_interactions()
            
            if not interactions:
                logger.warning("No movie interactions found, skipping training")
                return False
            
            # Train model
            self.engine.train_model(
                interactions=interactions,
                content_type='movie',
                n_components=30,
                epochs=30
            )
            
            logger.info("Movie model training completed")
            return True
        
        except Exception as e:
            logger.error(f"Error training movie model: {e}")
            return False
    
    async def train_manga_model(self) -> bool:
        """
        Train the manga recommendation model
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Training manga recommendation model")
        
        try:
            # Get all manga interactions
            interactions = await self.data_service.get_manga_interactions()
            
            if not interactions:
                logger.warning("No manga interactions found, skipping training")
                return False
            
            # Train model
            self.engine.train_model(
                interactions=interactions,
                content_type='manga',
                n_components=30,
                epochs=30
            )
            
            logger.info("Manga model training completed")
            return True
        
        except Exception as e:
            logger.error(f"Error training manga model: {e}")
            return False
    
    async def train_anime_model(self) -> bool:
        """
        Train the anime recommendation model
        
        Returns:
            True if successful, False otherwise
        """
        logger.info("Training anime recommendation model")
        
        try:
            # Get all anime interactions
            interactions = await self.data_service.get_anime_interactions()
            
            if not interactions:
                logger.warning("No anime interactions found, skipping training")
                return False
            
            # Train model
            self.engine.train_model(
                interactions=interactions,
                content_type='anime',
                n_components=30,
                epochs=30
            )
            
            logger.info("Anime model training completed")
            return True
        
        except Exception as e:
            logger.error(f"Error training anime model: {e}")
            return False
    
    async def train_all_models(self) -> Dict[str, bool]:
        """
        Train all recommendation models
        
        Returns:
            Dictionary with training results for each model
        """
        logger.info("Training all recommendation models")
        
        results = {
            'movie': await self.train_movie_model(),
            'manga': await self.train_manga_model(),
            'anime': await self.train_anime_model(),
        }
        
        logger.info(f"Model training results: {results}")
        return results


# Global instance
_recommendation_service = None


def get_recommendation_service() -> RecommendationService:
    """
    Get or create the global recommendation service instance
    """
    global _recommendation_service
    if _recommendation_service is None:
        _recommendation_service = RecommendationService()
    return _recommendation_service
