from django.http import JsonResponse
from adrf.views import APIView
from rest_framework.permissions import IsAuthenticated
from app.middlewares.async_jwt_authentication import AsyncJWTAuthentication
from ..pagination import StandardResultsSetPagination
import logging
import traceback

logger = logging.getLogger('app')

class LibraryMixin(APIView):
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]
    library_type = None

    async def get(self, request):
        try:
            parent_user = request.parent_user
            if not parent_user:
                return JsonResponse({'error': 'User not found'}, status=404)

            # For now, return empty library content
            # In a real implementation, this would fetch user's library
            content = []

            paginator = StandardResultsSetPagination()
            paginated_content = paginator.paginate_queryset(content, request)
            paginated_response = paginator.get_paginated_response(paginated_content)

            return JsonResponse({
                'content': paginated_response,
                'message': f'Fetched {self.library_type} successfully.',
                'code': 200,
                'successful': True,
            })

        except Exception as e:
            logger.error(f'Error fetching {self.library_type}: {e}')
            logger.error(traceback.format_exc())
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

class GetLibrary(LibraryMixin):
    library_type = 'library'

class GetLibraryPlaylists(LibraryMixin):
    library_type = 'playlists'

class GetLibraryLiked(LibraryMixin):
    library_type = 'liked'

class GetLibraryDownloads(LibraryMixin):
    library_type = 'downloads'

class GetLibraryRecent(LibraryMixin):
    library_type = 'recent'