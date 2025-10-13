"""
Hybrid ASGI Application for Django to FastAPI Migration
This allows running both Django and FastAPI simultaneously during migration
"""
import os
import logging
from typing import Dict, Any
from urllib.parse import urlparse

# Django imports
from django.core.asgi import get_asgi_application
from django.conf import settings

# FastAPI imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import Mount

# Set Django settings before importing Django ASGI app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicbud.settings')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import FastAPI app
from fastapi_backend.app.main import app as fastapi_app

class HybridApplication:
    """
    Hybrid application that routes requests between Django and FastAPI
    based on URL patterns
    """
    
    def __init__(self):
        self.django_app = get_asgi_application()
        self.fastapi_app = fastapi_app
        
        # Define routing rules
        self.fastapi_prefixes = [
            '/api/v2/',    # New FastAPI v2 endpoints
            '/api/fastapi/',  # FastAPI-specific endpoints
            '/docs',       # FastAPI docs
            '/redoc',      # FastAPI redoc
            '/openapi.json',  # OpenAPI spec
            '/v1/discover/public/',  # Public endpoints in FastAPI
            '/v1/recommendations/public/',
            '/health',     # Health check
        ]
        
        # Django handles everything else for now
        self.django_prefixes = [
            '/admin/',     # Django admin
            '/v1/',        # Current Django API v1 (except FastAPI prefixes)
            '/chat/',      # Chat system
            '/login/',     # Auth pages
            '/register/',
            '/',           # Root and other Django views
        ]
        
        logger.info("🚀 Hybrid ASGI application initialized")
        logger.info(f"📡 FastAPI routes: {self.fastapi_prefixes}")
        logger.info(f"📋 Django routes: {self.django_prefixes}")
    
    async def __call__(self, scope: Dict[str, Any], receive, send):
        """
        Main ASGI entrypoint - routes requests between Django and FastAPI
        """
        if scope["type"] == "http":
            return await self.route_http_request(scope, receive, send)
        elif scope["type"] == "websocket":
            # WebSocket requests go to Django (for channels/chat)
            return await self.django_app(scope, receive, send)
        else:
            # Other protocols go to Django
            return await self.django_app(scope, receive, send)
    
    async def route_http_request(self, scope: Dict[str, Any], receive, send):
        """
        Route HTTP requests between Django and FastAPI
        """
        path = scope.get("path", "")
        method = scope.get("method", "GET")
        
        # Log request for debugging
        logger.debug(f"📥 {method} {path}")
        
        # Check if request should go to FastAPI
        if self.should_use_fastapi(path):
            logger.debug(f"➡️  Routing to FastAPI: {path}")
            return await self.fastapi_app(scope, receive, send)
        else:
            logger.debug(f"➡️  Routing to Django: {path}")
            return await self.django_app(scope, receive, send)
    
    def should_use_fastapi(self, path: str) -> bool:
        """
        Determine if request should be routed to FastAPI
        """
        # Check FastAPI prefixes first (these take priority)
        for prefix in self.fastapi_prefixes:
            if path.startswith(prefix):
                return True
        
        # Special case: root path goes to FastAPI if it's a health check
        if path == "/" and hasattr(self.fastapi_app, 'routes'):
            # Check if FastAPI has a root route
            return True
        
        return False


# Create FastAPI app with proper configuration
def create_fastapi_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    # Import here to avoid circular imports
    from fastapi_backend.app.core.config import settings as fastapi_settings
    from fastapi_backend.app.api.v1 import api_router
    
    app = FastAPI(
        title="MusicBud API v2",
        version="2.0.0",
        description="MusicBud FastAPI - Modern API with enhanced features",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure properly for production
        allow_credentials=True,
        allow_methods=["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"],
        allow_headers=[
            "accept",
            "accept-encoding", 
            "authorization",
            "content-type",
            "dnt",
            "origin",
            "user-agent",
            "x-csrftoken",
            "x-requested-with",
        ],
    )
    
    # Include API routes
    app.include_router(api_router, prefix="/v1")
    
    # Add migration-specific routes
    @app.get("/api/v2/migration-status")
    async def migration_status():
        """Migration status endpoint"""
        return {
            "status": "in_progress",
            "django_active": True,
            "fastapi_active": True,
            "version": "2.0.0",
            "migration_stage": "hybrid_mode"
        }
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Enhanced health check"""
        return {
            "status": "healthy",
            "service": "musicbud-hybrid",
            "version": "2.0.0",
            "timestamp": "2025-01-13T07:05:45Z"
        }
    
    # API Info endpoint
    @app.get("/api/info")
    async def api_info():
        """API information"""
        return {
            "api_name": "MusicBud Hybrid API",
            "version": "2.0.0",
            "fastapi_routes": [
                "/docs - API Documentation",
                "/redoc - Alternative API Documentation", 
                "/openapi.json - OpenAPI Specification",
                "/health - Health Check",
                "/api/v2/ - FastAPI v2 endpoints",
                "/v1/discover/public/ - Public content discovery",
                "/v1/recommendations/public/ - Public recommendations"
            ],
            "django_routes": [
                "/admin/ - Django Admin",
                "/v1/ - Django API v1 (existing endpoints)",
                "/chat/ - Chat system",
                "/login/, /register/ - Authentication",
                "/ - Web interface and other Django views"
            ]
        }
    
    logger.info("✅ FastAPI app configured for hybrid mode")
    return app


# Create the hybrid application
try:
    # Recreate FastAPI app for hybrid mode
    fastapi_app = create_fastapi_app()
    
    # Create hybrid application instance
    application = HybridApplication()
    application.fastapi_app = fastapi_app
    
    logger.info("🎯 Hybrid ASGI application ready!")
    logger.info("📍 FastAPI docs available at: /docs")
    logger.info("📍 Django admin available at: /admin/")
    logger.info("📍 Migration status at: /api/v2/migration-status")
    
except Exception as e:
    logger.error(f"❌ Failed to initialize hybrid application: {e}")
    # Fallback to Django only
    logger.info("🔄 Falling back to Django-only mode")
    application = get_asgi_application()