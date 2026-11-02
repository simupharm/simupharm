"""Experiments Router — CRUD for experiment history and logging."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from ..models import Experiment
from ..auth.router import get_current_user, require_user

router = APIRouter(prefix="/experiments", tags=["Experiments"])


class ExperimentCreate(BaseModel):
    instrument: str
    compound_name: str = ""
    parameters: dict = {}
    results: dict = {}
    notes: str = ""


class ExperimentResponse(BaseModel):
    id: int
    instrument: str
    compound_name: str
    parameters: dict
    results: dict
    notes: str
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("", response_model=ExperimentResponse)
def create_experiment(req: ExperimentCreate, user=Depends(require_user), db: Session = Depends(get_db)):
    """Log a new experiment (requires auth)."""
    experiment = Experiment(
        user_id=user.id,
        instrument=req.instrument,
        compound_name=req.compound_name,
        parameters=req.parameters,
        results=req.results,
        notes=req.notes,
    )
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    return experiment


@router.get("")
def list_experiments(
    instrument: str = "",
    limit: int = 50,
    user=Depends(require_user),
    db: Session = Depends(get_db)
):
    """Get experiment history for the current user."""
    query = db.query(Experiment).filter(Experiment.user_id == user.id)
    if instrument:
        query = query.filter(Experiment.instrument == instrument)
    experiments = query.order_by(Experiment.created_at.desc()).limit(limit).all()
    return {"count": len(experiments), "experiments": experiments}


@router.get("/{experiment_id}")
def get_experiment(experiment_id: int, user=Depends(require_user), db: Session = Depends(get_db)):
    """Get a single experiment by ID."""
    exp = db.query(Experiment).filter(
        Experiment.id == experiment_id, Experiment.user_id == user.id
    ).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp
