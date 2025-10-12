from adrf.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from app.middlewares.async_jwt_authentication import AsyncJWTAuthentication
from django.contrib.auth import get_user_model
from app.services.recommendation_service import get_recommendation_service
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class GetRecommendations(APIView):
    """
    Get personalized recommendations for the authenticated user
    Based on their listening history, liked items, and top items
    Includes movies, manga, and anime recommendations
    """
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        try:
            user = request.user
            logger.info(f"[GetRecommendations] User {user.username} requesting recommendations")

            recommendation_service = get_recommendation_service()
            
            # Get recommendations for different content types
            recommendations = {
                'movies': [],
                'manga': [],
                'anime': [],
                'tracks': [],
                'artists': [],
                'albums': [],
                'genres': [],
                'buds': [],
            }
            
            # Get movie recommendations
            try:
                movies = await recommendation_service.get_movie_recommendations(
                    user_id=str(user.id),
                    n_recommendations=10
                )
                recommendations['movies'] = movies
            except Exception as e:
                logger.error(f"Error getting movie recommendations: {e}")
            
            # Get manga recommendations
            try:
                manga = await recommendation_service.get_manga_recommendations(
                    user_id=str(user.id),
                    n_recommendations=10
                )
                recommendations['manga'] = manga
            except Exception as e:
                logger.error(f"Error getting manga recommendations: {e}")
            
            # Get anime recommendations
            try:
                anime = await recommendation_service.get_anime_recommendations(
                    user_id=str(user.id),
                    n_recommendations=10
                )
                recommendations['anime'] = anime
            except Exception as e:
                logger.error(f"Error getting anime recommendations: {e}")

            return Response({
                'success': True,
                'message': 'Recommendations fetched successfully',
                'data': recommendations
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"[GetRecommendations] Error: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error fetching recommendations: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetRecommendationsByType(APIView):
    """
    Get recommendations of a specific type (tracks, artists, albums, genres, movies, manga, anime)
    """
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def get(self, request, rec_type):
        try:
            user = request.user
            logger.info(f"[GetRecommendationsByType] User {user.username} requesting {rec_type} recommendations")

            valid_types = ['tracks', 'artists', 'albums', 'genres', 'buds', 'movies', 'manga', 'anime']
            if rec_type not in valid_types:
                return Response({
                    'success': False,
                    'message': f'Invalid recommendation type: {rec_type}. Valid types: {valid_types}'
                }, status=status.HTTP_400_BAD_REQUEST)

            recommendation_service = get_recommendation_service()
            recommendations = []
            
            # Handle different recommendation types
            if rec_type == 'movies':
                recommendations = await recommendation_service.get_movie_recommendations(
                    user_id=str(user.id),
                    n_recommendations=20
                )
            elif rec_type == 'manga':
                recommendations = await recommendation_service.get_manga_recommendations(
                    user_id=str(user.id),
                    n_recommendations=20
                )
            elif rec_type == 'anime':
                recommendations = await recommendation_service.get_anime_recommendations(
                    user_id=str(user.id),
                    n_recommendations=20
                )
            else:
                # For music-related types, return empty for now
                # Can be implemented later
                recommendations = []

            return Response({
                'success': True,
                'message': f'{rec_type.capitalize()} recommendations fetched successfully',
                'data': recommendations
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"[GetRecommendationsByType] Error: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error fetching {rec_type} recommendations: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TrainRecommendationModels(APIView):
    """
    Train recommendation models for movies, manga, and anime
    Admin/background task endpoint
    """
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def post(self, request):
        try:
            user = request.user
            logger.info(f"[TrainRecommendationModels] User {user.username} requesting model training")
            
            # Check if user is staff/admin
            if not user.is_staff:
                return Response({
                    'success': False,
                    'message': 'Only staff users can train models'
                }, status=status.HTTP_403_FORBIDDEN)
            
            recommendation_service = get_recommendation_service()
            
            # Train all models
            results = await recommendation_service.train_all_models()
            
            return Response({
                'success': True,
                'message': 'Model training completed',
                'data': results
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"[TrainRecommendationModels] Error: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error training models: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
