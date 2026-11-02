"""SimuPharma Backend Configuration

All secrets and environment-specific values are loaded from environment
variables (via .env file in development).  Never hardcode secrets here.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env file (no-op in production where env vars are set directly)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BASE_DIR = Path(__file__).resolve().parent

# --- Environment ---
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development | staging | production

# --- Database ---
# Supports both SQLite (dev) and PostgreSQL (production) via DATABASE_URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{BASE_DIR / 'simupharma.db'}"
)

# --- JWT Settings ---
SECRET_KEY = os.getenv("SIMUPHARMA_SECRET_KEY", "")
if not SECRET_KEY:
    if ENVIRONMENT in ("production", "staging"):
        print(
            "FATAL: SIMUPHARMA_SECRET_KEY is not set in production/staging. "
            "Set it in your .env file or environment variables.",
            file=sys.stderr,
        )
        sys.exit(1)
    else:
        import warnings
        warnings.warn(
            "⚠️  SIMUPHARMA_SECRET_KEY is not set! Using insecure default. "
            "Set it in your .env file for production.",
            stacklevel=1,
        )
        SECRET_KEY = "insecure-dev-only-key-do-not-use-in-production"

ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# --- CORS ---
_cors_raw = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5500,http://127.0.0.1:5500,http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000"
)
CORS_ORIGINS = [origin.strip() for origin in _cors_raw.split(",") if origin.strip()]

# --- External APIs ---
PUBCHEM_BASE_URL = os.getenv("PUBCHEM_BASE_URL", "https://pubchem.ncbi.nlm.nih.gov/rest/pug")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# --- Rate Limiting ---
RATE_LIMIT_AUTH = os.getenv("RATE_LIMIT_AUTH", "5/minute")
RATE_LIMIT_API = os.getenv("RATE_LIMIT_API", "60/minute")

# --- Logging ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv("LOG_FORMAT", "json")

# --- Email / SMTP ---
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "noreply@simupharma.com")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"

# --- Frontend ---
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5500")

# --- Verification Token ---
VERIFICATION_TOKEN_EXPIRE_HOURS = int(os.getenv("VERIFICATION_TOKEN_EXPIRE_HOURS", "24"))
PASSWORD_RESET_TOKEN_EXPIRE_HOURS = int(os.getenv("PASSWORD_RESET_TOKEN_EXPIRE_HOURS", "1"))

# --- Razorpay / Payments ---
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "")
# Razorpay Plan IDs (create these in Razorpay Dashboard)
RAZORPAY_PLAN_PRO_MONTHLY = os.getenv("RAZORPAY_PLAN_PRO_MONTHLY", "")
RAZORPAY_PLAN_PRO_SEMESTER = os.getenv("RAZORPAY_PLAN_PRO_SEMESTER", "")
RAZORPAY_PLAN_PRO_ANNUAL = os.getenv("RAZORPAY_PLAN_PRO_ANNUAL", "")
