"""Leaderboard API — Real Student Rankings

Replaces the fake client-side leaderboard with real database-backed rankings.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import User, Experiment, QuizResult, Progress

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("")
def get_leaderboard(limit: int = 20, db: Session = Depends(get_db)):
    """Get top students by mastery score."""

    # Aggregate mastery per user
    results = db.query(
        User.id,
        User.name,
        User.institution,
        func.avg(Progress.mastery_level).label("avg_mastery"),
        func.sum(Progress.simulations_run).label("total_sims"),
    ).join(Progress, Progress.user_id == User.id).filter(
        User.role == "student",
    ).group_by(User.id, User.name, User.institution).order_by(
        func.avg(Progress.mastery_level).desc()
    ).limit(limit).all()

    leaderboard = []
    for rank, row in enumerate(results, 1):
        # Get quiz stats
        quiz_count = db.query(func.count(QuizResult.id)).filter(
            QuizResult.user_id == row.id
        ).scalar() or 0

        # Anonymize: First name + last initial
        name_parts = (row.name or "Student").split()
        display_name = name_parts[0]
        if len(name_parts) > 1:
            display_name += f" {name_parts[-1][0]}."

        leaderboard.append({
            "rank": rank,
            "name": display_name,
            "institution": row.institution or "",
            "avg_mastery_pct": round(float(row.avg_mastery or 0) * 100, 1),
            "total_simulations": int(row.total_sims or 0),
            "quizzes_completed": quiz_count,
        })

    return {
        "leaderboard": leaderboard,
        "total_students": len(leaderboard),
    }
