"""
Common middleware for Aura Backend Services
"""

import time
import uuid
import logging
from typing import Callable, Dict, Any
from fastapi import Request, Response, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint
import json

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging all requests and responses"""
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Log request
        start_time = time.time()
        logger.info(
            f"REQUEST {request_id}: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"RESPONSE {request_id}: {response.status_code} "
                f"in {process_time:.3f}s"
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.3f}"
            
            return response
            
        except Exception as e:
            # Log error
            process_time = time.time() - start_time
            logger.error(
                f"ERROR {request_id}: {str(e)} in {process_time:.3f}s"
            )
            raise


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for global error handling"""
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except HTTPException:
            # Re-raise HTTP exceptions to be handled by FastAPI
            raise
        except Exception as e:
            # Handle unexpected errors
            request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))
            
            logger.error(f"Unhandled error {request_id}: {str(e)}", exc_info=True)
            
            error_response = {
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An internal server error occurred",
                    "request_id": request_id
                },
                "timestamp": time.time()
            }
            
            return JSONResponse(
                status_code=500,
                content=error_response
            )


class RateLimitingMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware using in-memory storage"""
    
    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.clients = {}
        self.window_size = 60  # 1 minute in seconds
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean old entries
        self._cleanup_old_entries(current_time)
        
        # Check rate limit
        if self._is_rate_limited(client_ip, current_time):
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": f"Rate limit exceeded. Maximum {self.requests_per_minute} requests per minute."
                    }
                }
            )
        
        # Record request
        self._record_request(client_ip, current_time)
        
        return await call_next(request)
    
    def _cleanup_old_entries(self, current_time: float):
        """Remove entries older than the window size"""
        cutoff_time = current_time - self.window_size
        
        for client_ip in list(self.clients.keys()):
            self.clients[client_ip] = [
                timestamp for timestamp in self.clients[client_ip]
                if timestamp > cutoff_time
            ]
            
            # Remove empty entries
            if not self.clients[client_ip]:
                del self.clients[client_ip]
    
    def _is_rate_limited(self, client_ip: str, current_time: float) -> bool:
        """Check if client has exceeded rate limit"""
        if client_ip not in self.clients:
            return False
        
        # Count requests in current window
        cutoff_time = current_time - self.window_size
        valid_requests = [
            timestamp for timestamp in self.clients[client_ip]
            if timestamp > cutoff_time
        ]
        
        return len(valid_requests) >= self.requests_per_minute
    
    def _record_request(self, client_ip: str, current_time: float):
        """Record a request for the client"""
        if client_ip not in self.clients:
            self.clients[client_ip] = []
        
        self.clients[client_ip].append(current_time)


class CORSMiddleware(BaseHTTPMiddleware):
    """Custom CORS middleware"""
    
    def __init__(self, app, allow_origins: list = None, allow_methods: list = None, allow_headers: list = None):
        super().__init__(app)
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
        self.allow_headers = allow_headers or ["*"]
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Handle preflight requests
        if request.method == "OPTIONS":
            response = Response()
            self._add_cors_headers(response, request)
            return response
        
        # Process normal request
        response = await call_next(request)
        self._add_cors_headers(response, request)
        
        return response
    
    def _add_cors_headers(self, response: Response, request: Request):
        """Add CORS headers to response"""
        origin = request.headers.get("origin")
        
        if "*" in self.allow_origins:
            response.headers["Access-Control-Allow-Origin"] = "*"
        elif origin and origin in self.allow_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
        
        response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
        response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
        response.headers["Access-Control-Allow-Credentials"] = "true"


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers"""
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response


def create_error_handler():
    """Create a standard error handler function"""
    
    def error_handler(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))
        
        if isinstance(exc, HTTPException):
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "success": False,
                    "error": {
                        "code": f"HTTP_{exc.status_code}",
                        "message": exc.detail,
                        "request_id": request_id
                    },
                    "timestamp": time.time()
                }
            )
        
        # Log unexpected errors
        logger.error(f"Unhandled error {request_id}: {str(exc)}", exc_info=True)
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An internal server error occurred",
                    "request_id": request_id
                },
                "timestamp": time.time()
            }
        )
    
    return error_handler


def get_request_id(request: Request) -> str:
    """Get request ID from request state"""
    return getattr(request.state, 'request_id', str(uuid.uuid4()))


def validate_json_content_type(request: Request):
    """Validate that request has JSON content type"""
    content_type = request.headers.get("content-type", "")
    if not content_type.startswith("application/json"):
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_CONTENT_TYPE",
                "message": "Content-Type must be application/json"
            }
        )


async def log_request_body(request: Request) -> Dict[str, Any]:
    """Log request body for debugging (use carefully with sensitive data)"""
    try:
        body = await request.body()
        if body:
            request_data = json.loads(body.decode())
            request_id = get_request_id(request)
            logger.debug(f"Request body {request_id}: {request_data}")
            return request_data
        return {}
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body")
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_JSON",
                "message": "Request body must be valid JSON"
            }
        )
    except Exception as e:
        logger.error(f"Error reading request body: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "code": "REQUEST_BODY_ERROR",
                "message": "Error reading request body"
            }
        )


class HealthCheckMiddleware(BaseHTTPMiddleware):
    """Middleware to handle health check requests efficiently"""
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Fast path for health checks
        if request.url.path in ["/health", "/healthz", "/ping"]:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "healthy",
                    "timestamp": time.time(),
                    "service": "aura-backend"
                }
            )
        
        return await call_next(request)
