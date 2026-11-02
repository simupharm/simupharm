"""Razorpay Service — Handles all Razorpay API interactions.

Razorpay flow:
1. Backend creates an Order (or Subscription)
2. Frontend opens Razorpay checkout modal with order_id
3. User pays → Razorpay sends payment data to frontend callback
4. Frontend sends payment details to backend for signature verification
5. Backend verifies signature and activates plan

For subscriptions, Razorpay has Plans → Subscriptions → Invoices.
"""
import razorpay
import hmac
import hashlib
from ..config import (
    RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET,
    RAZORPAY_PLAN_PRO_MONTHLY, RAZORPAY_PLAN_PRO_SEMESTER, RAZORPAY_PLAN_PRO_ANNUAL,
    FRONTEND_URL,
)
from ..logging_config import get_logger

logger = get_logger(__name__)

# Initialize Razorpay client
_client = None


def get_client():
    """Lazy-init Razorpay client."""
    global _client
    if _client is None and is_razorpay_configured():
        _client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    return _client


# ---- Plan Constants ----
PLANS = {
    "free": {
        "name": "Student Free",
        "price_monthly": 0,
        "currency": "INR",
        "instruments": ["uvvis", "polarimeter", "psa"],
        "daily_simulation_limit": 5,
        "quiz_limit_monthly": 5,
        "features": [
            "3 instruments (UV-Vis, Polarimeter, PSA)",
            "Basic simulation mode",
            "5 quiz attempts/month",
            "Learning dashboard",
            "Community access",
        ],
        "restricted": [
            "AI Lab Agent",
            "Advanced instruments (HPLC, FTIR, GC, Mass Spec)",
            "ML Compound Identification",
            "Certificates",
            "Adaptive learning paths",
        ],
    },
    "pro": {
        "name": "Student Pro",
        "prices": {
            "monthly": {"amount": 19900, "label": "₹199/month", "razorpay_plan_id": RAZORPAY_PLAN_PRO_MONTHLY},
            "semester": {"amount": 79900, "label": "₹799/semester (₹133/mo)", "razorpay_plan_id": RAZORPAY_PLAN_PRO_SEMESTER},
            "annual": {"amount": 129900, "label": "₹1,299/year (₹108/mo)", "razorpay_plan_id": RAZORPAY_PLAN_PRO_ANNUAL},
        },
        "currency": "INR",
        "instruments": ["uvvis", "ftir", "hplc", "gc", "mass_spec", "polarimeter", "psa"],
        "daily_simulation_limit": None,  # Unlimited
        "quiz_limit_monthly": None,  # Unlimited
        "features": [
            "All 7 instruments",
            "Full parameter control",
            "AI Lab Agent (Gemini)",
            "ML Compound Identification",
            "Unlimited quizzes",
            "PDF Certificate generation",
            "Adaptive learning paths",
            "Knowledge Graph navigation",
            "Priority support",
        ],
    },
    "institution_starter": {
        "name": "Institution Starter",
        "price_annual": 5000000,  # ₹50,000 in paise
        "max_students": 100,
        "currency": "INR",
    },
    "institution_standard": {
        "name": "Institution Standard",
        "price_annual": 12000000,  # ₹1,20,000
        "max_students": 300,
        "currency": "INR",
    },
    "institution_premium": {
        "name": "Institution Premium",
        "price_annual": 30000000,  # ₹3,00,000
        "max_students": 1000,
        "currency": "INR",
    },
}

FREE_INSTRUMENTS = PLANS["free"]["instruments"]
ALL_INSTRUMENTS = PLANS["pro"]["instruments"]
FREE_DAILY_LIMIT = PLANS["free"]["daily_simulation_limit"]


def is_razorpay_configured() -> bool:
    """Check if Razorpay API keys are configured."""
    return bool(RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET
                and RAZORPAY_KEY_ID != "rzp_test_xxx")


def create_subscription(plan_id: str, user_email: str, user_name: str) -> dict | None:
    """Create a Razorpay Subscription.

    Returns dict with subscription_id and short_url for checkout.
    """
    client = get_client()
    if not client or not plan_id:
        return None
    try:
        subscription = client.subscription.create({
            "plan_id": plan_id,
            "total_count": 12,  # Max billing cycles
            "quantity": 1,
            "notify_info": {
                "notify_phone": "",
                "notify_email": user_email,
            },
            "notes": {
                "user_email": user_email,
                "user_name": user_name,
            },
        })
        logger.info(f"Razorpay subscription created: {subscription['id']}")
        return {
            "subscription_id": subscription["id"],
            "short_url": subscription.get("short_url", ""),
        }
    except Exception as e:
        logger.error(f"Razorpay subscription error: {e}")
        return None


def create_order(amount: int, currency: str = "INR", receipt: str = "", notes: dict = None) -> dict | None:
    """Create a one-time Razorpay Order (for non-subscription payments).

    Amount is in paise (₹199 = 19900 paise).
    Returns dict with order_id.
    """
    client = get_client()
    if not client:
        return None
    try:
        order = client.order.create({
            "amount": amount,
            "currency": currency,
            "receipt": receipt,
            "notes": notes or {},
        })
        logger.info(f"Razorpay order created: {order['id']}")
        return {
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
        }
    except Exception as e:
        logger.error(f"Razorpay order error: {e}")
        return None


def verify_payment_signature(order_id: str, payment_id: str, signature: str) -> bool:
    """Verify Razorpay payment signature using HMAC SHA256.

    signature = HMAC_SHA256(order_id + '|' + payment_id, key_secret)
    """
    client = get_client()
    if not client:
        return False
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        })
        return True
    except razorpay.errors.SignatureVerificationError:
        logger.warning(f"Razorpay signature verification failed for order {order_id}")
        return False


def verify_subscription_signature(subscription_id: str, payment_id: str, signature: str) -> bool:
    """Verify Razorpay subscription payment signature.

    signature = HMAC_SHA256(payment_id + '|' + subscription_id, key_secret)
    """
    client = get_client()
    if not client:
        return False
    try:
        client.utility.verify_subscription_payment_signature({
            "razorpay_subscription_id": subscription_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        })
        return True
    except razorpay.errors.SignatureVerificationError:
        logger.warning(f"Razorpay subscription signature failed for {subscription_id}")
        return False


def verify_webhook_signature(body: bytes, signature: str, secret: str) -> bool:
    """Verify Razorpay webhook signature."""
    try:
        expected = hmac.new(
            secret.encode("utf-8"), body, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)
    except Exception:
        return False


def get_subscription_details(subscription_id: str) -> dict | None:
    """Fetch subscription details from Razorpay."""
    client = get_client()
    if not client or not subscription_id:
        return None
    try:
        sub = client.subscription.fetch(subscription_id)
        return {
            "id": sub["id"],
            "plan_id": sub["plan_id"],
            "status": sub["status"],  # created, authenticated, active, pending, halted, cancelled, completed, expired
            "current_start": sub.get("current_start"),
            "current_end": sub.get("current_end"),
            "charge_at": sub.get("charge_at"),
            "total_count": sub.get("total_count"),
            "paid_count": sub.get("paid_count"),
        }
    except Exception as e:
        logger.error(f"Razorpay fetch error: {e}")
        return None


def cancel_subscription(subscription_id: str, cancel_at_cycle_end: bool = True) -> bool:
    """Cancel a Razorpay subscription."""
    client = get_client()
    if not client or not subscription_id:
        return False
    try:
        client.subscription.cancel(subscription_id, {"cancel_at_cycle_end": 1 if cancel_at_cycle_end else 0})
        logger.info(f"Razorpay subscription {subscription_id} canceled")
        return True
    except Exception as e:
        logger.error(f"Razorpay cancel error: {e}")
        return False


def get_payments(subscription_id: str = None, count: int = 10) -> list:
    """Get payment history (invoices equivalent)."""
    client = get_client()
    if not client:
        return []
    try:
        if subscription_id:
            # Get payments for a subscription
            payments = client.subscription.fetch(subscription_id).get("invoices", [])
            return payments[:count]
        return []
    except Exception as e:
        logger.error(f"Razorpay payments error: {e}")
        return []
