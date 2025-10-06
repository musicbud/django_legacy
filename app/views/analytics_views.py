from django.http import JsonResponse
from adrf.views import APIView
from rest_framework.permissions import IsAuthenticated
from app.middlewares.async_jwt_authentication import AsyncJWTAuthentication
import logging
import traceback

logger = logging.getLogger('app')

class GetAnalytics(APIView):
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        try:
            # For now, return empty analytics
            analytics = {
                'total_users': 0,
                'active_users': 0,
                'total_tracks': 0,
                'total_artists': 0,
                'total_playlists': 0,
            }

            return JsonResponse({
                'analytics': analytics,
                'message': 'Analytics fetched successfully.',
                'code': 200,
                'successful': True,
            })

        except Exception as e:
            logger.error(f'Error fetching analytics: {e}')
            logger.error(traceback.format_exc())
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

class GetAnalyticsStats(APIView):
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        try:
            # For now, return empty stats
            stats = {
                'user_growth': [],
                'content_growth': [],
                'engagement_metrics': {},
            }

            return JsonResponse({
                'stats': stats,
                'message': 'Analytics stats fetched successfully.',
                'code': 200,
                'successful': True,
            })

        except Exception as e:
            logger.error(f'Error fetching analytics stats: {e}')
            logger.error(traceback.format_exc())
            return JsonResponse({'error': 'Internal Server Error'}, status=500)