"""
Pharmaceutical Knowledge Graph — Concept Mastery & Learning Paths

Maps prerequisite relationships between instruments and analytical concepts.
Used by the Adaptive Engine to recommend learning sequences and identify gaps.
"""
import networkx as nx
from typing import Optional


# ---- Concept Knowledge Graph ----
class PharmaConcepts:
    """Directed acyclic graph of pharmaceutical analytical concepts.
    
    Nodes represent concepts/skills. Edges represent prerequisites.
    Edge: A → B means "A is a prerequisite for B".
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_graph()

    def _build_graph(self):
        """Build the pharmaceutical knowledge graph with concepts and prerequisites."""
        
        # ---- Foundation Concepts ----
        self._add_concept("light_matter_interaction", 
            label="Light-Matter Interaction",
            instrument=None,
            difficulty=1,
            description="How electromagnetic radiation interacts with molecules")
        
        self._add_concept("electromagnetic_spectrum",
            label="Electromagnetic Spectrum",
            instrument=None,
            difficulty=1,
            description="UV, Visible, IR regions and their energies")
        
        self._add_concept("molecular_structure",
            label="Molecular Structure Basics",
            instrument=None,
            difficulty=1,
            description="Bonds, functional groups, molecular formula")
        
        self._add_concept("chromatography_basics",
            label="Chromatography Principles",
            instrument=None,
            difficulty=1,
            description="Separation based on differential partitioning")
        
        self._add_concept("stereochemistry",
            label="Stereochemistry & Chirality",
            instrument=None,
            difficulty=2,
            description="Enantiomers, optical activity, chiral centers")
        
        self._add_concept("particle_physics",
            label="Particle Properties",
            instrument=None,
            difficulty=1,
            description="Size, shape, distribution of solid particles")

        # ---- UV-Vis Concepts ----
        self._add_concept("beer_lambert_law",
            label="Beer-Lambert Law (A=εlc)",
            instrument="uvvis",
            difficulty=2,
            description="Relationship between absorbance, concentration, and path length")
        
        self._add_concept("chromophores",
            label="Chromophores & Auxochromes",
            instrument="uvvis",
            difficulty=3,
            description="Molecular groups responsible for UV-Vis absorption")
        
        self._add_concept("uvvis_calibration",
            label="UV-Vis Calibration Curves",
            instrument="uvvis",
            difficulty=3,
            description="Building calibration curves for quantitative analysis")
        
        self._add_concept("uvvis_method_validation",
            label="UV-Vis Method Validation",
            instrument="uvvis",
            difficulty=4,
            description="Linearity, accuracy, precision, LOD/LOQ")

        # ---- FTIR Concepts ----
        self._add_concept("ir_absorption",
            label="IR Absorption Principles",
            instrument="ftir",
            difficulty=2,
            description="Molecular vibrations and IR absorption")
        
        self._add_concept("functional_groups_ir",
            label="Functional Group Identification",
            instrument="ftir",
            difficulty=3,
            description="Identifying O-H, C=O, N-H, etc. from IR spectra")
        
        self._add_concept("fingerprint_region",
            label="Fingerprint Region Analysis",
            instrument="ftir",
            difficulty=3,
            description="Using sub-1500 cm⁻¹ region for compound identification")
        
        self._add_concept("atr_sampling",
            label="ATR Sampling Technique",
            instrument="ftir",
            difficulty=3,
            description="Attenuated Total Reflectance for solid/liquid samples")

        # ---- HPLC Concepts ----
        self._add_concept("retention_time",
            label="Retention Time & Selectivity",
            instrument="hplc",
            difficulty=2,
            description="Understanding tR, k', α, and Rs")
        
        self._add_concept("mobile_phase_optimization",
            label="Mobile Phase Optimization",
            instrument="hplc",
            difficulty=3,
            description="Solvent selection, gradient elution, pH effects")
        
        self._add_concept("column_selection",
            label="Column Selection (C18, C8, HILIC)",
            instrument="hplc",
            difficulty=3,
            description="Choosing appropriate stationary phase")
        
        self._add_concept("hplc_method_development",
            label="HPLC Method Development",
            instrument="hplc",
            difficulty=4,
            description="Systematic approach to developing robust HPLC methods")

        # ---- GC Concepts ----
        self._add_concept("gc_separation",
            label="GC Separation Principles",
            instrument="gc",
            difficulty=2,
            description="Volatility-based separation with carrier gas")
        
        self._add_concept("temperature_programming",
            label="Temperature Programming",
            instrument="gc",
            difficulty=3,
            description="Optimizing oven temperature ramps for complex mixtures")
        
        self._add_concept("gc_detectors",
            label="GC Detectors (FID, TCD, ECD)",
            instrument="gc",
            difficulty=3,
            description="Detector selection based on compound properties")

        # ---- Mass Spec Concepts ----
        self._add_concept("ionization_techniques",
            label="Ionization Techniques (EI, ESI)",
            instrument="mass_spec",
            difficulty=2,
            description="Electron impact vs electrospray ionization")
        
        self._add_concept("fragmentation_patterns",
            label="Fragmentation Pattern Analysis",
            instrument="mass_spec",
            difficulty=3,
            description="Interpreting m/z values and fragmentation pathways")
        
        self._add_concept("molecular_ion_identification",
            label="Molecular Ion & Base Peak",
            instrument="mass_spec",
            difficulty=3,
            description="Identifying M⁺, base peak, and isotope patterns")

        # ---- Polarimetry Concepts ----
        self._add_concept("optical_rotation",
            label="Optical Rotation & Specific Rotation",
            instrument="polarimeter",
            difficulty=2,
            description="Measuring rotation of plane-polarized light")
        
        self._add_concept("enantiomeric_analysis",
            label="Enantiomeric Purity Analysis",
            instrument="polarimeter",
            difficulty=3,
            description="Using polarimetry for chiral drug quality control")

        # ---- PSA Concepts ----
        self._add_concept("laser_diffraction",
            label="Laser Diffraction Principles",
            instrument="psa",
            difficulty=2,
            description="Measuring particle size via light scattering")
        
        self._add_concept("particle_distribution",
            label="Particle Size Distribution (D10/D50/D90)",
            instrument="psa",
            difficulty=3,
            description="Interpreting distribution curves and D-values")

        # ---- Cross-Instrument Concepts ----
        self._add_concept("multi_instrument_id",
            label="Multi-Instrument Compound Identification",
            instrument=None,
            difficulty=4,
            description="Using UV-Vis + FTIR + MS together for identification")
        
        self._add_concept("method_validation",
            label="Analytical Method Validation (ICH Q2)",
            instrument=None,
            difficulty=5,
            description="Full method validation per regulatory guidelines")
        
        self._add_concept("drug_quality_testing",
            label="Drug Quality Control Testing",
            instrument=None,
            difficulty=5,
            description="Complete analytical testing of pharmaceutical products")

        # ---- Prerequisites (Edges) ----
        prerequisites = [
            # Foundations → Instruments
            ("light_matter_interaction", "beer_lambert_law"),
            ("light_matter_interaction", "ir_absorption"),
            ("electromagnetic_spectrum", "beer_lambert_law"),
            ("electromagnetic_spectrum", "ir_absorption"),
            ("molecular_structure", "chromophores"),
            ("molecular_structure", "functional_groups_ir"),
            ("molecular_structure", "fragmentation_patterns"),
            ("chromatography_basics", "retention_time"),
            ("chromatography_basics", "gc_separation"),
            ("stereochemistry", "optical_rotation"),
            ("particle_physics", "laser_diffraction"),
            
            # Within UV-Vis
            ("beer_lambert_law", "chromophores"),
            ("beer_lambert_law", "uvvis_calibration"),
            ("uvvis_calibration", "uvvis_method_validation"),
            
            # Within FTIR
            ("ir_absorption", "functional_groups_ir"),
            ("functional_groups_ir", "fingerprint_region"),
            ("functional_groups_ir", "atr_sampling"),
            
            # Within HPLC
            ("retention_time", "mobile_phase_optimization"),
            ("retention_time", "column_selection"),
            ("mobile_phase_optimization", "hplc_method_development"),
            ("column_selection", "hplc_method_development"),
            
            # Within GC
            ("gc_separation", "temperature_programming"),
            ("gc_separation", "gc_detectors"),
            
            # Within MS
            ("ionization_techniques", "fragmentation_patterns"),
            ("ionization_techniques", "molecular_ion_identification"),
            
            # Within Polarimetry
            ("optical_rotation", "enantiomeric_analysis"),
            
            # Within PSA
            ("laser_diffraction", "particle_distribution"),
            
            # Cross-instrument
            ("chromophores", "multi_instrument_id"),
            ("functional_groups_ir", "multi_instrument_id"),
            ("fragmentation_patterns", "multi_instrument_id"),
            
            # Advanced
            ("multi_instrument_id", "method_validation"),
            ("uvvis_method_validation", "method_validation"),
            ("hplc_method_development", "method_validation"),
            ("method_validation", "drug_quality_testing"),
            ("enantiomeric_analysis", "drug_quality_testing"),
            ("particle_distribution", "drug_quality_testing"),
        ]
        
        for prereq, concept in prerequisites:
            self.graph.add_edge(prereq, concept)

    def _add_concept(self, concept_id: str, label: str, instrument: Optional[str],
                     difficulty: int, description: str):
        """Add a concept node to the graph."""
        self.graph.add_node(concept_id, 
                           label=label,
                           instrument=instrument,
                           difficulty=difficulty,
                           description=description)

    def get_learning_path(self, target_concept: str = "drug_quality_testing") -> list[dict]:
        """Get the optimal learning path to reach a target concept.
        
        Returns concepts in topological order (prerequisites first).
        """
        if target_concept not in self.graph:
            return []
        
        # Get all ancestors (prerequisites) + the target
        ancestors = nx.ancestors(self.graph, target_concept)
        ancestors.add(target_concept)
        
        # Subgraph of relevant concepts
        subgraph = self.graph.subgraph(ancestors)
        
        # Topological sort = learning order
        ordered = list(nx.topological_sort(subgraph))
        
        return [
            {
                "concept_id": cid,
                **self.graph.nodes[cid]
            }
            for cid in ordered
        ]

    def get_instrument_concepts(self, instrument: str) -> list[dict]:
        """Get all concepts related to a specific instrument."""
        return [
            {"concept_id": nid, **data}
            for nid, data in self.graph.nodes(data=True)
            if data.get("instrument") == instrument
        ]

    def get_prerequisites(self, concept_id: str) -> list[dict]:
        """Get direct prerequisites for a concept."""
        if concept_id not in self.graph:
            return []
        return [
            {"concept_id": pred, **self.graph.nodes[pred]}
            for pred in self.graph.predecessors(concept_id)
        ]

    def find_gaps(self, mastery: dict[str, float], threshold: float = 0.5) -> list[dict]:
        """Find concept gaps: low-mastery concepts that are blocking higher concepts.
        
        Args:
            mastery: dict mapping concept_id → mastery level (0.0 to 1.0)
            threshold: mastery level below which a concept is considered a gap
        
        Returns:
            List of gap concepts sorted by impact (how many downstream concepts are blocked)
        """
        gaps = []
        for node in self.graph.nodes:
            level = mastery.get(node, 0.0)
            if level < threshold:
                # Count how many downstream concepts are blocked
                descendants = len(nx.descendants(self.graph, node))
                gaps.append({
                    "concept_id": node,
                    **self.graph.nodes[node],
                    "current_mastery": level,
                    "blocked_concepts": descendants
                })
        
        # Sort by impact (most downstream concepts blocked first)
        gaps.sort(key=lambda g: g["blocked_concepts"], reverse=True)
        return gaps

    def get_all_concepts(self) -> list[dict]:
        """Get all concepts in the graph."""
        return [
            {"concept_id": nid, **data}
            for nid, data in self.graph.nodes(data=True)
        ]

    def to_dict(self) -> dict:
        """Serialize the graph to a dictionary for API responses."""
        return {
            "concepts": self.get_all_concepts(),
            "edges": [
                {"from": u, "to": v}
                for u, v in self.graph.edges()
            ],
            "total_concepts": self.graph.number_of_nodes(),
            "total_prerequisites": self.graph.number_of_edges()
        }


# ---- Singleton Instance ----
pharma_concepts = PharmaConcepts()
