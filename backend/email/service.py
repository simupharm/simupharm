"""Email Service — Sends transactional emails (verification, password reset).

In development mode (no SMTP configured), emails are printed to console.
In production, uses SMTP (compatible with SendGrid, SES, Gmail, etc.)
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config import (
    ENVIRONMENT, SMTP_HOST, SMTP_PORT, SMTP_USERNAME,
    SMTP_PASSWORD, SMTP_FROM_EMAIL, SMTP_USE_TLS, FRONTEND_URL
)
from ..logging_config import get_logger

logger = get_logger(__name__)


def _send_email(to_email: str, subject: str, html_body: str, text_body: str = "") -> bool:
    """Send an email. Uses SMTP in production, console in development."""
    if not SMTP_HOST:
        # Development mode — print to console
        logger.info(
            f"\n{'='*60}\n"
            f"📧 EMAIL (dev mode — not actually sent)\n"
            f"To: {to_email}\n"
            f"Subject: {subject}\n"
            f"{'─'*60}\n"
            f"{text_body or html_body}\n"
            f"{'='*60}"
        )
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_FROM_EMAIL
        msg["To"] = to_email

        if text_body:
            msg.attach(MIMEText(text_body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            if SMTP_USE_TLS:
                server.starttls()
            if SMTP_USERNAME:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}", extra={"error": str(e)})
        return False


def send_verification_email(to_email: str, token: str, user_name: str = "User") -> bool:
    """Send email verification link."""
    verification_url = f"{FRONTEND_URL}/verify-email?token={token}"
    subject = "SimuPharma — Verify Your Email"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8fafc;">
        <div style="background: linear-gradient(135deg, #2563EB, #7C3AED); padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">🧪 SimuPharma</h1>
            <p style="color: rgba(255,255,255,0.9); margin-top: 8px; font-size: 14px;">Virtual Pharmaceutical Laboratory</p>
        </div>
        <div style="background: white; padding: 30px; border-radius: 0 0 12px 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h2 style="color: #1e293b; margin-top: 0;">Welcome, {user_name}! 👋</h2>
            <p style="color: #475569; line-height: 1.6;">
                Thank you for joining SimuPharma. Please verify your email address to activate your account.
            </p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{verification_url}"
                   style="background: linear-gradient(135deg, #2563EB, #7C3AED); color: white; padding: 14px 32px;
                          border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 16px;
                          display: inline-block;">
                    Verify Email Address
                </a>
            </div>
            <p style="color: #94a3b8; font-size: 13px;">
                If the button doesn't work, copy and paste this link into your browser:<br>
                <a href="{verification_url}" style="color: #2563EB; word-break: break-all;">{verification_url}</a>
            </p>
            <p style="color: #94a3b8; font-size: 13px;">This link expires in 24 hours.</p>
        </div>
    </body>
    </html>
    """

    text_body = (
        f"Welcome to SimuPharma, {user_name}!\n\n"
        f"Please verify your email by visiting:\n{verification_url}\n\n"
        f"This link expires in 24 hours."
    )

    return _send_email(to_email, subject, html_body, text_body)


def send_password_reset_email(to_email: str, token: str, user_name: str = "User") -> bool:
    """Send password reset link."""
    reset_url = f"{FRONTEND_URL}/reset-password?token={token}"
    subject = "SimuPharma — Reset Your Password"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: 'Inter', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f8fafc;">
        <div style="background: linear-gradient(135deg, #2563EB, #7C3AED); padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">🧪 SimuPharma</h1>
            <p style="color: rgba(255,255,255,0.9); margin-top: 8px; font-size: 14px;">Virtual Pharmaceutical Laboratory</p>
        </div>
        <div style="background: white; padding: 30px; border-radius: 0 0 12px 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h2 style="color: #1e293b; margin-top: 0;">Password Reset Request</h2>
            <p style="color: #475569; line-height: 1.6;">
                Hi {user_name}, we received a request to reset your password.
                Click the button below to set a new password.
            </p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_url}"
                   style="background: linear-gradient(135deg, #2563EB, #7C3AED); color: white; padding: 14px 32px;
                          border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 16px;
                          display: inline-block;">
                    Reset Password
                </a>
            </div>
            <p style="color: #94a3b8; font-size: 13px;">
                If the button doesn't work, copy and paste this link:<br>
                <a href="{reset_url}" style="color: #2563EB; word-break: break-all;">{reset_url}</a>
            </p>
            <p style="color: #94a3b8; font-size: 13px;">
                This link expires in 1 hour. If you didn't request this, you can safely ignore this email.
            </p>
        </div>
    </body>
    </html>
    """

    text_body = (
        f"Hi {user_name},\n\n"
        f"You requested a password reset. Visit this link:\n{reset_url}\n\n"
        f"This link expires in 1 hour. If you didn't request this, ignore this email."
    )

    return _send_email(to_email, subject, html_body, text_body)
