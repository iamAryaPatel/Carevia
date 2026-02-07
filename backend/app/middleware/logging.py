"""Logging configuration and middleware."""

import logging
import sys
from datetime import datetime
from fastapi import Request
import time
import uuid


def setup_logging(log_level: str = "INFO"):
    """
    Configure structured logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    root_logger.addHandler(console_handler)
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)


async def log_requests_middleware(request: Request, call_next):
    """
    Middleware to log all incoming requests and responses.
    
    Args:
        request: FastAPI request object
        call_next: Next middleware/route handler
    """
    # Generate correlation ID for request tracking
    correlation_id = str(uuid.uuid4())
    request.state.correlation_id = correlation_id
    
    # Log request
    logger = logging.getLogger("carevia.requests")
    start_time = time.time()
    
    logger.info(
        f"[{correlation_id}] {request.method} {request.url.path} - "
        f"Client: {request.client.host if request.client else 'unknown'}"
    )
    
    # Process request
    try:
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"[{correlation_id}] {request.method} {request.url.path} - "
            f"Status: {response.status_code} - Time: {process_time:.3f}s"
        )
        
        # Add custom headers
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Process-Time"] = f"{process_time:.3f}"
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"[{correlation_id}] {request.method} {request.url.path} - "
            f"Error: {str(e)} - Time: {process_time:.3f}s",
            exc_info=True
        )
        raise
