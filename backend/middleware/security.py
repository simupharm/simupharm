"""Security Middleware — Headers, HTTPS redirect, and request ID tracking.

Adds production security headers, HTTPS redirect (in production), and a
unique X-Request-ID to every response for traceability.
"""
import uuid
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from ..config import ENVIRONMENT
from ..logging_config import get_logger

logger = get_logger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Adds security headers to all responses."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Request ID for traceability
        request_id = str(uuid.uuid4())
        response.headers["X-Request-ID"] = request_id

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

        # HSTS in production (tells browsers to always use HTTPS)
        if ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        # Content Security Policy (permissive for dev, strict for prod)
        if ENVIRONMENT == "production":
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
                "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
                "img-src 'self' data: https:; "
                "connect-src 'self' https://generativelanguage.googleapis.com https://pubchem.ncbi.nlm.nih.gov; "
                "frame-ancestors 'none';"
            )

        return response


class HTTPSRedirectMiddleware(BaseHTTPMiddleware):
    """Redirects HTTP to HTTPS in production."""

    async def dispatch(self, request: Request, call_next):
        if ENVIRONMENT == "production":
            # Check X-Forwarded-Proto header (set by reverse proxy like Nginx)
            forwarded_proto = request.headers.get("x-forwarded-proto", "")
            if forwarded_proto == "http":
                url = request.url.replace(scheme="https")
                return RedirectResponse(url=str(url), status_code=301)
        return await call_next(request)
