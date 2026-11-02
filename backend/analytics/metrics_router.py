"""Public Metrics API — Platform Usage Statistics

Provides aggregate, non-PII metrics for demonstrating traction.
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import User, Experiment, QuizResult, Progress

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get("/public")
def public_metrics(db: Session = Depends(get_db)):
    """Get aggregate platform metrics (no auth required)."""

    total_users = db.query(func.count(User.id)).scalar() or 0
    total_simulations = db.query(func.count(Experiment.id)).scalar() or 0
    total_quizzes = db.query(func.count(QuizResult.id)).scalar() or 0

    # Active users last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    active_7d = db.query(func.count(func.distinct(Experiment.user_id))).filter(
        Experiment.created_at >= week_ago
    ).scalar() or 0

    # Instrument usage breakdown
    instrument_counts = db.query(
        Experiment.instrument, func.count(Experiment.id)
    ).group_by(Experiment.instrument).all()
    instrument_usage = {row[0]: row[1] for row in instrument_counts}

    # Avg mastery across all users
    avg_mastery = db.query(func.avg(Progress.mastery_level)).scalar()

    # Pro subscribers
    pro_count = db.query(func.count(User.id)).filter(User.plan != "free").scalar() or 0

    # Institutions represented
    institutions = db.query(func.count(func.distinct(User.institution))).filter(
        User.institution != "", User.institution.isnot(None)
    ).scalar() or 0

    return {
        "platform": "SimuPharma",
        "total_registered_users": total_users,
        "active_users_7d": active_7d,
        "total_simulations_run": total_simulations,
        "total_quizzes_completed": total_quizzes,
        "pro_subscribers": pro_count,
        "institutions_represented": institutions,
        "instrument_usage": instrument_usage,
        "avg_mastery_pct": round(float(avg_mastery or 0) * 100, 1),
        "instruments_available": 7,
        "ai_features": ["Autonomous Lab Agent", "Adaptive Learning", "Spectral Matching", "Knowledge Graph"],
        "updated_at": datetime.utcnow().isoformat(),
    }
