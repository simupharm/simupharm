"""Auth Router — Register, Login, Profile, Email Verification, Password Reset"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from slowapi import Limiter
from slowapi.util import get_remote_address
from ..config import (
    RATE_LIMIT_AUTH, ENVIRONMENT,
    VERIFICATION_TOKEN_EXPIRE_HOURS, PASSWORD_RESET_TOKEN_EXPIRE_HOURS
)
from ..database import get_db
from ..models import User
from ..logging_config import get_logger
from .utils import (
    hash_password, verify_password, create_access_token, decode_token,
    generate_verification_token, generate_password_reset_token,
    validate_password_strength
)
from ..email.service import send_verification_email, send_password_reset_email

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)
logger = get_logger(__name__)

# Auth-specific rate limiter (stricter than global)
auth_limiter = Limiter(key_func=get_remote_address)


# ---- Schemas ----
class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    institution: str = ""


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    institution: str
    role: str
    is_verified: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class VerifyEmailRequest(BaseModel):
    token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class MessageResponse(BaseModel):
    message: str


# ---- Dependencies ----
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User | None:
    """Returns current user or None if not authenticated."""
    if not credentials:
        return None
    payload = decode_token(credentials.credentials)
    if not payload:
        return None
    user = db.query(User).filter(User.id == int(payload.get("sub", 0))).first()
    return user


def require_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Requires authenticated user — raises 401 if not."""
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == int(payload.get("sub", 0))).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# ---- Endpoints ----
@router.post("/register", response_model=TokenResponse)
@auth_limiter.limit("3/minute")
def register(req: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    # Check existing
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validate password strength
    password_error = validate_password_strength(req.password)
    if password_error:
        raise HTTPException(status_code=400, detail=password_error)

    # Generate verification token
    verification_token = generate_verification_token()
    token_expires = datetime.utcnow() + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)

    user = User(
        email=req.email,
        name=req.name,
        password_hash=hash_password(req.password),
        institution=req.institution,
        is_verified=False,
        verification_token=verification_token,
        verification_token_expires=token_expires,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Send verification email
    send_verification_email(req.email, verification_token, req.name)

    logger.info(f"New user registered: {user.email}", extra={"user_id": user.id})
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.post("/login", response_model=TokenResponse)
@auth_limiter.limit(RATE_LIMIT_AUTH)
def login(req: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        logger.warning(f"Failed login attempt for: {req.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check email verification (bypass in development mode)
    if not user.is_verified and ENVIRONMENT != "development":
        raise HTTPException(
            status_code=403,
            detail="Email not verified. Please check your email for the verification link."
        )

    logger.info(f"User logged in: {user.email}", extra={"user_id": user.id})
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(require_user)):
    return UserResponse.model_validate(user)


@router.post("/verify-email", response_model=MessageResponse)
def verify_email(req: VerifyEmailRequest, db: Session = Depends(get_db)):
    """Verify a user's email address using the token sent during registration."""
    user = db.query(User).filter(User.verification_token == req.token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")

    if user.is_verified:
        return MessageResponse(message="Email already verified")

    # Check token expiry
    if user.verification_token_expires and user.verification_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification token has expired. Request a new one.")

    user.is_verified = True
    user.verification_token = None
    user.verification_token_expires = None
    db.commit()

    logger.info(f"Email verified: {user.email}", extra={"user_id": user.id})
    return MessageResponse(message="Email verified successfully")


@router.post("/resend-verification", response_model=MessageResponse)
@auth_limiter.limit("2/minute")
def resend_verification(req: ForgotPasswordRequest, request: Request, db: Session = Depends(get_db)):
    """Resend email verification link."""
    user = db.query(User).filter(User.email == req.email).first()

    # Always return success to prevent email enumeration
    if not user or user.is_verified:
        return MessageResponse(message="If the email exists and is unverified, a verification link has been sent.")

    # Generate new token
    token = generate_verification_token()
    user.verification_token = token
    user.verification_token_expires = datetime.utcnow() + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)
    db.commit()

    send_verification_email(user.email, token, user.name)
    return MessageResponse(message="If the email exists and is unverified, a verification link has been sent.")


@router.post("/forgot-password", response_model=MessageResponse)
@auth_limiter.limit("3/minute")
def forgot_password(req: ForgotPasswordRequest, request: Request, db: Session = Depends(get_db)):
    """Request a password reset link. Sends an email with a secure reset token."""
    user = db.query(User).filter(User.email == req.email).first()

    # Always return success to prevent email enumeration
    if not user:
        return MessageResponse(message="If the email exists, a password reset link has been sent.")

    # Generate reset token
    token = generate_password_reset_token()
    user.password_reset_token = token
    user.password_reset_token_expires = datetime.utcnow() + timedelta(hours=PASSWORD_RESET_TOKEN_EXPIRE_HOURS)
    db.commit()

    send_password_reset_email(user.email, token, user.name)
    logger.info(f"Password reset requested for: {user.email}", extra={"user_id": user.id})
    return MessageResponse(message="If the email exists, a password reset link has been sent.")


@router.post("/reset-password", response_model=MessageResponse)
@auth_limiter.limit("5/minute")
def reset_password(req: ResetPasswordRequest, request: Request, db: Session = Depends(get_db)):
    """Reset password using the token from the forgot-password email."""
    user = db.query(User).filter(User.password_reset_token == req.token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    # Check token expiry
    if user.password_reset_token_expires and user.password_reset_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Reset token has expired. Request a new one.")

    # Validate new password strength
    password_error = validate_password_strength(req.new_password)
    if password_error:
        raise HTTPException(status_code=400, detail=password_error)

    # Update password and clear token
    user.password_hash = hash_password(req.new_password)
    user.password_reset_token = None
    user.password_reset_token_expires = None

    # Also verify email if not already (they had access to the email)
    if not user.is_verified:
        user.is_verified = True
        user.verification_token = None
        user.verification_token_expires = None

    db.commit()

    logger.info(f"Password reset completed for: {user.email}", extra={"user_id": user.id})
    return MessageResponse(message="Password has been reset successfully. You can now log in with your new password.")
