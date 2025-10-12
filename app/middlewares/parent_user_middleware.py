import logging
from asgiref.sync import sync_to_async, async_to_sync
from app.db_models.parent_user import ParentUser
import asyncio
from django.utils.deprecation import MiddlewareMixin
logger = logging.getLogger(__name__)


class ParentUserMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        user = request.user
        if user and user.is_authenticated:
            parent_user = self.get_parent_user(user.username)
            request.parent_user = parent_user
        else:
            request.parent_user = None
    
    def get_parent_user(self, username):
        from app.db_models.parent_user import ParentUser

        try:
            # Convert async neomodel call to sync using async_to_sync
            get_parent_sync = async_to_sync(self._get_parent_user_async)
            return get_parent_sync(username)
        except ParentUser.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting parent user: {e}")
            return None
    
    async def _get_parent_user_async(self, username):
        from app.db_models.parent_user import ParentUser
        return await ParentUser.nodes.get(username=username)
