"""
MusicBud FastAPI Application - Complete Django Replacement
Production-ready async music recommendation API
"""

import logging
import os
import json # Import json for structured logging
import uuid # Import uuid for request IDs
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
from pythonjsonlogger import jsonlogger # Import jsonlogger for structured logging

# Import our custom modules
from backend.app.core.settings import settings
from backend.app.core.database import init_databases, close_databases
from backend.app.core.middleware import setup_middleware

# Import all routers
from backend.app.api.routers.auth import router as auth_router
from backend.app.api.routers.users import router as users_router
from backend.app.api.routers.content import router as content_router
from backend.app.api.routers.search import router as search_router
from backend.app.api.routers.recommendations import router as recommendations_router
from backend.app.api.routers.public import router as public_router
from backend.app.api.routers.library import router as library_router
from backend.app.api.routers.social import router as social_router
from backend.app.api.routers.analytics import router as analytics_router
from backend.app.api.routers.activity import router as activity_router
from backend.app.api.routers.admin import router as admin_router
from backend.app.api.routers.events import router as events_router
from backend.app.api.routers.stories import router as stories_router
from backend.app.api.routers.services import router as services_router # Import services_router

# Configure logging with structured JSON format
log_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt='%(levelname)s %(asctime)s %(name)s %(message)s %(request_id)s %(user_id)s %(remote_ip)s'
)
log_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(log_handler)
logger.setLevel(getattr(logging, settings.LOG_LEVEL))
logger.propagate = False # Prevent double logging if root handler is also configured


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup/shutdown events
    """
    # Startup
    logger.info("Starting MusicBud FastAPI application...")
    try:
        await init_databases()
        logger.info("Database connections initialized")
        
        # Initialize services
        from backend.app.services.recommendation_service import get_recommendation_service
        rec_service = get_recommendation_service()
        await rec_service.initialize()
        logger.info("Recommendation service initialized")
        
        logger.info("✅ MusicBud FastAPI application started successfully!")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down MusicBud FastAPI application...")
    try:
        await close_databases()
        logger.info("Database connections closed")
        logger.info("✅ MusicBud FastAPI application shut down successfully!")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# Setup middleware (includes CORS, security, rate limiting, etc.)
setup_middleware(app)

# Custom middleware for request ID and contextual logging
@app.middleware("http")
async def add_request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    # Add request ID to logs
    log_extra = {"request_id": request_id, "remote_ip": request.client.host}
    
    # Log user ID if available (from auth middleware)
    if hasattr(request.state, 'user') and request.state.user:
        log_extra["user_id"] = request.state.user.user_id
    else:
        log_extra["user_id"] = "anonymous"

    logger.info(f"Incoming request: {request.method} {request.url.path}", extra=log_extra)
    
    response = await call_next(request)
    
    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id
    return response


# Include routers with prefixes - organize by logical API structure
app.include_router(public_router, prefix="/v1/discover/public", tags=["Public Discovery"])
app.include_router(public_router, prefix="/v1/recommendations/public", tags=["Public Recommendations"])
app.include_router(recommendations_router, prefix="/v1/recommendations", tags=["Recommendations"])
app.include_router(auth_router, prefix="/v1/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/v1/users", tags=["Users"])
app.include_router(content_router, prefix="/v1/content", tags=["Content"])
app.include_router(search_router, prefix="/v1/search", tags=["Search"])
app.include_router(library_router, prefix="/v1/library", tags=["Library"])
app.include_router(social_router, prefix="/v1/social", tags=["Social"])
app.include_router(analytics_router, prefix="/v1/analytics", tags=["Analytics"])
app.include_router(activity_router, prefix="/v1/activity", tags=["Activity"])
app.include_router(admin_router, prefix="/v1/admin", tags=["Admin"])
app.include_router(events_router, prefix="/v1/events", tags=["Events"])
app.include_router(stories_router, prefix="/v1/stories", tags=["Stories"])
app.include_router(services_router, prefix="/v1/services", tags=["External Services"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MusicBud FastAPI - Music Recommendation Platform",
        "version": settings.VERSION,
        "status": "healthy",
        "docs": "/docs" if settings.DEBUG else "disabled in production"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from backend.app.core.database import DatabaseHealthCheck # Corrected import
    
    try:
        db_health = await DatabaseHealthCheck.check_all()
        
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "databases": db_health,
            "timestamp": db_health["timestamp"]
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "version": settings.VERSION
            }
        )


@app.get("/metrics")
async def get_metrics():
    """Get application metrics"""
    if not settings.DEBUG and not hasattr(app.state, 'metrics'):
        raise HTTPException(status_code=404, detail="Metrics not available")
    
    try:
        metrics = app.state.metrics.get_metrics() if hasattr(app.state, 'metrics') else {}
        return {
            "status": "success",
            "data": metrics,
            "version": settings.VERSION
        }
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving metrics")


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Custom 404 handler"""
    logger.error(f"Endpoint not found: {request.method} {request.url.path}", extra={"request_id": getattr(request.state, "request_id", None)})
    return JSONResponse(
        status_code=404,
        content={
            "error": True,
            "message": "Endpoint not found",
            "status_code": 404,
            "path": str(request.url.path),
            "method": request.method
        }
    )


@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: HTTPException):
    """Custom 500 handler"""
    logger.error(f"Internal server error: {exc}", extra={"request_id": getattr(request.state, "request_id", None)})
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500,
            "request_id": getattr(request.state, "request_id", None)
        }
    )


def create_app() -> FastAPI:
    """Factory function to create FastAPI app"""
    return app


if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "fastapi_app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )