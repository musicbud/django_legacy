"""
Service for preparing recommendation training data from Neo4j
Extracts user-item interactions for movies and manga
"""
import logging
from typing import List, Tuple
from app.db_models.parent_user import ParentUser
from app.db_models.imdb.imdb_user import ImdbUser
from app.db_models.imdb.imdb_movie import ImdbMovie
from app.db_models.mal.mal_user import MalUser
from app.db_models.mal.mal_anime import Anime
from app.db_models.mal.mal_manga import Manga

logger = logging.getLogger(__name__)


class RecommendationDataService:
    """
    Service for extracting and preparing recommendation data from Neo4j
    """
    
    @staticmethod
    async def get_movie_interactions() -> List[Tuple[str, str, float]]:
        """
        Extract movie interactions from Neo4j
        
        Returns:
            List of (user_id, movie_id, rating) tuples
        """
        logger.info("Extracting movie interactions from Neo4j")
        interactions = []
        
        try:
            # Get all IMDB users
            imdb_users = await ImdbUser.nodes.all()
            
            for user in imdb_users:
                user_id = str(user.user_id)
                
                # Get liked movies (implicit positive feedback)
                liked_movies = await user.likes_movies.all()
                for movie in liked_movies:
                    interactions.append((user_id, str(movie.imdb_id), 5.0))
                
                # Get watched movies (implicit feedback)
                watched_movies = await user.watched_movies.all()
                for movie in watched_movies:
                    interactions.append((user_id, str(movie.imdb_id), 3.0))
                
                # Get movies in watchlist (weak positive signal)
                watchlist_movies = await user.watchlist_movies.all()
                for movie in watchlist_movies:
                    interactions.append((user_id, str(movie.imdb_id), 2.0))
            
            logger.info(f"Extracted {len(interactions)} movie interactions")
            
        except Exception as e:
            logger.error(f"Error extracting movie interactions: {e}")
        
        return interactions
    
    @staticmethod
    async def get_manga_interactions() -> List[Tuple[str, str, float]]:
        """
        Extract manga interactions from Neo4j
        
        Returns:
            List of (user_id, manga_id, rating) tuples
        """
        logger.info("Extracting manga interactions from Neo4j")
        interactions = []
        
        try:
            # Get all MAL users
            mal_users = await MalUser.nodes.all()
            
            for user in mal_users:
                user_id = str(user.user_id)
                
                # Get top manga (implicit positive feedback)
                top_manga = await user.top_manga.all()
                for manga in top_manga:
                    interactions.append((user_id, str(manga.manga_id), 5.0))
            
            logger.info(f"Extracted {len(interactions)} manga interactions")
            
        except Exception as e:
            logger.error(f"Error extracting manga interactions: {e}")
        
        return interactions
    
    @staticmethod
    async def get_anime_interactions() -> List[Tuple[str, str, float]]:
        """
        Extract anime interactions from Neo4j
        
        Returns:
            List of (user_id, anime_id, rating) tuples
        """
        logger.info("Extracting anime interactions from Neo4j")
        interactions = []
        
        try:
            # Get all MAL users
            mal_users = await MalUser.nodes.all()
            
            for user in mal_users:
                user_id = str(user.user_id)
                
                # Get top anime (implicit positive feedback)
                top_anime = await user.top_anime.all()
                for anime in top_anime:
                    # Use score if available, otherwise default to 5.0
                    rating = float(anime.score) if hasattr(anime, 'score') and anime.score else 5.0
                    interactions.append((user_id, str(anime.anime_id), rating))
            
            logger.info(f"Extracted {len(interactions)} anime interactions")
            
        except Exception as e:
            logger.error(f"Error extracting anime interactions: {e}")
        
        return interactions
    
    @staticmethod
    async def get_user_movie_interactions(user_id: str) -> List[Tuple[str, str, float]]:
        """
        Get movie interactions for a specific user
        
        Args:
            user_id: User ID to get interactions for
        
        Returns:
            List of (user_id, movie_id, rating) tuples
        """
        interactions = []
        
        try:
            # Try to find IMDB user
            imdb_user = await ImdbUser.nodes.get_or_none(user_id=user_id)
            
            if imdb_user:
                # Get liked movies
                liked_movies = await imdb_user.likes_movies.all()
                for movie in liked_movies:
                    interactions.append((user_id, str(movie.imdb_id), 5.0))
                
                # Get watched movies
                watched_movies = await imdb_user.watched_movies.all()
                for movie in watched_movies:
                    interactions.append((user_id, str(movie.imdb_id), 3.0))
        
        except Exception as e:
            logger.error(f"Error getting user movie interactions: {e}")
        
        return interactions
    
    @staticmethod
    async def get_user_manga_interactions(user_id: str) -> List[Tuple[str, str, float]]:
        """
        Get manga interactions for a specific user
        
        Args:
            user_id: User ID to get interactions for
        
        Returns:
            List of (user_id, manga_id, rating) tuples
        """
        interactions = []
        
        try:
            # Try to find MAL user
            mal_user = await MalUser.nodes.get_or_none(user_id=user_id)
            
            if mal_user:
                # Get top manga
                top_manga = await mal_user.top_manga.all()
                for manga in top_manga:
                    interactions.append((user_id, str(manga.manga_id), 5.0))
        
        except Exception as e:
            logger.error(f"Error getting user manga interactions: {e}")
        
        return interactions
    
    @staticmethod
    async def get_movie_by_id(movie_id: str) -> dict:
        """
        Get movie details by ID
        
        Args:
            movie_id: Movie ID
        
        Returns:
            Dictionary with movie details
        """
        try:
            movie = await ImdbMovie.nodes.get_or_none(imdb_id=movie_id)
            if movie:
                return {
                    'id': movie.imdb_id,
                    'title': movie.title,
                    'year': movie.year,
                    'rating': movie.rating,
                    'genres': movie.genres,
                    'plot': movie.plot,
                    'director': movie.director,
                }
        except Exception as e:
            logger.error(f"Error getting movie by ID: {e}")
        
        return None
    
    @staticmethod
    async def get_manga_by_id(manga_id: str) -> dict:
        """
        Get manga details by ID
        
        Args:
            manga_id: Manga ID
        
        Returns:
            Dictionary with manga details
        """
        try:
            manga = await Manga.nodes.get_or_none(manga_id=int(manga_id))
            if manga:
                return await manga.serialize()
        except Exception as e:
            logger.error(f"Error getting manga by ID: {e}")
        
        return None
    
    @staticmethod
    async def get_anime_by_id(anime_id: str) -> dict:
        """
        Get anime details by ID
        
        Args:
            anime_id: Anime ID
        
        Returns:
            Dictionary with anime details
        """
        try:
            anime = await Anime.nodes.get_or_none(anime_id=int(anime_id))
            if anime:
                return await anime.serialize()
        except Exception as e:
            logger.error(f"Error getting anime by ID: {e}")
        
        return None
    
    @staticmethod
    async def get_popular_movies(limit: int = 10) -> List[dict]:
        """
        Get popular movies based on interaction count
        
        Args:
            limit: Number of movies to return
        
        Returns:
            List of movie dictionaries
        """
        try:
            # Query to get movies with most likes
            query = '''
            MATCH (m:ImdbMovie)<-[:LIKES]-(u:ImdbUser)
            WITH m, count(u) as likes
            ORDER BY likes DESC
            LIMIT $limit
            RETURN m
            '''
            
            results, _ = await ImdbMovie.cypher(query, {'limit': limit})
            
            movies = []
            for row in results:
                movie_node = ImdbMovie.inflate(row[0])
                movies.append({
                    'id': movie_node.imdb_id,
                    'title': movie_node.title,
                    'year': movie_node.year,
                    'rating': movie_node.rating,
                    'genres': movie_node.genres,
                })
            
            return movies
        
        except Exception as e:
            logger.error(f"Error getting popular movies: {e}")
            return []
    
    @staticmethod
    async def get_popular_manga(limit: int = 10) -> List[dict]:
        """
        Get popular manga based on interaction count
        
        Args:
            limit: Number of manga to return
        
        Returns:
            List of manga dictionaries
        """
        try:
            # Query to get manga with most users
            query = '''
            MATCH (m:Manga)<-[:TOP_MANGA]-(u:MalUser)
            WITH m, count(u) as users
            ORDER BY users DESC
            LIMIT $limit
            RETURN m
            '''
            
            results, _ = await Manga.cypher(query, {'limit': limit})
            
            manga_list = []
            for row in results:
                manga_node = Manga.inflate(row[0])
                manga_list.append(await manga_node.serialize())
            
            return manga_list
        
        except Exception as e:
            logger.error(f"Error getting popular manga: {e}")
            return []
