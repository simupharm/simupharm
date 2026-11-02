"""Razorpay Webhook Handler — Processes Razorpay events for subscription lifecycle.

Razorpay webhooks are signed with HMAC SHA256.
Events: subscription.activated, subscription.charged, subscription.completed,
        subscription.cancelled, subscription.halted, payment.captured, etc.
"""
import json
import hmac
import hashlib
from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..config import RAZORPAY_WEBHOOK_SECRET
from ..database import SessionLocal
from ..models import User, Subscription
from ..logging_config import get_logger

router = APIRouter(tags=["Webhooks"])
logger = get_logger(__name__)


def _verify_signature(body: bytes, signature: str) -> bool:
    """Verify Razorpay webhook HMAC SHA256 signature."""
    if not RAZORPAY_WEBHOOK_SECRET:
        return True  # Dev mode — skip verification
    expected = hmac.new(
        RAZORPAY_WEBHOOK_SECRET.encode("utf-8"),
        body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/billing/webhook")
async def razorpay_webhook(request: Request):
    """Handle Razorpay webhook events."""
    payload = await request.body()
    signature = request.headers.get("x-razorpay-signature", "")

    if not _verify_signature(payload, signature):
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    try:
        event = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    event_type = event.get("event", "")
    event_payload = event.get("payload", {})

    logger.info(f"Razorpay webhook: {event_type}")

    db = SessionLocal()
    try:
        if event_type == "subscription.activated":
            _handle_subscription_activated(db, event_payload)
        elif event_type == "subscription.charged":
            _handle_subscription_charged(db, event_payload)
        elif event_type in ("subscription.cancelled", "subscription.completed"):
            _handle_subscription_ended(db, event_payload)
        elif event_type == "subscription.halted":
            _handle_subscription_halted(db, event_payload)
        elif event_type == "payment.captured":
            _handle_payment_captured(db, event_payload)
        else:
            logger.info(f"Unhandled Razorpay event: {event_type}")
    finally:
        db.close()

    return {"status": "ok"}


def _get_user_by_subscription(db: Session, subscription_id: str) -> User | None:
    """Find user by Razorpay subscription ID."""
    return db.query(User).filter(User.razorpay_subscription_id == subscription_id).first()


def _handle_subscription_activated(db: Session, payload: dict):
    """Subscription is now active — ensure user has pro access."""
    sub_entity = payload.get("subscription", {}).get("entity", {})
    subscription_id = sub_entity.get("id")
    if not subscription_id:
        return

    user = _get_user_by_subscription(db, subscription_id)
    if not user:
        logger.warning(f"Subscription activated but user not found: {subscription_id}")
        return

    user.plan = "pro"

    current_end = sub_entity.get("current_end")
    if current_end:
        user.plan_expires_at = datetime.fromtimestamp(current_end)

    db.commit()
    logger.info(f"Subscription activated for {user.email}")


def _handle_subscription_charged(db: Session, payload: dict):
    """Recurring payment succeeded — extend plan."""
    sub_entity = payload.get("subscription", {}).get("entity", {})
    subscription_id = sub_entity.get("id")
    if not subscription_id:
        return

    user = _get_user_by_subscription(db, subscription_id)
    if not user:
        return

    user.plan = "pro"
    current_end = sub_entity.get("current_end")
    if current_end:
        user.plan_expires_at = datetime.fromtimestamp(current_end)

    db.commit()
    logger.info(f"Subscription charged for {user.email}")


def _handle_subscription_ended(db: Session, payload: dict):
    """Subscription cancelled or completed — downgrade to free."""
    sub_entity = payload.get("subscription", {}).get("entity", {})
    subscription_id = sub_entity.get("id")
    if not subscription_id:
        return

    user = _get_user_by_subscription(db, subscription_id)
    if not user:
        return

    user.plan = "free"
    user.razorpay_subscription_id = None
    user.plan_expires_at = None

    sub = db.query(Subscription).filter(
        Subscription.razorpay_subscription_id == subscription_id
    ).first()
    if sub:
        sub.status = "canceled"
        sub.canceled_at = datetime.utcnow()

    db.commit()
    logger.info(f"Subscription ended for {user.email}")


def _handle_subscription_halted(db: Session, payload: dict):
    """Payment failed repeatedly — subscription paused."""
    sub_entity = payload.get("subscription", {}).get("entity", {})
    subscription_id = sub_entity.get("id")
    if not subscription_id:
        return

    user = _get_user_by_subscription(db, subscription_id)
    if user:
        logger.warning(f"Subscription halted for {user.email} — payment failures")


def _handle_payment_captured(db: Session, payload: dict):
    """Individual payment captured — log it."""
    payment = payload.get("payment", {}).get("entity", {})
    logger.info(
        f"Payment captured: {payment.get('id')} — ₹{payment.get('amount', 0) / 100}"
    )
