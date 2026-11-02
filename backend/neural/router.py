"""
Neural AI Router — API Endpoints for the Autonomous Lab Agent & Adaptive Learning Engine

Exposes the neural AI capabilities as REST endpoints:
- Lab Agent: Plan, execute, and analyze experiments autonomously
- Adaptive Engine: Student mastery tracking, difficulty adjustment, learning paths
- Knowledge Graph: Concept relationships and gap analysis
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from .lab_agent import lab_agent
from .adaptive_engine import adaptive_engine
from .knowledge_graph import pharma_concepts


router = APIRouter(prefix="/neural", tags=["Neural AI"])


# ========================================================================
# REQUEST MODELS
# ========================================================================

class AgentPlanRequest(BaseModel):
    goal: str
    compound_ids: list[str] = []

class AgentExecuteToolRequest(BaseModel):
    tool_name: str
    arguments: dict = {}

class MasteryUpdateRequest(BaseModel):
    user_id: int = 1
    instrument: str
    score: float
    concepts: list[str] = []
    activity_type: str = "simulation"

class LearningPathRequest(BaseModel):
    target_concept: str = "drug_quality_testing"
    user_id: Optional[int] = None


# ========================================================================
# LAB AGENT ENDPOINTS — Autonomous Experiment Planning & Execution
# ========================================================================

@router.post("/agent/plan")
def plan_experiment(req: AgentPlanRequest):
    """Generate an experiment plan from a research goal.
    
    The agent analyzes your goal and creates a step-by-step plan
    selecting the optimal instruments and analysis sequence.
    
    Examples:
    - "Identify an unknown white powder" → UV-Vis + FTIR + MS + ML identification
    - "Compare aspirin and ibuprofen" → Side-by-side comparison across instruments
    - "Assess drug purity" → HPLC + UV-Vis calibration + FTIR identity
    """
    if not req.goal.strip():
        raise HTTPException(status_code=400, detail="Please provide a research goal")
    
    plan = lab_agent.plan_experiment(req.goal, req.compound_ids or None)
    return plan


@router.post("/agent/execute-tool")
def execute_single_tool(req: AgentExecuteToolRequest):
    """Execute a single lab tool/instrument.
    
    Available tools: search_compound, get_compound_info, run_uvvis, run_ftir,
    run_hplc, run_gc, run_mass_spec, run_polarimeter, run_psa, 
    identify_unknown, compare_compounds
    """
    if req.tool_name not in lab_agent.TOOLS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown tool '{req.tool_name}'. Available: {list(lab_agent.TOOLS.keys())}"
        )
    
    result = lab_agent.execute_tool(req.tool_name, req.arguments)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@router.post("/agent/analyze")
def full_analysis(req: AgentPlanRequest):
    """Plan AND execute a full autonomous analysis.
    
    This is the highest-level endpoint: give it a goal and compound(s),
    and the agent will plan the experiment, run all instruments,
    cross-reference results, and return a comprehensive report.
    
    This is what makes SimuPharma an AUTONOMOUS AI — not just a simulator.
    """
    if not req.goal.strip():
        raise HTTPException(status_code=400, detail="Please provide a research goal")
    
    result = lab_agent.full_analysis(req.goal, req.compound_ids or None)
    return result


@router.get("/agent/tools")
def list_available_tools():
    """List all available tools the agent can use.
    
    Returns tool declarations compatible with Gemini function calling.
    """
    return {
        "tools": lab_agent.get_tool_declarations(),
        "total": len(lab_agent.TOOLS),
        "tool_names": list(lab_agent.TOOLS.keys())
    }


@router.get("/agent/log")
def get_execution_log():
    """Get the agent's recent execution log."""
    return {
        "log": lab_agent.execution_log[-50:],
        "total_executions": len(lab_agent.execution_log)
    }


# ========================================================================
# ADAPTIVE ENGINE ENDPOINTS — Student Mastery & Personalization
# ========================================================================

@router.get("/adaptive/profile/{user_id}")
def get_student_profile(user_id: int):
    """Get a student's full mastery profile.
    
    Shows per-instrument mastery levels, strengths, weaknesses,
    and personalized next-step recommendations.
    """
    profile = adaptive_engine.get_profile(user_id)
    return profile.get_mastery_summary()


@router.post("/adaptive/update")
def update_student_mastery(req: MasteryUpdateRequest):
    """Update a student's mastery after an activity.
    
    Call this after a student runs a simulation, takes a quiz,
    or completes an experiment. The engine updates their mastery
    using Bayesian knowledge tracing and returns updated recommendations.
    """
    if req.instrument not in ["uvvis", "ftir", "hplc", "gc", "mass_spec", "polarimeter", "psa"]:
        raise HTTPException(status_code=400, detail=f"Unknown instrument: {req.instrument}")
    
    if not 0 <= req.score <= 1:
        raise HTTPException(status_code=400, detail="Score must be between 0.0 and 1.0")
    
    result = adaptive_engine.update_mastery(
        user_id=req.user_id,
        instrument=req.instrument,
        score=req.score,
        concepts=req.concepts or None,
        activity_type=req.activity_type
    )
    return result


@router.get("/adaptive/suggest/{user_id}")
def suggest_next_activity(user_id: int):
    """Get AI-recommended next activity for a student.
    
    The engine analyzes the student's mastery state and recommends
    the most impactful next step — considering prerequisites,
    concept gaps, and learning efficiency.
    """
    profile = adaptive_engine.get_profile(user_id)
    return profile.suggest_next_activity()


@router.get("/adaptive/difficulty/{user_id}/{instrument}")
def get_recommended_difficulty(user_id: int, instrument: str):
    """Get the recommended difficulty level for a specific instrument.
    
    Returns beginner/intermediate/advanced/expert/research based on
    the student's current mastery level.
    """
    if instrument not in ["uvvis", "ftir", "hplc", "gc", "mass_spec", "polarimeter", "psa"]:
        raise HTTPException(status_code=400, detail=f"Unknown instrument: {instrument}")
    
    profile = adaptive_engine.get_profile(user_id)
    return profile.get_difficulty(instrument)


# ========================================================================
# KNOWLEDGE GRAPH ENDPOINTS — Concept Map & Learning Paths
# ========================================================================

@router.get("/knowledge/graph")
def get_knowledge_graph():
    """Get the full pharmaceutical knowledge graph.
    
    Returns all concepts and their prerequisite relationships.
    Useful for visualizing the learning map on the dashboard.
    """
    return pharma_concepts.to_dict()


@router.post("/knowledge/learning-path")
def get_learning_path(req: LearningPathRequest):
    """Get the optimal learning path to a target concept.
    
    Returns concepts in prerequisite order (learn these first → then these).
    If a user_id is provided, annotates each concept with their mastery level.
    """
    return adaptive_engine.get_learning_path(req.target_concept, req.user_id)


@router.get("/knowledge/instrument/{instrument}")
def get_instrument_concepts(instrument: str):
    """Get all concepts related to a specific instrument."""
    concepts = pharma_concepts.get_instrument_concepts(instrument)
    if not concepts:
        raise HTTPException(status_code=404, detail=f"No concepts found for instrument: {instrument}")
    return {"instrument": instrument, "concepts": concepts}


@router.get("/knowledge/gaps/{user_id}")
def get_knowledge_gaps(user_id: int, threshold: float = 0.4):
    """Find concept gaps that are blocking a student's progress.
    
    Returns low-mastery concepts sorted by impact (how many downstream
    concepts they're blocking).
    """
    profile = adaptive_engine.get_profile(user_id)
    gaps = pharma_concepts.find_gaps(profile.concept_mastery, threshold)
    return {
        "user_id": user_id,
        "threshold": threshold,
        "gaps": gaps[:20],
        "total_gaps": len(gaps)
    }
