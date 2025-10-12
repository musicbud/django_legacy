"""
Public/Guest-accessible API endpoints
These endpoints don't require authentication and are rate-limited
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from django.core.cache import cache
import logging

from app.services.recommendation_service import get_recommendation_service
from app.services.recommendation_data_service import RecommendationDataService

logger = logging.getLogger(__name__)


class GuestRateThrottle(AnonRateThrottle):
    """Rate limiting for guest/anonymous users"""
    rate = '100/hour'  # 100 requests per hour for guests


class PublicDiscoverView(APIView):
    """
    Public discover endpoint - returns popular content for guest users
    No authentication required
    """
    permission_classes = [AllowAny]
    throttle_classes = []  # Disable throttling for now
    
    def get(self, request):
        """Get public discovery content"""
        try:
            # Check cache first (1 hour)
            # Temporarily disabled due to Redis auth issues
            # cache_key = 'public_discover_content'
            # cached_data = cache.get(cache_key)
            # 
            # if cached_data:
            #     logger.info("Returning cached public discover content")
            #     return Response(cached_data, status=status.HTTP_200_OK)
            
            data_service = RecommendationDataService()
            
            # Get popular items (no personalization for guests)
            response_data = {
                'success': True,
                'message': 'Public discover content fetched successfully',
                'data': {
                    'trending_tracks': [],
                    'popular_artists': [],
                    'popular_movies': [],
                    'popular_manga': [],
                    'popular_anime': [],
                    'genres': self._get_popular_genres(),
                }
            }
            
            # Try to get popular movies (async call)
            try:
                import asyncio
                movies = asyncio.run(data_service.get_popular_movies(limit=10))
                response_data['data']['popular_movies'] = movies
            except Exception as e:
                logger.error(f"Error fetching popular movies: {e}")
            
            # Try to get popular manga
            try:
                import asyncio
                manga = asyncio.run(data_service.get_popular_manga(limit=10))
                response_data['data']['popular_manga'] = manga
            except Exception as e:
                logger.error(f"Error fetching popular manga: {e}")
            
            # Cache for 1 hour
            # Temporarily disabled due to Redis auth issues
            # cache.set(cache_key, response_data, 3600)
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error in PublicDiscoverView: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error fetching discover content: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_popular_genres(self):
        """Get popular genres list"""
        return [
            {'name': 'Pop', 'color': '#FF6B6B'},
            {'name': 'Rock', 'color': '#4ECDC4'},
            {'name': 'Hip Hop', 'color': '#FFE66D'},
            {'name': 'Electronic', 'color': '#95E1D3'},
            {'name': 'Jazz', 'color': '#AA96DA'},
            {'name': 'Classical', 'color': '#8B4513'},
        ]


class PublicTrendingView(APIView):
    """
    Public trending content endpoint
    Returns trending tracks, artists, and other content
    """
    permission_classes = [AllowAny]
    throttle_classes = []  # Disable throttling for now
    
    def get(self, request):
        """Get trending content"""
        try:
            content_type = request.query_params.get('type', 'all')
            
            # Check cache
            # Temporarily disabled due to Redis auth issues
            # cache_key = f'public_trending_{content_type}'
            # cached_data = cache.get(cache_key)
            # 
            # if cached_data:
            #     return Response(cached_data, status=status.HTTP_200_OK)
            
            response_data = {
                'success': True,
                'message': 'Trending content fetched successfully',
                'data': {}
            }
            
            if content_type in ['all', 'tracks']:
                response_data['data']['tracks'] = self._get_mock_trending_tracks()
            
            if content_type in ['all', 'artists']:
                response_data['data']['artists'] = self._get_mock_trending_artists()
            
            if content_type in ['all', 'movies']:
                response_data['data']['movies'] = self._get_mock_trending_movies()
            
            if content_type in ['all', 'manga']:
                response_data['data']['manga'] = self._get_mock_trending_manga()
            
            # Cache for 30 minutes
            # Temporarily disabled due to Redis auth issues
            # cache.set(cache_key, response_data, 1800)
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error in PublicTrendingView: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error fetching trending content: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_mock_trending_tracks(self):
        """Get mock trending tracks"""
        return [
            {
                'id': 'track_1',
                'name': 'Anti-Hero',
                'artist': 'Taylor Swift',
                'album': 'Midnights',
                'duration': '3:20',
                'popularity': 95,
                'image': None,
            },
            {
                'id': 'track_2',
                'name': 'Blinding Lights',
                'artist': 'The Weeknd',
                'album': 'After Hours',
                'duration': '3:22',
                'popularity': 92,
                'image': None,
            },
            {
                'id': 'track_3',
                'name': 'What Was I Made For?',
                'artist': 'Billie Eilish',
                'album': 'Barbie Soundtrack',
                'duration': '3:42',
                'popularity': 89,
                'image': None,
            },
        ]
    
    def _get_mock_trending_artists(self):
        """Get mock trending artists"""
        return [
            {
                'id': 'artist_1',
                'name': 'Taylor Swift',
                'genre': 'Pop',
                'followers': 1500000,
                'popularity': 95,
                'image': None,
            },
            {
                'id': 'artist_2',
                'name': 'The Weeknd',
                'genre': 'R&B',
                'followers': 1200000,
                'popularity': 92,
                'image': None,
            },
            {
                'id': 'artist_3',
                'name': 'Billie Eilish',
                'genre': 'Alternative',
                'followers': 1000000,
                'popularity': 89,
                'image': None,
            },
        ]
    
    def _get_mock_trending_movies(self):
        """Get mock trending movies"""
        return [
            {
                'id': 'movie_1',
                'title': 'Sample Movie 1',
                'year': 2024,
                'rating': 8.5,
                'genres': ['Action', 'Adventure'],
            },
            {
                'id': 'movie_2',
                'title': 'Sample Movie 2',
                'year': 2024,
                'rating': 8.2,
                'genres': ['Drama', 'Thriller'],
            },
        ]
    
    def _get_mock_trending_manga(self):
        """Get mock trending manga"""
        return [
            {
                'id': 'manga_1',
                'title': 'Sample Manga 1',
                'chapters': 150,
                'rating': 9.0,
                'genres': ['Action', 'Fantasy'],
            },
            {
                'id': 'manga_2',
                'title': 'Sample Manga 2',
                'chapters': 200,
                'rating': 8.8,
                'genres': ['Romance', 'Drama'],
            },
        ]


class PublicRecommendationsView(APIView):
    """
    Public recommendations endpoint
    Returns popular items (not personalized) for guest users
    """
    permission_classes = [AllowAny]
    throttle_classes = []  # Disable throttling for now
    
    def get(self, request):
        """Get public recommendations (popular items)"""
        try:
            rec_type = request.query_params.get('type', 'all')
            
            # Check cache
            # Temporarily disabled due to Redis auth issues
            # cache_key = f'public_recommendations_{rec_type}'
            # cached_data = cache.get(cache_key)
            # 
            # if cached_data:
            #     return Response(cached_data, status=status.HTTP_200_OK)
            
            data_service = RecommendationDataService()
            
            response_data = {
                'success': True,
                'message': 'Public recommendations fetched successfully',
                'data': {},
                'is_personalized': False,  # Indicate these are not personalized
            }
            
            # Get popular items based on type
            if rec_type in ['all', 'movies']:
                try:
                    import asyncio
                    movies = asyncio.run(data_service.get_popular_movies(limit=20))
                    response_data['data']['movies'] = movies
                except Exception as e:
                    logger.error(f"Error fetching popular movies: {e}")
                    response_data['data']['movies'] = []
            
            if rec_type in ['all', 'manga']:
                try:
                    import asyncio
                    manga = asyncio.run(data_service.get_popular_manga(limit=20))
                    response_data['data']['manga'] = manga
                except Exception as e:
                    logger.error(f"Error fetching popular manga: {e}")
                    response_data['data']['manga'] = []
            
            # Cache for 1 hour
            # Temporarily disabled due to Redis auth issues
            # cache.set(cache_key, response_data, 3600)
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error in PublicRecommendationsView: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error fetching recommendations: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PublicGenresView(APIView):
    """
    Public genres endpoint
    Returns available genres/categories
    """
    permission_classes = [AllowAny]
    throttle_classes = []  # Disable throttling for now
    
    def get(self, request):
        """Get available genres"""
        try:
            genres = {
                'music': [
                    {'id': 'pop', 'name': 'Pop', 'color': '#FF6B6B'},
                    {'id': 'rock', 'name': 'Rock', 'color': '#4ECDC4'},
                    {'id': 'hip_hop', 'name': 'Hip Hop', 'color': '#FFE66D'},
                    {'id': 'electronic', 'name': 'Electronic', 'color': '#95E1D3'},
                    {'id': 'jazz', 'name': 'Jazz', 'color': '#AA96DA'},
                    {'id': 'classical', 'name': 'Classical', 'color': '#8B4513'},
                    {'id': 'country', 'name': 'Country', 'color': '#DEB887'},
                    {'id': 'rb', 'name': 'R&B', 'color': '#9370DB'},
                ],
                'movies': [
                    {'id': 'action', 'name': 'Action', 'color': '#FF4500'},
                    {'id': 'comedy', 'name': 'Comedy', 'color': '#FFD700'},
                    {'id': 'drama', 'name': 'Drama', 'color': '#4169E1'},
                    {'id': 'thriller', 'name': 'Thriller', 'color': '#8B0000'},
                    {'id': 'sci_fi', 'name': 'Sci-Fi', 'color': '#00CED1'},
                    {'id': 'horror', 'name': 'Horror', 'color': '#800080'},
                ],
                'anime': [
                    {'id': 'shonen', 'name': 'Shonen', 'color': '#FF6347'},
                    {'id': 'shojo', 'name': 'Shojo', 'color': '#FFB6C1'},
                    {'id': 'seinen', 'name': 'Seinen', 'color': '#4682B4'},
                    {'id': 'mecha', 'name': 'Mecha', 'color': '#708090'},
                    {'id': 'isekai', 'name': 'Isekai', 'color': '#9370DB'},
                ],
            }
            
            return Response({
                'success': True,
                'message': 'Genres fetched successfully',
                'data': genres
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error in PublicGenresView: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error fetching genres: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PublicContentDetailView(APIView):
    """
    Public content detail endpoint
    Returns detailed information about a specific content item
    """
    permission_classes = [AllowAny]
    throttle_classes = []  # Disable throttling for now
    
    def get(self, request, content_type, content_id):
        """Get content details by type and ID"""
        try:
            # Validate content type
            valid_types = ['movie', 'manga', 'anime', 'track', 'artist', 'album']
            if content_type not in valid_types:
                return Response({
                    'success': False,
                    'message': f'Invalid content type. Must be one of: {valid_types}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get content details based on type
            if content_type == 'movie':
                content = self._get_movie_details(content_id)
            elif content_type == 'manga':
                content = self._get_manga_details(content_id)
            elif content_type == 'anime':
                content = self._get_anime_details(content_id)
            elif content_type == 'track':
                content = self._get_track_details(content_id)
            elif content_type == 'artist':
                content = self._get_artist_details(content_id)
            elif content_type == 'album':
                content = self._get_album_details(content_id)
            else:
                content = None
            
            if content is None:
                return Response({
                    'success': False,
                    'message': f'{content_type.capitalize()} not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'success': True,
                'message': f'{content_type.capitalize()} details fetched successfully',
                'data': content
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error in PublicContentDetailView: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error fetching content details: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_movie_details(self, movie_id):
        """Get mock movie details"""
        # TODO: Replace with real data from database
        movies = {
            'movie_1': {
                'id': 'movie_1',
                'title': 'The Shawshank Redemption',
                'year': 1994,
                'rating': 9.3,
                'duration': '2h 22min',
                'genres': ['Drama'],
                'director': 'Frank Darabont',
                'cast': ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton'],
                'plot': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'poster': None,
                'trailer_url': None,
            },
            'movie_2': {
                'id': 'movie_2',
                'title': 'The Godfather',
                'year': 1972,
                'rating': 9.2,
                'duration': '2h 55min',
                'genres': ['Crime', 'Drama'],
                'director': 'Francis Ford Coppola',
                'cast': ['Marlon Brando', 'Al Pacino', 'James Caan'],
                'plot': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                'poster': None,
                'trailer_url': None,
            },
        }
        return movies.get(movie_id)
    
    def _get_manga_details(self, manga_id):
        """Get mock manga details"""
        # TODO: Replace with real data from database
        manga_list = {
            'manga_1': {
                'id': 'manga_1',
                'title': 'One Piece',
                'author': 'Eiichiro Oda',
                'chapters': 1100,
                'volumes': 107,
                'status': 'Ongoing',
                'rating': 9.0,
                'genres': ['Action', 'Adventure', 'Fantasy'],
                'synopsis': 'The story follows the adventures of Monkey D. Luffy, a boy whose body gained the properties of rubber after unintentionally eating a Devil Fruit.',
                'cover': None,
                'published': '1997-present',
            },
            'manga_2': {
                'id': 'manga_2',
                'title': 'Attack on Titan',
                'author': 'Hajime Isayama',
                'chapters': 139,
                'volumes': 34,
                'status': 'Completed',
                'rating': 8.8,
                'genres': ['Action', 'Dark Fantasy', 'Post-apocalyptic'],
                'synopsis': 'In a world where humanity lives inside cities surrounded by enormous walls due to the Titans, gigantic humanoid beings who devour humans.',
                'cover': None,
                'published': '2009-2021',
            },
        }
        return manga_list.get(manga_id)
    
    def _get_anime_details(self, anime_id):
        """Get mock anime details"""
        # TODO: Replace with real data from database
        anime_list = {
            'anime_1': {
                'id': 'anime_1',
                'title': 'Fullmetal Alchemist: Brotherhood',
                'episodes': 64,
                'rating': 9.1,
                'status': 'Completed',
                'genres': ['Action', 'Adventure', 'Drama', 'Fantasy'],
                'studio': 'Bones',
                'synopsis': 'Two brothers search for a Philosopher\'s Stone after an attempt to revive their deceased mother goes awry and leaves them in damaged physical forms.',
                'cover': None,
                'aired': '2009-2010',
            },
            'anime_2': {
                'id': 'anime_2',
                'title': 'Steins;Gate',
                'episodes': 24,
                'rating': 9.0,
                'status': 'Completed',
                'genres': ['Sci-Fi', 'Thriller', 'Drama'],
                'studio': 'White Fox',
                'synopsis': 'A group of friends discover a way to send messages to the past, but their time-bending experiments soon spiral out of control.',
                'cover': None,
                'aired': '2011',
            },
        }
        return anime_list.get(anime_id)
    
    def _get_track_details(self, track_id):
        """Get mock track details"""
        tracks = {
            'track_1': {
                'id': 'track_1',
                'name': 'Anti-Hero',
                'artist': 'Taylor Swift',
                'album': 'Midnights',
                'duration': '3:20',
                'release_date': '2022-10-21',
                'popularity': 95,
                'genres': ['Pop'],
                'preview_url': None,
                'lyrics_available': False,
            },
            'track_2': {
                'id': 'track_2',
                'name': 'Blinding Lights',
                'artist': 'The Weeknd',
                'album': 'After Hours',
                'duration': '3:22',
                'release_date': '2019-11-29',
                'popularity': 92,
                'genres': ['Synth-pop', 'R&B'],
                'preview_url': None,
                'lyrics_available': False,
            },
        }
        return tracks.get(track_id)
    
    def _get_artist_details(self, artist_id):
        """Get mock artist details"""
        artists = {
            'artist_1': {
                'id': 'artist_1',
                'name': 'Taylor Swift',
                'genre': 'Pop',
                'followers': 1500000,
                'popularity': 95,
                'bio': 'American singer-songwriter known for narrative songs about her personal life.',
                'top_tracks': ['Anti-Hero', 'Blank Space', 'Shake It Off'],
                'image': None,
            },
            'artist_2': {
                'id': 'artist_2',
                'name': 'The Weeknd',
                'genre': 'R&B',
                'followers': 1200000,
                'popularity': 92,
                'bio': 'Canadian singer, songwriter, and record producer.',
                'top_tracks': ['Blinding Lights', 'Starboy', 'The Hills'],
                'image': None,
            },
        }
        return artists.get(artist_id)
    
    def _get_album_details(self, album_id):
        """Get mock album details"""
        albums = {
            'album_1': {
                'id': 'album_1',
                'name': 'Midnights',
                'artist': 'Taylor Swift',
                'release_date': '2022-10-21',
                'total_tracks': 13,
                'genres': ['Pop'],
                'cover': None,
                'tracks': [
                    {'id': 'track_1', 'name': 'Anti-Hero', 'duration': '3:20'},
                ],
            },
        }
        return albums.get(album_id)
