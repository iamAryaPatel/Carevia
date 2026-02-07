from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
from datetime import datetime
import logging

from app.config import settings
from app.routes.job_routes import router as job_router
from app.scheduler import start_scheduler, stop_scheduler
from app.database import close_database_connection, check_database_health
from app.middleware import (
    setup_logging,
    log_requests_middleware,
    carevia_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler,
    CareviaException,
)
from app.models import HealthResponse

# Setup logging
setup_logging(settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting Carevia application...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"API Version: {settings.api_version}")
    
    # Start background scheduler
    start_scheduler()
    logger.info("Background scheduler started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Carevia application...")
    stop_scheduler()
    close_database_connection()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Carevia Job Aggregator API",
    description="API for aggregating job listings from multiple sources",
    version=settings.api_version,
    docs_url=f"/api/{settings.api_version}/docs",
    redoc_url=f"/api/{settings.api_version}/redoc",
    openapi_url=f"/api/{settings.api_version}/openapi.json",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted Host Middleware (security)
if settings.is_production:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.cors_origins
    )

# Request logging middleware
app.middleware("http")(log_requests_middleware)

# Exception handlers
app.add_exception_handler(CareviaException, carevia_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers with API versioning
app.include_router(job_router, prefix=f"/api/{settings.api_version}")


@app.get("/", tags=["Root"])
def root():
    """Root endpoint."""
    return {
        "message": "Carevia Job Aggregator API",
        "version": settings.api_version,
        "docs": f"/api/{settings.api_version}/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        HealthResponse: Application health status
    """
    db_healthy = check_database_health()
    
    return HealthResponse(
        status="healthy" if db_healthy else "degraded",
        database="connected" if db_healthy else "disconnected",
        timestamp=datetime.now()
    )


@app.get("/ready", tags=["Health"])
def readiness_check():
    """
    Readiness check endpoint for load balancers.
    
    Returns:
        dict: Readiness status
    """
    db_healthy = check_database_health()
    
    if not db_healthy:
        return {"ready": False, "reason": "Database not connected"}, 503
    
    return {"ready": True}

