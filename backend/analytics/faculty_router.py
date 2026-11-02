"""Faculty Dashboard API — Institution Analytics & Student Tracking

Provides endpoints for faculty/admin to:
- View aggregate institution usage stats
- Track individual student progress
- Generate NAAC/NBA accreditation reports
- Export usage reports
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import User, Experiment, QuizResult, Progress
from ..auth.router import get_current_user

router = APIRouter(prefix="/faculty", tags=["Faculty"])


def require_instructor(current_user: User = Depends(get_current_user)):
    """Ensure the current user is an instructor or admin."""
    if current_user.role not in ("instructor", "admin"):
        raise HTTPException(status_code=403, detail="Faculty access required")
    return current_user


@router.get("/dashboard")
def faculty_dashboard(
    db: Session = Depends(get_db),
    user: User = Depends(require_instructor),
):
    """Get the faculty dashboard with aggregate institution stats."""
    institution = user.institution or ""

    # Get all students at this institution
    students_query = db.query(User).filter(
        User.institution == institution,
        User.role == "student",
    )
    students = students_query.all()
    student_ids = [s.id for s in students]

    total_students = len(student_ids)

    # Aggregate stats
    total_simulations = 0
    total_quizzes = 0
    avg_mastery = 0.0
    instrument_usage = {}

    if student_ids:
        # Total simulations
        total_simulations = db.query(func.count(Experiment.id)).filter(
            Experiment.user_id.in_(student_ids)
        ).scalar() or 0

        # Total quizzes
        total_quizzes = db.query(func.count(QuizResult.id)).filter(
            QuizResult.user_id.in_(student_ids)
        ).scalar() or 0

        # Average mastery
        avg_result = db.query(func.avg(Progress.mastery_level)).filter(
            Progress.user_id.in_(student_ids)
        ).scalar()
        avg_mastery = round(float(avg_result or 0), 3)

        # Instrument usage breakdown
        instrument_counts = db.query(
            Experiment.instrument, func.count(Experiment.id)
        ).filter(
            Experiment.user_id.in_(student_ids)
        ).group_by(Experiment.instrument).all()

        instrument_usage = {row[0]: row[1] for row in instrument_counts}

    # Active students (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    active_students = db.query(func.count(func.distinct(Experiment.user_id))).filter(
        Experiment.user_id.in_(student_ids) if student_ids else False,
        Experiment.created_at >= week_ago,
    ).scalar() or 0

    # Student list with mastery
    student_list = []
    for student in students[:100]:  # Cap at 100
        progress_records = db.query(Progress).filter(
            Progress.user_id == student.id
        ).all()

        mastery_map = {}
        total_sims = 0
        for p in progress_records:
            mastery_map[p.instrument] = round(p.mastery_level, 3)
            total_sims += p.simulations_run

        quiz_count = db.query(func.count(QuizResult.id)).filter(
            QuizResult.user_id == student.id
        ).scalar() or 0

        avg_quiz_score = db.query(func.avg(QuizResult.score)).filter(
            QuizResult.user_id == student.id
        ).scalar()

        student_list.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "plan": student.plan,
            "mastery": mastery_map,
            "avg_mastery": round(sum(mastery_map.values()) / max(len(mastery_map), 1), 3),
            "simulations_run": total_sims,
            "quizzes_completed": quiz_count,
            "avg_quiz_score": round(float(avg_quiz_score or 0), 1),
            "last_active": student.created_at.isoformat() if student.created_at else None,
        })

    # Sort by avg mastery descending
    student_list.sort(key=lambda s: s["avg_mastery"], reverse=True)

    return {
        "institution": institution,
        "faculty_name": user.name,
        "total_students": total_students,
        "active_students_7d": active_students,
        "total_simulations": total_simulations,
        "total_quizzes": total_quizzes,
        "avg_mastery": avg_mastery,
        "instrument_usage": instrument_usage,
        "students": student_list,
        "generated_at": datetime.utcnow().isoformat(),
    }


@router.get("/report/naac")
def naac_report(
    db: Session = Depends(get_db),
    user: User = Depends(require_instructor),
):
    """Generate NAAC/NBA accreditation report data.

    Maps to:
    - Criterion 2: Teaching-Learning (2.3 Teaching-Learning Process)
    - Criterion 4: Infrastructure (4.1 Physical Facilities, 4.3 IT Infrastructure)
    """
    institution = user.institution or ""

    students = db.query(User).filter(
        User.institution == institution,
        User.role == "student",
    ).all()
    student_ids = [s.id for s in students]

    # Instrument labels
    instrument_labels = {
        "uvvis": "UV-Vis Spectrophotometer",
        "ftir": "FTIR Spectrophotometer",
        "hplc": "High Performance Liquid Chromatography",
        "gc": "Gas Chromatograph",
        "mass_spec": "Mass Spectrometer",
        "polarimeter": "Polarimeter",
        "psa": "Particle Size Analyzer",
    }

    # Instrument-wise stats
    instrument_stats = {}
    if student_ids:
        for inst_id, inst_name in instrument_labels.items():
            sim_count = db.query(func.count(Experiment.id)).filter(
                Experiment.user_id.in_(student_ids),
                Experiment.instrument == inst_id,
            ).scalar() or 0

            unique_users = db.query(func.count(func.distinct(Experiment.user_id))).filter(
                Experiment.user_id.in_(student_ids),
                Experiment.instrument == inst_id,
            ).scalar() or 0

            avg_mastery = db.query(func.avg(Progress.mastery_level)).filter(
                Progress.user_id.in_(student_ids),
                Progress.instrument == inst_id,
            ).scalar()

            instrument_stats[inst_id] = {
                "name": inst_name,
                "total_sessions": sim_count,
                "unique_students": unique_users,
                "avg_competency_pct": round(float(avg_mastery or 0) * 100, 1),
                "estimated_lab_hours": round(sim_count * 0.25, 1),  # ~15 min per simulation
            }

    # Total lab hours
    total_lab_hours = sum(s["estimated_lab_hours"] for s in instrument_stats.values())

    # Quiz performance
    total_quizzes = 0
    avg_score = 0.0
    if student_ids:
        total_quizzes = db.query(func.count(QuizResult.id)).filter(
            QuizResult.user_id.in_(student_ids)
        ).scalar() or 0
        avg_score_result = db.query(func.avg(QuizResult.score)).filter(
            QuizResult.user_id.in_(student_ids)
        ).scalar()
        avg_score = round(float(avg_score_result or 0), 1)

    # Student competency summary
    competency_levels = {"Beginner (<30%)": 0, "Intermediate (30-60%)": 0, "Advanced (60-80%)": 0, "Expert (>80%)": 0}
    for student in students:
        progress = db.query(Progress).filter(Progress.user_id == student.id).all()
        if progress:
            avg_m = sum(p.mastery_level for p in progress) / len(progress)
            if avg_m < 0.3:
                competency_levels["Beginner (<30%)"] += 1
            elif avg_m < 0.6:
                competency_levels["Intermediate (30-60%)"] += 1
            elif avg_m < 0.8:
                competency_levels["Advanced (60-80%)"] += 1
            else:
                competency_levels["Expert (>80%)"] += 1
        else:
            competency_levels["Beginner (<30%)"] += 1

    return {
        "report_title": "NAAC/NBA Virtual Laboratory Usage Report",
        "institution": institution,
        "report_generated": datetime.utcnow().isoformat(),
        "reporting_period": {
            "from": (datetime.utcnow() - timedelta(days=365)).strftime("%Y-%m-%d"),
            "to": datetime.utcnow().strftime("%Y-%m-%d"),
        },
        "criterion_2_teaching_learning": {
            "description": "Integration of ICT-enabled virtual laboratory tools for pharmaceutical education",
            "platform": "SimuPharma — AI-Powered Virtual Pharmaceutical Laboratory",
            "total_students_enrolled": len(students),
            "total_virtual_lab_sessions": sum(s["total_sessions"] for s in instrument_stats.values()),
            "total_virtual_lab_hours": total_lab_hours,
            "instruments_available": len(instrument_stats),
            "instrument_details": instrument_stats,
            "assessment_conducted": total_quizzes,
            "average_assessment_score_pct": avg_score,
        },
        "criterion_4_infrastructure": {
            "description": "Virtual infrastructure complementing physical laboratory facilities",
            "instruments_simulated": [v["name"] for v in instrument_stats.values()],
            "equivalent_physical_lab_cost_inr": "₹2.2 Crore (7 instruments)",
            "virtual_lab_annual_cost_inr": "₹50,000 – ₹3,00,000 (depending on plan)",
            "cost_savings_pct": 97,
            "access_hours": "24/7 (browser-based, any device)",
            "ai_features": [
                "Autonomous AI Lab Agent for experiment planning",
                "Adaptive learning with Bayesian Knowledge Tracing",
                "Multi-instrument spectral matching for compound identification",
                "Pharmaceutical knowledge graph for personalized learning paths",
            ],
        },
        "student_competency_distribution": competency_levels,
        "recommendations": [
            "Continue virtual lab integration for enhanced learning outcomes",
            "Use adaptive learning data to identify students needing additional support",
            "Leverage AI Lab Agent for advanced research-oriented practicals",
        ],
    }
