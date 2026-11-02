"""Billing Router — Plans, Subscriptions, Payment Verification.

Uses Razorpay's flow:
1. GET /plans → list available plans
2. POST /create-subscription → creates Razorpay subscription, returns sub_id + checkout config
3. POST /verify-payment → verifies Razorpay signature after frontend checkout
4. GET /subscription → current plan status
5. POST /cancel → cancel subscription
6. GET /invoices → payment history
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models import User, Subscription
from ..auth.router import require_user
from ..config import RAZORPAY_KEY_ID
from ..logging_config import get_logger
from .razorpay_service import (
    PLANS, is_razorpay_configured, create_subscription,
    verify_subscription_signature, get_subscription_details,
    cancel_subscription, get_payments,
)

router = APIRouter(prefix="/billing", tags=["Billing"])
logger = get_logger(__name__)


# ---- Schemas ----
class CreateSubscriptionRequest(BaseModel):
    plan: str = "pro"
    billing_period: str = "monthly"  # monthly, semester, annual


class VerifyPaymentRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_subscription_id: str
    razorpay_signature: str


# ---- Endpoints ----

@router.get("/plans")
def get_plans():
    """Get available pricing plans with feature comparison."""
    return {
        "plans": [
            {
                "id": "free",
                "name": PLANS["free"]["name"],
                "price_label": "Free",
                "currency": "INR",
                "instruments": PLANS["free"]["instruments"],
                "daily_simulation_limit": PLANS["free"]["daily_simulation_limit"],
                "quiz_limit_monthly": PLANS["free"]["quiz_limit_monthly"],
                "features": PLANS["free"]["features"],
                "restricted": PLANS["free"]["restricted"],
            },
            {
                "id": "pro",
                "name": PLANS["pro"]["name"],
                "prices": {
                    "monthly": {"amount": 19900, "label": "₹199/month"},
                    "semester": {"amount": 79900, "label": "₹799/semester", "per_month": "₹133/mo"},
                    "annual": {"amount": 129900, "label": "₹1,299/year", "per_month": "₹108/mo"},
                },
                "currency": "INR",
                "instruments": PLANS["pro"]["instruments"],
                "daily_simulation_limit": None,
                "quiz_limit_monthly": None,
                "features": PLANS["pro"]["features"],
            },
            {
                "id": "institution_starter",
                "name": "Institution Starter",
                "price_label": "₹50,000/year",
                "max_students": 100,
                "per_student": "₹500/student",
                "currency": "INR",
            },
            {
                "id": "institution_standard",
                "name": "Institution Standard",
                "price_label": "₹1,20,000/year",
                "max_students": 300,
                "per_student": "₹400/student",
                "currency": "INR",
            },
            {
                "id": "institution_premium",
                "name": "Institution Premium",
                "price_label": "₹3,00,000/year",
                "max_students": 1000,
                "per_student": "₹300/student",
                "currency": "INR",
            },
        ],
        "razorpay_configured": is_razorpay_configured(),
        "razorpay_key_id": RAZORPAY_KEY_ID if is_razorpay_configured() else None,
    }


@router.post("/create-subscription")
def create_user_subscription(
    req: CreateSubscriptionRequest,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Create a Razorpay Subscription for upgrading to Pro.

    Returns subscription_id and Razorpay key for frontend checkout.
    """
    # Validate input first
    if req.plan not in ("pro",):
        raise HTTPException(status_code=400, detail="Invalid plan. Use 'pro' for individual subscriptions.")

    if req.billing_period not in ("monthly", "semester", "annual"):
        raise HTTPException(status_code=400, detail="Invalid billing period. Use monthly, semester, or annual.")

    if not is_razorpay_configured():
        raise HTTPException(status_code=503, detail="Payment system not configured")

    # Get the Razorpay Plan ID
    plan_prices = PLANS["pro"]["prices"]
    price_info = plan_prices.get(req.billing_period)
    if not price_info or not price_info["razorpay_plan_id"]:
        raise HTTPException(
            status_code=503,
            detail=f"Plan ID not configured for {req.billing_period}. Set RAZORPAY_PLAN_PRO_{req.billing_period.upper()} in .env."
        )

    # Create Razorpay subscription
    result = create_subscription(
        plan_id=price_info["razorpay_plan_id"],
        user_email=user.email,
        user_name=user.name,
    )
    if not result:
        raise HTTPException(status_code=502, detail="Failed to create subscription")

    # Store pending subscription record
    sub = Subscription(
        user_id=user.id,
        razorpay_subscription_id=result["subscription_id"],
        plan="pro",
        status="pending",
        billing_period=req.billing_period,
        amount=price_info["amount"],
        currency="INR",
    )
    db.add(sub)
    db.commit()

    return {
        "subscription_id": result["subscription_id"],
        "razorpay_key_id": RAZORPAY_KEY_ID,
        "amount": price_info["amount"],
        "currency": "INR",
        "name": "SimuPharma Pro",
        "description": f"Student Pro — {req.billing_period}",
        "prefill": {
            "name": user.name,
            "email": user.email,
        },
    }


@router.post("/verify-payment")
def verify_payment(
    req: VerifyPaymentRequest,
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Verify Razorpay payment after frontend checkout completes.

    This is called by the frontend after Razorpay.js checkout succeeds.
    Verifies the signature and activates the subscription.
    """
    # Verify signature
    is_valid = verify_subscription_signature(
        subscription_id=req.razorpay_subscription_id,
        payment_id=req.razorpay_payment_id,
        signature=req.razorpay_signature,
    )

    if not is_valid:
        raise HTTPException(status_code=400, detail="Payment signature verification failed")

    # Activate user's plan
    user.plan = "pro"
    user.razorpay_subscription_id = req.razorpay_subscription_id

    # Update subscription record
    sub = db.query(Subscription).filter(
        Subscription.razorpay_subscription_id == req.razorpay_subscription_id
    ).first()
    if sub:
        sub.status = "active"
        sub.razorpay_checkout_session_id = req.razorpay_payment_id

    db.commit()

    logger.info(
        f"User {user.email} upgraded to Pro via Razorpay",
        extra={"user_id": user.id, "subscription_id": req.razorpay_subscription_id}
    )

    return {
        "message": "Payment verified! Your Pro plan is now active.",
        "plan": "pro",
    }


@router.get("/subscription")
def get_subscription_status(
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Get current subscription status for the authenticated user."""
    result = {
        "plan": user.plan,
        "plan_name": PLANS.get(user.plan, {}).get("name", user.plan.title()),
        "is_paid": user.plan != "free",
        "instruments": PLANS.get(user.plan, PLANS["pro"]).get("instruments", PLANS["pro"]["instruments"]),
        "daily_simulation_limit": PLANS.get(user.plan, {}).get("daily_simulation_limit"),
        "simulations_today": user.daily_simulation_count,
        "razorpay_subscription_id": user.razorpay_subscription_id,
        "expires_at": user.plan_expires_at.isoformat() if user.plan_expires_at else None,
    }

    # Fetch live status from Razorpay if available
    if user.razorpay_subscription_id and is_razorpay_configured():
        rz_sub = get_subscription_details(user.razorpay_subscription_id)
        if rz_sub:
            result["razorpay_status"] = rz_sub["status"]
            result["paid_count"] = rz_sub["paid_count"]

    return result


@router.post("/cancel")
def cancel_user_subscription(
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Cancel the current subscription (at cycle end)."""
    if user.plan == "free":
        raise HTTPException(status_code=400, detail="No active subscription to cancel")

    if not user.razorpay_subscription_id:
        raise HTTPException(status_code=400, detail="No subscription found")

    success = cancel_subscription(user.razorpay_subscription_id)
    if not success:
        raise HTTPException(status_code=502, detail="Failed to cancel subscription")

    logger.info(f"Subscription canceled for user {user.email}", extra={"user_id": user.id})
    return {"message": "Subscription will be canceled at the end of the current billing cycle."}


@router.get("/invoices")
def get_user_invoices(
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """Get payment history for the authenticated user."""
    if not user.razorpay_subscription_id:
        return {"invoices": []}

    # Get from DB records
    subs = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.status == "active",
    ).order_by(Subscription.created_at.desc()).limit(10).all()

    invoices = [
        {
            "id": s.id,
            "plan": s.plan,
            "amount": s.amount,
            "currency": s.currency,
            "status": s.status,
            "billing_period": s.billing_period,
            "created_at": s.created_at.isoformat() if s.created_at else None,
        }
        for s in subs
    ]

    return {"invoices": invoices}
