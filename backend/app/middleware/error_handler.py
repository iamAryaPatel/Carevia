"""Custom exception classes and global exception handler."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


class CareviaException(Exception):
    """Base exception for Carevia application."""
    
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class DatabaseException(CareviaException):
    """Exception for database-related errors."""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(message, status_code=503)


class ExternalAPIException(CareviaException):
    """Exception for external API errors."""
    
    def __init__(self, message: str = "External API request failed"):
        super().__init__(message, status_code=502)


class NotFoundException(CareviaException):
    """Exception for resource not found errors."""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


async def carevia_exception_handler(request: Request, exc: CareviaException):
    """Handle custom Carevia exceptions."""
    logger.error(f"CareviaException: {exc.message}", exc_info=True)
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "path": str(request.url)
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Request validation failed",
            "details": exc.errors(),
            "path": str(request.url)
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions."""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTPException",
            "message": exc.detail,
            "path": str(request.url)
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "path": str(request.url)
        }
    )
