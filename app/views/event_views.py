from django.http import JsonResponse
from adrf.views import APIView
from rest_framework.permissions import IsAuthenticated
from app.middlewares.async_jwt_authentication import AsyncJWTAuthentication
from ..pagination import StandardResultsSetPagination
import logging
import traceback

logger = logging.getLogger('app')

class GetEvents(APIView):
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        try:
            # For now, return empty events
            events = []

            paginator = StandardResultsSetPagination()
            paginated_events = paginator.paginate_queryset(events, request)
            paginated_response = paginator.get_paginated_response(paginated_events)

            return JsonResponse({
                'events': paginated_response,
                'message': 'Events fetched successfully.',
                'code': 200,
                'successful': True,
            })

        except Exception as e:
            logger.error(f'Error fetching events: {e}')
            logger.error(traceback.format_exc())
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

class GetEventById(APIView):
    authentication_classes = [AsyncJWTAuthentication]
    permission_classes = [IsAuthenticated]

    async def get(self, request, event_id):
        try:
            # For now, return empty event
            event = {}

            return JsonResponse({
                'event': event,
                'message': 'Event fetched successfully.',
                'code': 200,
                'successful': True,
            })

        except Exception as e:
            logger.error(f'Error fetching event {event_id}: {e}')
            logger.error(traceback.format_exc())
            return JsonResponse({'error': 'Internal Server Error'}, status=500)