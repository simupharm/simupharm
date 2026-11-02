"""Feature Gate Middleware — Plan-based access control and simulation limits.

Controls which features and instruments are available based on user's
subscription plan. Enforces daily simulation limits for free users.
"""
from datetime import date
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..auth.router import require_user
from ..logging_config import get_logger
from ..billing.razorpay_service import FREE_INSTRUMENTS, ALL_INSTRUMENTS, FREE_DAILY_LIMIT

logger = get_logger(__name__)


def require_plan(*allowed_plans: str):
    """Dependency that requires user to be on one of the allowed plans.

    Usage:
        @router.get("/pro-feature")
        def pro_feature(user=Depends(require_plan("pro", "institution"))):
            ...
    """
    async def plan_checker(user: User = Depends(require_user)) -> User:
        # Map institution sub-plans to base plan check
        effective_plan = user.plan
        if effective_plan.startswith("institution"):
            effective_plan = "institution"

        if effective_plan not in allowed_plans and user.plan not in allowed_plans:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "upgrade_required",
                    "message": f"This feature requires a {' or '.join(allowed_plans)} plan.",
                    "current_plan": user.plan,
                    "upgrade_url": "/pricing.html",
                }
            )
        return user
    return plan_checker


# Pre-built plan dependencies
require_pro = require_plan("pro", "institution", "institution_starter", "institution_standard", "institution_premium")
require_institution = require_plan("institution", "institution_starter", "institution_standard", "institution_premium")


def get_allowed_instruments(user: User) -> list[str]:
    """Get list of instruments the user can access based on their plan."""
    if user.plan == "free":
        return FREE_INSTRUMENTS
    return ALL_INSTRUMENTS


def check_instrument_access(instrument: str):
    """Dependency that checks if user can access a specific instrument.

    Usage:
        @router.post("/simulate/hplc")
        def simulate_hplc(user=Depends(check_instrument_access("hplc"))):
            ...
    """
    async def checker(user: User = Depends(require_user), db: Session = Depends(get_db)) -> User:
        allowed = get_allowed_instruments(user)
        if instrument not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "instrument_locked",
                    "message": f"The {instrument.upper()} instrument requires a Pro plan.",
                    "instrument": instrument,
                    "current_plan": user.plan,
                    "allowed_instruments": allowed,
                    "upgrade_url": "/pricing.html",
                }
            )
        return user
    return checker


async def check_simulation_limit(
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> User:
    """Check and enforce daily simulation limits for free users.

    Pro/institution users have unlimited simulations.
    Free users get 5 simulations per day.
    """
    if user.plan != "free":
        return user  # Unlimited for paid users

    today = date.today().isoformat()

    # Reset counter if it's a new day
    if user.last_simulation_date != today:
        user.daily_simulation_count = 0
        user.last_simulation_date = today
        db.commit()

    if user.daily_simulation_count >= FREE_DAILY_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "daily_limit_reached",
                "message": f"Free plan allows {FREE_DAILY_LIMIT} simulations per day. Upgrade to Pro for unlimited.",
                "daily_limit": FREE_DAILY_LIMIT,
                "simulations_used": user.daily_simulation_count,
                "upgrade_url": "/pricing.html",
            }
        )

    return user


async def increment_simulation_count(
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
) -> User:
    """Increment the daily simulation counter after a successful simulation."""
    today = date.today().isoformat()
    if user.last_simulation_date != today:
        user.daily_simulation_count = 1
        user.last_simulation_date = today
    else:
        user.daily_simulation_count += 1
    db.commit()
    return user
