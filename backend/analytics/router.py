"""Analytics Router — Progress tracking, stats, leaderboard, quiz results."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from ..models import Progress, QuizResult, Experiment, User
from ..auth.router import require_user, get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


class QuizSubmit(BaseModel):
    instrument: str = "general"
    score: float
    total_questions: int
    time_taken_seconds: int = 0


class ProgressUpdate(BaseModel):
    instrument: str
    time_spent_minutes: int = 0
    simulations_run: int = 0


@router.post("/quiz-result")
def submit_quiz(req: QuizSubmit, user=Depends(require_user), db: Session = Depends(get_db)):
    """Save a quiz result."""
    result = QuizResult(
        user_id=user.id,
        instrument=req.instrument,
        score=req.score,
        total_questions=req.total_questions,
        time_taken_seconds=req.time_taken_seconds,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return {"id": result.id, "score": result.score, "message": "Quiz result saved"}


@router.post("/progress")
def update_progress(req: ProgressUpdate, user=Depends(require_user), db: Session = Depends(get_db)):
    """Update learning progress for an instrument."""
    progress = db.query(Progress).filter(
        Progress.user_id == user.id, Progress.instrument == req.instrument
    ).first()

    if not progress:
        progress = Progress(user_id=user.id, instrument=req.instrument)
        db.add(progress)

    progress.time_spent_minutes += req.time_spent_minutes
    progress.simulations_run += req.simulations_run
    progress.last_accessed = datetime.utcnow()

    # Calculate mastery based on time + simulations
    mastery = min(1.0, (progress.time_spent_minutes / 60 + progress.simulations_run * 0.1) / 5)
    progress.mastery_level = round(mastery, 3)

    db.commit()
    return {"instrument": req.instrument, "mastery": progress.mastery_level, "total_time": progress.time_spent_minutes}


@router.get("/progress")
def get_progress(user=Depends(require_user), db: Session = Depends(get_db)):
    """Get learning progress across all instruments."""
    progress = db.query(Progress).filter(Progress.user_id == user.id).all()
    return {
        "instruments": [
            {
                "instrument": p.instrument,
                "mastery_level": p.mastery_level,
                "time_spent_minutes": p.time_spent_minutes,
                "simulations_run": p.simulations_run,
                "last_accessed": p.last_accessed.isoformat() if p.last_accessed else None
            }
            for p in progress
        ]
    }


@router.get("/stats")
def get_stats(user=Depends(require_user), db: Session = Depends(get_db)):
    """Get overall statistics for the current user."""
    # Total experiments
    exp_count = db.query(func.count(Experiment.id)).filter(Experiment.user_id == user.id).scalar()

    # Quiz stats
    quiz_count = db.query(func.count(QuizResult.id)).filter(QuizResult.user_id == user.id).scalar()
    avg_score = db.query(func.avg(QuizResult.score)).filter(QuizResult.user_id == user.id).scalar()

    # Total time
    total_time = db.query(func.sum(Progress.time_spent_minutes)).filter(Progress.user_id == user.id).scalar()

    # Instruments explored
    instruments = db.query(func.count(func.distinct(Progress.instrument))).filter(Progress.user_id == user.id).scalar()

    return {
        "experiments_run": exp_count or 0,
        "quizzes_completed": quiz_count or 0,
        "average_score": round(avg_score or 0, 1),
        "total_time_minutes": total_time or 0,
        "instruments_explored": instruments or 0,
    }


@router.get("/leaderboard")
def get_leaderboard(db: Session = Depends(get_db)):
    """Get top students by quiz scores (public endpoint)."""
    results = db.query(
        User.name,
        func.count(QuizResult.id).label("quizzes"),
        func.avg(QuizResult.score).label("avg_score"),
        func.sum(Progress.time_spent_minutes).label("total_time")
    ).join(QuizResult, User.id == QuizResult.user_id, isouter=True) \
     .join(Progress, User.id == Progress.user_id, isouter=True) \
     .group_by(User.id) \
     .order_by(func.avg(QuizResult.score).desc()) \
     .limit(20).all()

    return {
        "leaderboard": [
            {
                "name": r.name,
                "quizzes": r.quizzes or 0,
                "average_score": round(r.avg_score or 0, 1),
                "total_time_minutes": r.total_time or 0
            }
            for r in results
        ]
    }
