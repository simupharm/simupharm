"""
SimuPharma Backend — FastAPI Application

Powers the pharmaceutical instrument simulation platform with:
- Real scientific computing (Beer-Lambert, FFT, Van Deemter, etc.)
- 20+ pharmaceutical compound database with multi-instrument data
- JWT authentication & user management
- Email verification & password reset
- Role-based access control (RBAC)
- Experiment logging & progress analytics
- Rate limiting, structured logging & security headers

Run: uvicorn backend.main:app --reload --port 8000
Docs: http://localhost:8000/docs (Swagger UI)
"""
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
from pathlib import Path
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .config import CORS_ORIGINS, RATE_LIMIT_API, ENVIRONMENT
from .database import create_tables
from .logging_config import get_logger
from .middleware.security import SecurityHeadersMiddleware, HTTPSRedirectMiddleware

logger = get_logger(__name__)

# ---- Rate Limiter (shared across routers) ----
limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMIT_API])

# Routers
from .auth.router import router as auth_router
from .compounds.router import router as compounds_router
from .experiments.router import router as experiments_router
from .analytics.router import router as analytics_router
from .analytics.faculty_router import router as faculty_router
from .analytics.metrics_router import router as metrics_router
from .analytics.leaderboard_router import router as leaderboard_router
from .neural.router import router as neural_router
from .ai.router import router as ai_router
from .simulations.router import router as simulations_router
from .billing.router import router as billing_router
from .billing.webhooks import router as webhook_router


# ---- App Setup ----
app = FastAPI(
    title="SimuPharma API",
    description="Pharmaceutical Instrument Simulation Engine — Real scientific computing for UV-Vis, FTIR, HPLC, GC, Mass Spec, Polarimeter, and PSA.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security middleware
app.add_middleware(SecurityHeadersMiddleware)
if ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)


# ---- Rate Limit Error Handler ----
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ---- Request Logging Middleware ----
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        f"{request.method} {request.url.path} → {response.status_code}",
        extra={
            "endpoint": str(request.url.path),
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    return response


@app.on_event("startup")
def startup():
    create_tables()
    logger.info(f"SimuPharma API started successfully (environment: {ENVIRONMENT})")


# ---- Include Routers (API v1) ----
# All routers are mounted under /api/v1/ prefix
app.include_router(auth_router, prefix="/api/v1")
app.include_router(compounds_router, prefix="/api/v1")
app.include_router(experiments_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(faculty_router, prefix="/api/v1")
app.include_router(metrics_router, prefix="/api/v1")
app.include_router(leaderboard_router, prefix="/api/v1")
app.include_router(neural_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
app.include_router(simulations_router, prefix="/api/v1")
app.include_router(billing_router, prefix="/api/v1")
app.include_router(webhook_router, prefix="/api/v1")


# ---- Health Check (unversioned — convention) ----
@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "SimuPharma API",
        "version": "2.0.0",
        "environment": ENVIRONMENT,
        "engines": ["uvvis", "ftir", "hplc", "gc", "mass_spec", "polarimeter", "psa"],
        "ai": {
            "autonomous_agent": True,
            "adaptive_learning": True,
            "knowledge_graph": True,
            "tools_available": 11
        }
    }


# ---- Backward Compatibility: Redirect old /api/* to /api/v1/* ----
@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"], include_in_schema=False)
async def redirect_old_api(path: str, request: Request):
    """Redirect old /api/ paths to /api/v1/ for backward compatibility."""
    # Don't redirect health check or docs
    if path in ("health", "docs", "redoc", "openapi.json"):
        return None

    new_url = f"/api/v1/{path}"
    if request.url.query:
        new_url += f"?{request.url.query}"
    return RedirectResponse(url=new_url, status_code=307)


# ========================================================================
# STATIC FILES — Serve Frontend (must be LAST so API routes take priority)
# ========================================================================
class NoCacheStaticFiles(StaticFiles):
    def is_not_modified(self, response_headers, request_headers) -> bool:
        return False

    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = "0"
        response.headers["Pragma"] = "no-cache"
        return response

frontend_dir = Path(__file__).resolve().parent.parent
if frontend_dir.exists():
    app.mount("/", NoCacheStaticFiles(directory=str(frontend_dir), html=True), name="frontend")
