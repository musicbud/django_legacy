from django.http import JsonResponse
from adrf.views import APIView
from rest_framework.permissions import IsAuthenticated
from app.middlewares.async_jwt_authentication import AsyncJWTAuthentication
from ..pagination import StandardResultsSetPagination
import logging
import traceback

logger = logging.getLogger('app')

class SearchView(APIView):
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        try:
            query = request.GET.get('q', '')
            # For now, return empty results
            # In a real implementation, this would search across content
            results = {
                'tracks': [],
                'artists': [],
                'albums': [],
                'playlists': [],
                'users': [],
            }

            return JsonResponse({
                'query': query,
                'results': results,
                'message': 'Search completed successfully.',
                'code': 200,
                'successful': True,
            })

        except Exception as e:
            logger.error(f'Error performing search: {e}')
            logger.error(traceback.format_exc())
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

class SearchSuggestionsView(APIView):
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        try:
            query = request.GET.get('q', '')
            # For now, return empty suggestions
            suggestions = []

            return JsonResponse({
                'query': query,
                'suggestions': suggestions,
                'message': 'Suggestions fetched successfully.',
                'code': 200,
                'successful': True,
            })

        except Exception as e:
            logger.error(f'Error fetching suggestions: {e}')
            logger.error(traceback.format_exc())
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

class SearchRecentView(APIView):
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        try:
            # For now, return empty recent searches
            recent_searches = []

            return JsonResponse({
                'recent_searches': recent_searches,
                'message': 'Recent searches fetched successfully.',
                'code': 200,
                'successful': True,
            })

        except Exception as e:
            logger.error(f'Error fetching recent searches: {e}')
            logger.error(traceback.format_exc())
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

class SearchTrendingView(APIView):
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        try:
            # For now, return empty trending searches
            trending_searches = []

            return JsonResponse({
                'trending_searches': trending_searches,
                'message': 'Trending searches fetched successfully.',
                'code': 200,
                'successful': True,
            })

        except Exception as e:
            logger.error(f'Error fetching trending searches: {e}')
            logger.error(traceback.format_exc())
            return JsonResponse({'error': 'Internal Server Error'}, status=500)