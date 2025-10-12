from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class GetRecentActivity(APIView):
    """
    Get recent activity for the authenticated user
    Includes recently played tracks, recently added items, etc.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))

            logger.info(f"[GetRecentActivity] User {user.username} requesting recent activity (page {page})")

            # TODO: Implement actual recent activity tracking
            # This would typically query a activity/history table
            recent_activity = {
                'items': [],
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': 0,
                    'total_pages': 0
                }
            }

            return Response({
                'success': True,
                'message': 'Recent activity fetched successfully',
                'data': recent_activity
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"[GetRecentActivity] Error: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error fetching recent activity: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetRecentActivityByType(APIView):
    """
    Get recent activity of a specific type
    Types: tracks, artists, albums, searches, etc.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, activity_type):
        try:
            user = request.user
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))

            logger.info(f"[GetRecentActivityByType] User {user.username} requesting {activity_type} activity")

            valid_types = ['tracks', 'artists', 'albums', 'searches', 'playlists']
            if activity_type not in valid_types:
                return Response({
                    'success': False,
                    'message': f'Invalid activity type: {activity_type}. Valid types: {", ".join(valid_types)}'
                }, status=status.HTTP_400_BAD_REQUEST)

            # TODO: Implement type-specific activity
            activity = {
                'items': [],
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': 0,
                    'total_pages': 0
                }
            }

            return Response({
                'success': True,
                'message': f'Recent {activity_type} activity fetched successfully',
                'data': activity
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"[GetRecentActivityByType] Error: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error fetching {activity_type} activity: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
