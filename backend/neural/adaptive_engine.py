"""
Adaptive Learning Engine — Bayesian Knowledge Tracing & Personalization

Tracks student mastery per concept and instrument, adjusts difficulty,
and recommends next activities based on their knowledge state.
"""
from datetime import datetime
from typing import Optional
from .knowledge_graph import pharma_concepts


# ---- Constants ----
INSTRUMENTS = ["uvvis", "ftir", "hplc", "gc", "mass_spec", "polarimeter", "psa"]

INSTRUMENT_LABELS = {
    "uvvis": "UV-Vis Spectroscopy",
    "ftir": "FTIR Spectroscopy",
    "hplc": "HPLC",
    "gc": "Gas Chromatography",
    "mass_spec": "Mass Spectrometry",
    "polarimeter": "Polarimetry",
    "psa": "Particle Size Analysis"
}

# Difficulty levels map to simulation complexity
DIFFICULTY_LEVELS = {
    1: {"label": "Beginner", "description": "Basic operation, pre-set parameters, guided steps"},
    2: {"label": "Intermediate", "description": "Manual parameter selection, interpretation required"},
    3: {"label": "Advanced", "description": "Troubleshooting, method development, unknowns"},
    4: {"label": "Expert", "description": "Multi-instrument analysis, method validation"},
    5: {"label": "Research", "description": "Open-ended investigation, regulatory compliance"}
}


class StudentProfile:
    """Tracks a student's knowledge state across all instruments and concepts.
    
    Uses Bayesian Knowledge Tracing (simplified as exponential moving average)
    to estimate mastery level from a sequence of correct/incorrect actions.
    """

    def __init__(self, user_id: int):
        self.user_id = user_id
        # Per-instrument mastery (0.0 to 1.0)
        self.instrument_mastery: dict[str, float] = {inst: 0.0 for inst in INSTRUMENTS}
        # Per-concept mastery
        self.concept_mastery: dict[str, float] = {}
        # History of learning events
        self.events: list[dict] = []
        # Total simulations run per instrument
        self.simulations_count: dict[str, int] = {inst: 0 for inst in INSTRUMENTS}
        # Last accessed timestamps
        self.last_accessed: dict[str, Optional[str]] = {inst: None for inst in INSTRUMENTS}

    def update_mastery(self, instrument: str, score: float, 
                       concepts: list[str] = None, activity_type: str = "simulation"):
        """Update mastery after a student action.
        
        Args:
            instrument: Which instrument was used
            score: Performance score (0.0 to 1.0). 
                   For simulations: 1.0 if completed successfully, 0.5 if partial, 0.0 if failed
                   For quizzes: fraction correct
            concepts: List of concept IDs that were exercised
            activity_type: "simulation", "quiz", "tutorial", "experiment"
        """
        if instrument not in INSTRUMENTS:
            return
        
        # Learning rate — how quickly mastery updates
        # Higher for quizzes (more informative), lower for passive activities
        learning_rates = {
            "quiz": 0.3,
            "simulation": 0.2,
            "experiment": 0.25,
            "tutorial": 0.1
        }
        lr = learning_rates.get(activity_type, 0.15)
        
        # Bayesian update (exponential moving average)
        old = self.instrument_mastery[instrument]
        self.instrument_mastery[instrument] = old + lr * (score - old)
        
        # Clamp to [0, 1]
        self.instrument_mastery[instrument] = max(0.0, min(1.0, self.instrument_mastery[instrument]))
        
        # Update concept mastery
        if concepts:
            for concept_id in concepts:
                old_c = self.concept_mastery.get(concept_id, 0.0)
                self.concept_mastery[concept_id] = old_c + lr * (score - old_c)
                self.concept_mastery[concept_id] = max(0.0, min(1.0, self.concept_mastery[concept_id]))
        
        # Track the event
        self.simulations_count[instrument] = self.simulations_count.get(instrument, 0) + 1
        self.last_accessed[instrument] = datetime.utcnow().isoformat()
        
        self.events.append({
            "timestamp": datetime.utcnow().isoformat(),
            "instrument": instrument,
            "activity_type": activity_type,
            "score": score,
            "concepts": concepts or [],
            "mastery_after": self.instrument_mastery[instrument]
        })

    def get_difficulty(self, instrument: str) -> dict:
        """Get the recommended difficulty level for an instrument.
        
        Maps mastery to difficulty:
        0.0-0.2 → Beginner (1)
        0.2-0.4 → Intermediate (2)
        0.4-0.6 → Advanced (3)
        0.6-0.8 → Expert (4)
        0.8-1.0 → Research (5)
        """
        mastery = self.instrument_mastery.get(instrument, 0.0)
        
        if mastery < 0.2:
            level = 1
        elif mastery < 0.4:
            level = 2
        elif mastery < 0.6:
            level = 3
        elif mastery < 0.8:
            level = 4
        else:
            level = 5
        
        return {
            "level": level,
            **DIFFICULTY_LEVELS[level],
            "mastery": round(mastery, 3)
        }

    def suggest_next_activity(self) -> dict:
        """Recommend the best next activity for the student.
        
        Strategy:
        1. Find the instrument with lowest mastery (needs most work)
        2. Check knowledge graph for concept gaps
        3. Prioritize prerequisites over advanced topics
        4. Suggest a specific activity type based on mastery level
        """
        # Sort instruments by mastery (lowest first)
        sorted_instruments = sorted(
            INSTRUMENTS,
            key=lambda i: self.instrument_mastery.get(i, 0.0)
        )
        
        # Find concept gaps
        gaps = pharma_concepts.find_gaps(self.concept_mastery, threshold=0.4)
        
        # Pick the weakest instrument
        weakest = sorted_instruments[0]
        weakest_mastery = self.instrument_mastery[weakest]
        
        # Determine activity type based on mastery level
        if weakest_mastery < 0.15:
            activity = "tutorial"
            action = f"Start with the {INSTRUMENT_LABELS[weakest]} tutorial to learn the fundamentals"
        elif weakest_mastery < 0.35:
            activity = "simulation"
            action = f"Run a guided {INSTRUMENT_LABELS[weakest]} simulation with a known compound"
        elif weakest_mastery < 0.6:
            activity = "experiment"
            action = f"Try analyzing an unknown compound using {INSTRUMENT_LABELS[weakest]}"
        else:
            activity = "quiz"
            action = f"Test your {INSTRUMENT_LABELS[weakest]} knowledge with a quiz"
        
        # Check if there's a more impactful gap to address
        priority_gap = None
        if gaps:
            # Find a gap that's both impactful and foundational
            for gap in gaps[:3]:
                if gap["difficulty"] <= 2 and gap["blocked_concepts"] >= 3:
                    priority_gap = gap
                    break
        
        result = {
            "recommended_instrument": weakest,
            "instrument_label": INSTRUMENT_LABELS[weakest],
            "current_mastery": round(weakest_mastery, 3),
            "suggested_activity": activity,
            "action": action,
            "difficulty": self.get_difficulty(weakest),
            "reasoning": f"Your {INSTRUMENT_LABELS[weakest]} mastery is {round(weakest_mastery*100)}%, "
                        f"which is your lowest. {f'Focusing here will unlock {gaps[0]['blocked_concepts']} related concepts.' if gaps else 'Building this skill will strengthen your overall analytical capabilities.'}"
        }
        
        if priority_gap:
            result["priority_concept"] = {
                "concept_id": priority_gap["concept_id"],
                "label": priority_gap["label"],
                "description": priority_gap["description"],
                "impact": f"Mastering this unlocks {priority_gap['blocked_concepts']} downstream concepts"
            }
        
        return result

    def get_mastery_summary(self) -> dict:
        """Get a full summary of the student's mastery state."""
        total_mastery = sum(self.instrument_mastery.values()) / len(INSTRUMENTS)
        total_sims = sum(self.simulations_count.values())
        
        instruments = []
        for inst in INSTRUMENTS:
            instruments.append({
                "instrument": inst,
                "label": INSTRUMENT_LABELS[inst],
                "mastery": round(self.instrument_mastery[inst], 3),
                "mastery_percent": round(self.instrument_mastery[inst] * 100, 1),
                "difficulty": self.get_difficulty(inst),
                "simulations_run": self.simulations_count.get(inst, 0),
                "last_accessed": self.last_accessed.get(inst)
            })
        
        # Sort by mastery descending (strengths first)
        instruments.sort(key=lambda x: x["mastery"], reverse=True)
        
        # Find strengths and weaknesses
        strengths = [i for i in instruments if i["mastery"] >= 0.5]
        weaknesses = [i for i in instruments if i["mastery"] < 0.3]
        
        return {
            "user_id": self.user_id,
            "overall_mastery": round(total_mastery, 3),
            "overall_mastery_percent": round(total_mastery * 100, 1),
            "total_simulations": total_sims,
            "total_events": len(self.events),
            "instruments": instruments,
            "strengths": [s["label"] for s in strengths],
            "weaknesses": [w["label"] for w in weaknesses],
            "next_suggestion": self.suggest_next_activity()
        }


class AdaptiveEngine:
    """Manages student profiles and provides adaptive learning features.
    
    In production, profiles would be persisted to DB. For now, in-memory
    with serialization support.
    """
    
    def __init__(self):
        self._profiles: dict[int, StudentProfile] = {}
    
    def get_profile(self, user_id: int) -> StudentProfile:
        """Get or create a student profile."""
        if user_id not in self._profiles:
            self._profiles[user_id] = StudentProfile(user_id)
        return self._profiles[user_id]
    
    def update_mastery(self, user_id: int, instrument: str, score: float,
                       concepts: list[str] = None, activity_type: str = "simulation") -> dict:
        """Update a student's mastery and return updated state."""
        profile = self.get_profile(user_id)
        profile.update_mastery(instrument, score, concepts, activity_type)
        return {
            "instrument": instrument,
            "new_mastery": round(profile.instrument_mastery[instrument], 3),
            "new_mastery_percent": round(profile.instrument_mastery[instrument] * 100, 1),
            "difficulty": profile.get_difficulty(instrument),
            "next_suggestion": profile.suggest_next_activity()
        }
    
    def get_learning_path(self, target: str = "drug_quality_testing",
                          user_id: int = None) -> dict:
        """Get the recommended learning path, optionally personalized for a user."""
        path = pharma_concepts.get_learning_path(target)
        
        if user_id:
            profile = self.get_profile(user_id)
            # Annotate each concept with the user's mastery
            for concept in path:
                cid = concept["concept_id"]
                concept["mastery"] = round(profile.concept_mastery.get(cid, 0.0), 3)
                concept["completed"] = concept["mastery"] >= 0.7
        
        return {
            "target": target,
            "path": path,
            "total_concepts": len(path)
        }


# ---- Singleton Instance ----
adaptive_engine = AdaptiveEngine()
