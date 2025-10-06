from django.http import JsonResponse
from adrf.views import APIView
from rest_framework.permissions import IsAuthenticated
from app.middlewares.async_jwt_authentication import AsyncJWTAuthentication
from ..pagination import StandardResultsSetPagination
import logging
import traceback

logger = logging.getLogger('app')

class ContentMixin(APIView):
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]
    content_type = None

    async def get(self, request):
        try:
            # For now, return empty content
            # In a real implementation, this would fetch from a content service
            content = []

            paginator = StandardResultsSetPagination()
            paginated_content = paginator.paginate_queryset(content, request)
            paginated_response = paginator.get_paginated_response(paginated_content)

            return JsonResponse({
                'content': paginated_response,
                'message': f'Fetched {self.content_type} successfully.',
                'code': 200,
                'successful': True,
            })

        except Exception as e:
            logger.error(f'Error fetching {self.content_type}: {e}')
            logger.error(traceback.format_exc())
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

class GetTracks(ContentMixin):
    content_type = 'tracks'

class GetArtists(ContentMixin):
    content_type = 'artists'

class GetAlbums(ContentMixin):
    content_type = 'albums'

class GetPlaylists(ContentMixin):
    content_type = 'playlists'

class GetGenres(ContentMixin):
    content_type = 'genres'