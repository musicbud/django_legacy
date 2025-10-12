"""
API v1 Router
"""
from fastapi import APIRouter
from app.api.v1.endpoints.public import router as public_router
from app.api.v1.endpoints.public import recommendations_router, content_router
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.matching import router as matching_router
from app.api.v1.endpoints.chat import router as chat_router

api_router = APIRouter()

# Include all routers
api_router.include_router(public_router)
api_router.include_router(recommendations_router)
api_router.include_router(content_router)
api_router.include_router(users_router)
api_router.include_router(matching_router)
api_router.include_router(chat_router)
