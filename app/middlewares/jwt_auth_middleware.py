import logging
from django.utils.functional import SimpleLazyObject
from asgiref.sync import sync_to_async
import asyncio

logger = logging.getLogger(__name__)

class JWTAuthMiddleware:
    # Paths that should bypass authentication
    PUBLIC_PATHS = [
        '/v1/discover/public/',
        '/v1/recommendations/public/',
        '/v1/content/public/',
        '/register/',
        '/login/',
        '/token/refresh/',
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if this is a public path
        if any(request.path.startswith(path) for path in self.PUBLIC_PATHS):
            # For public paths, set user to None (anonymous)
            request.user = None
        else:
            request.user = self._get_user(request)
        return self.get_response(request)

    def _get_user(self, request):
        from .async_jwt_authentication import AsyncJWTAuthentication

        auth = AsyncJWTAuthentication()
        try:
            result = auth.authenticate(request)
            if result is None:
                return None
            user, _ = result
            return user
        except Exception as e:
            logger.error(f"JWTAuthMiddleware: Authentication error: {str(e)}")
            return None

