"""
Autonomous Lab Agent — The Core Intelligence

Plans, executes, and interprets multi-instrument experiments autonomously.
Given a research goal, it selects instruments, runs simulations, cross-references
results, and produces a comprehensive analysis report.

This is the "brain" that makes SimuPharma an AI — not just a simulator.
"""
from typing import Optional
from datetime import datetime

# Import all science engines
from ..science.uvvis import generate_spectrum as uvvis_spectrum, calibration_curve as uvvis_calibration
from ..science.ftir import generate_ftir_spectrum
from ..science.hplc import simulate_hplc, HPLCParams
from ..science.gc import simulate_gc, GCParams
from ..science.mass_spec import simulate_mass_spec, MassSpecParams, MassSpecCompound
from ..science.polarimeter import calculate_rotation
from ..science.psa import simulate_psa, PSAParams

# Import compound database
from ..compounds.database import get_compound, search_compounds, COMPOUNDS

# Import ML analyzer
from ..analytics.ml_analyzer import identify_compound


class LabAgent:
    """Autonomous laboratory agent that can plan and execute experiments.
    
    The agent operates through a tool-calling pattern:
    1. Receives a goal/question from the user
    2. Plans which instruments and analyses to run
    3. Executes each step by calling the appropriate science engine
    4. Interprets results and produces a report
    
    All tools are backed by the existing SimuPharma science engines,
    ensuring scientific accuracy.
    """

    # Registry of available tools that can be called by the AI
    TOOLS = {
        "search_compound": {
            "description": "Search the pharmaceutical compound database by name, formula, CAS number, or category. Returns matching compounds with basic info.",
            "parameters": {
                "query": {"type": "string", "description": "Search query (name, formula, CAS, or category)"},
                "category": {"type": "string", "description": "Optional category filter (e.g., 'Analgesic', 'Antibiotic')"}
            },
            "required": ["query"]
        },
        "get_compound_info": {
            "description": "Get detailed information about a specific compound including all available spectral data, molecular weight, formula, therapeutic class, and pharmacopeia references.",
            "parameters": {
                "compound_id": {"type": "string", "description": "The compound identifier (e.g., 'paracetamol', 'aspirin', 'ibuprofen')"}
            },
            "required": ["compound_id"]
        },
        "run_uvvis": {
            "description": "Run a UV-Vis spectroscopy simulation using Beer-Lambert Law. Generates absorption spectrum with peaks, absorbance values, and λmax. Use for quantitative analysis and chromophore identification.",
            "parameters": {
                "compound_id": {"type": "string", "description": "Compound to analyze (e.g., 'paracetamol')"},
                "concentration": {"type": "number", "description": "Concentration in mol/L (default: 0.001)"},
                "path_length": {"type": "number", "description": "Path length in cm (default: 1.0)"}
            },
            "required": ["compound_id"]
        },
        "run_ftir": {
            "description": "Run an FTIR spectroscopy simulation. Generates infrared absorption spectrum with functional group assignments. Use for molecular structure identification.",
            "parameters": {
                "compound_id": {"type": "string", "description": "Compound to analyze"}
            },
            "required": ["compound_id"]
        },
        "run_hplc": {
            "description": "Run an HPLC chromatography simulation using Van Deemter plate theory. Generates a chromatogram with retention times, peak areas, and resolution. Use for separation and purity analysis.",
            "parameters": {
                "compound_id": {"type": "string", "description": "Compound to analyze"},
                "flow_rate": {"type": "number", "description": "Flow rate in mL/min (default: 1.0)"},
                "column_length": {"type": "number", "description": "Column length in cm (default: 15.0)"}
            },
            "required": ["compound_id"]
        },
        "run_gc": {
            "description": "Run a Gas Chromatography simulation with temperature programming. Use for volatile compound analysis, residual solvents.",
            "parameters": {
                "compound_id": {"type": "string", "description": "Compound to analyze"},
                "initial_temp": {"type": "number", "description": "Initial oven temperature °C (default: 40)"},
                "final_temp": {"type": "number", "description": "Final oven temperature °C (default: 280)"}
            },
            "required": ["compound_id"]
        },
        "run_mass_spec": {
            "description": "Run a Mass Spectrometry simulation. Generates mass spectrum with m/z values, fragmentation patterns, molecular ion peak, and base peak. Use for molecular weight determination and structure elucidation.",
            "parameters": {
                "compound_id": {"type": "string", "description": "Compound to analyze"},
                "ionization_mode": {"type": "string", "description": "Ionization mode: 'EI' or 'ESI' (default: 'EI')"}
            },
            "required": ["compound_id"]
        },
        "run_polarimeter": {
            "description": "Run a polarimetry measurement. Calculates optical rotation for chiral compounds. Use for enantiomeric purity and chiral drug identity testing.",
            "parameters": {
                "compound_id": {"type": "string", "description": "Compound to analyze"},
                "concentration": {"type": "number", "description": "Concentration in g/mL (default: 0.1)"},
                "temperature": {"type": "number", "description": "Temperature in °C (default: 20.0)"}
            },
            "required": ["compound_id"]
        },
        "run_psa": {
            "description": "Run a Particle Size Analysis simulation using laser diffraction. Generates particle size distribution with D10, D50, D90 values. Use for formulation development.",
            "parameters": {
                "compound_id": {"type": "string", "description": "Compound to analyze"},
                "mean_size": {"type": "number", "description": "Mean particle size in μm (default: 50.0)"}
            },
            "required": ["compound_id"]
        },
        "identify_unknown": {
            "description": "Use multi-instrument spectral matching to identify an unknown compound from spectral data. Provide peaks from UV-Vis, FTIR, and/or Mass Spec for best results. Multi-instrument data gives higher confidence.",
            "parameters": {
                "uvvis_peaks": {"type": "array", "description": "UV-Vis peaks: [{wavelength, absorbance}]"},
                "ftir_peaks": {"type": "array", "description": "FTIR peaks: [{wavenumber}]"},
                "ms_fragments": {"type": "array", "description": "MS fragments: [{mz, intensity}]"},
                "molecular_weight": {"type": "number", "description": "Known molecular weight (if any)"}
            },
            "required": []
        },
        "compare_compounds": {
            "description": "Compare two compounds across all available instruments. Returns side-by-side spectral data, molecular properties, and key differences.",
            "parameters": {
                "compound_a": {"type": "string", "description": "First compound ID"},
                "compound_b": {"type": "string", "description": "Second compound ID"}
            },
            "required": ["compound_a", "compound_b"]
        }
    }

    def __init__(self):
        self.execution_log: list[dict] = []

    def get_tool_declarations(self) -> list[dict]:
        """Get Gemini-compatible function declarations for all tools.
        
        Returns the format expected by Gemini's function calling API.
        """
        declarations = []
        for name, tool in self.TOOLS.items():
            properties = {}
            for param_name, param_info in tool["parameters"].items():
                prop = {"type": param_info["type"], "description": param_info["description"]}
                # Gemini uses "STRING", "NUMBER", "ARRAY" as types
                type_map = {"string": "STRING", "number": "NUMBER", "array": "ARRAY", "object": "OBJECT"}
                prop["type"] = type_map.get(param_info["type"], "STRING")
                properties[param_name] = prop
            
            declarations.append({
                "name": name,
                "description": tool["description"],
                "parameters": {
                    "type": "OBJECT",
                    "properties": properties,
                    "required": tool.get("required", [])
                }
            })
        return declarations

    def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        """Execute a tool call and return the result.
        
        This is the core dispatch function that routes AI tool calls
        to the appropriate science engine.
        """
        timestamp = datetime.utcnow().isoformat()
        
        try:
            if tool_name == "search_compound":
                result = self._search_compound(**arguments)
            elif tool_name == "get_compound_info":
                result = self._get_compound_info(**arguments)
            elif tool_name == "run_uvvis":
                result = self._run_uvvis(**arguments)
            elif tool_name == "run_ftir":
                result = self._run_ftir(**arguments)
            elif tool_name == "run_hplc":
                result = self._run_hplc(**arguments)
            elif tool_name == "run_gc":
                result = self._run_gc(**arguments)
            elif tool_name == "run_mass_spec":
                result = self._run_mass_spec(**arguments)
            elif tool_name == "run_polarimeter":
                result = self._run_polarimeter(**arguments)
            elif tool_name == "run_psa":
                result = self._run_psa(**arguments)
            elif tool_name == "identify_unknown":
                result = self._identify_unknown(**arguments)
            elif tool_name == "compare_compounds":
                result = self._compare_compounds(**arguments)
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            
            # Log execution
            self.execution_log.append({
                "timestamp": timestamp,
                "tool": tool_name,
                "arguments": arguments,
                "success": "error" not in result,
                "result_summary": self._summarize_result(tool_name, result)
            })
            
            return result
            
        except Exception as e:
            error_result = {"error": str(e), "tool": tool_name}
            self.execution_log.append({
                "timestamp": timestamp,
                "tool": tool_name,
                "arguments": arguments,
                "success": False,
                "error": str(e)
            })
            return error_result

    # ---- Tool Implementations ----

    def _search_compound(self, query: str, category: str = "") -> dict:
        results = search_compounds(query, category)
        # Return summary (not full spectral data) to keep response concise
        summary = []
        for comp in results[:10]:
            summary.append({
                "id": comp["id"],
                "name": comp["name"],
                "category": comp.get("category", ""),
                "molecular_weight": comp.get("molecular_weight", 0),
                "formula": comp.get("formula", ""),
                "therapeutic_class": comp.get("therapeutic_class", "")
            })
        return {"results": summary, "total": len(results)}

    def _get_compound_info(self, compound_id: str) -> dict:
        compound = get_compound(compound_id)
        if not compound:
            return {"error": f"Compound '{compound_id}' not found in database"}
        return compound

    def _run_uvvis(self, compound_id: str, concentration: float = 0.001,
                   path_length: float = 1.0) -> dict:
        compound = get_compound(compound_id)
        if not compound:
            return {"error": f"Compound '{compound_id}' not found"}
        
        uv_data = compound.get("uvvis", {})
        peaks = uv_data.get("peaks", [])
        if not peaks:
            return {"error": f"No UV-Vis data available for {compound['name']}"}
        
        result = uvvis_spectrum(
            peaks=peaks,
            concentration=concentration,
            path_length=path_length
        )
        
        return {
            "instrument": "UV-Vis Spectroscopy",
            "compound": compound["name"],
            "concentration": concentration,
            "path_length": path_length,
            "solvent": uv_data.get("solvent", "water"),
            "peaks_found": [
                {"wavelength_nm": p["center"], "transition": p.get("label", ""), 
                 "molar_absorptivity": p["epsilon"]}
                for p in peaks
            ],
            "lambda_max": max(peaks, key=lambda p: p["epsilon"])["center"],
            "max_absorbance": round(max(peaks, key=lambda p: p["epsilon"])["epsilon"] * concentration * path_length, 4),
            "result": result.model_dump() if hasattr(result, 'model_dump') else result
        }

    def _run_ftir(self, compound_id: str) -> dict:
        compound = get_compound(compound_id)
        if not compound:
            return {"error": f"Compound '{compound_id}' not found"}
        
        peaks = compound.get("ftir", {}).get("peaks", [])
        if not peaks:
            return {"error": f"No FTIR data available for {compound['name']}"}
        
        result = generate_ftir_spectrum(peaks)
        
        return {
            "instrument": "FTIR Spectroscopy",
            "compound": compound["name"],
            "functional_groups": [
                {"wavenumber_cm1": p["wavenumber"], "assignment": p["assignment"],
                 "intensity": p["intensity"]}
                for p in peaks
            ],
            "total_peaks": len(peaks),
            "result": result.model_dump() if hasattr(result, 'model_dump') else result
        }

    def _run_hplc(self, compound_id: str, flow_rate: float = 1.0,
                  column_length: float = 15.0) -> dict:
        compound = get_compound(compound_id)
        if not compound:
            return {"error": f"Compound '{compound_id}' not found"}
        
        hplc_data = compound.get("hplc", {})
        
        params = HPLCParams(
            flow_rate=flow_rate,
            column_length=column_length,
            compounds=[{
                "name": compound["name"],
                "retention_factor": hplc_data.get("retention_factor", 2.0),
                "concentration": 100.0
            }]
        )
        
        result = simulate_hplc(params)
        
        return {
            "instrument": "HPLC",
            "compound": compound["name"],
            "flow_rate": flow_rate,
            "column_length": column_length,
            "logP": hplc_data.get("logP", "N/A"),
            "retention_factor": hplc_data.get("retention_factor", "N/A"),
            "result": result.model_dump() if hasattr(result, 'model_dump') else result
        }

    def _run_gc(self, compound_id: str, initial_temp: float = 40.0,
                final_temp: float = 280.0) -> dict:
        compound = get_compound(compound_id)
        if not compound:
            return {"error": f"Compound '{compound_id}' not found"}
        
        params = GCParams(
            initial_temp=initial_temp,
            final_temp=final_temp,
            compounds=[{
                "name": compound["name"],
                "boiling_point": compound.get("molecular_weight", 200) + 100,
                "concentration": 100.0
            }]
        )
        
        result = simulate_gc(params)
        
        return {
            "instrument": "Gas Chromatography",
            "compound": compound["name"],
            "initial_temp": initial_temp,
            "final_temp": final_temp,
            "result": result.model_dump() if hasattr(result, 'model_dump') else result
        }

    def _run_mass_spec(self, compound_id: str, ionization_mode: str = "EI") -> dict:
        compound = get_compound(compound_id)
        if not compound:
            return {"error": f"Compound '{compound_id}' not found"}
        
        ms_data = compound.get("mass_spec", {})
        fragments = ms_data.get("fragments", [])
        
        params = MassSpecParams(
            compound=MassSpecCompound(
                name=compound["name"],
                molecular_weight=compound["molecular_weight"],
                formula=compound.get("formula", ""),
                fragments=fragments
            ),
            ionization_mode=ionization_mode
        )
        
        result = simulate_mass_spec(params)
        
        # Find molecular ion and base peak
        mol_ion = None
        base_peak = None
        if fragments:
            base_peak = max(fragments, key=lambda f: f["intensity"])
            mol_ions = [f for f in fragments if "M⁺" in f.get("label", "") or "M+H" in f.get("label", "")]
            mol_ion = mol_ions[0] if mol_ions else fragments[0]
        
        return {
            "instrument": "Mass Spectrometry",
            "compound": compound["name"],
            "molecular_weight": compound["molecular_weight"],
            "formula": compound.get("formula", ""),
            "ionization_mode": ionization_mode,
            "molecular_ion": mol_ion,
            "base_peak": base_peak,
            "fragments": fragments,
            "total_fragments": len(fragments),
            "result": result.model_dump() if hasattr(result, 'model_dump') else result
        }

    def _run_polarimeter(self, compound_id: str, concentration: float = 0.1,
                         temperature: float = 20.0) -> dict:
        compound = get_compound(compound_id)
        if not compound:
            return {"error": f"Compound '{compound_id}' not found"}
        
        pol_data = compound.get("polarimetry", {})
        specific_rotation = pol_data.get("specific_rotation", 0)
        
        result = calculate_rotation(
            specific_rotation=specific_rotation,
            concentration=concentration,
            path_length=1.0,
            temperature=temperature,
            wavelength=589.3
        )
        
        return {
            "instrument": "Polarimetry",
            "compound": compound["name"],
            "specific_rotation": specific_rotation,
            "is_chiral": specific_rotation != 0,
            "note": pol_data.get("note", ""),
            "concentration": concentration,
            "temperature": temperature,
            "result": result.model_dump() if hasattr(result, 'model_dump') else result
        }

    def _run_psa(self, compound_id: str, mean_size: float = 50.0) -> dict:
        compound = get_compound(compound_id)
        if not compound:
            return {"error": f"Compound '{compound_id}' not found"}
        
        params = PSAParams(
            mean_size=mean_size,
            compound_name=compound["name"]
        )
        
        result = simulate_psa(params)
        
        return {
            "instrument": "Particle Size Analysis",
            "compound": compound["name"],
            "mean_size_um": mean_size,
            "result": result.model_dump() if hasattr(result, 'model_dump') else result
        }

    def _identify_unknown(self, uvvis_peaks: list = None, ftir_peaks: list = None,
                          ms_fragments: list = None, molecular_weight: float = 0) -> dict:
        result = identify_compound(
            uvvis_peaks=uvvis_peaks,
            ftir_peaks=ftir_peaks,
            ms_fragments=ms_fragments,
            molecular_weight=molecular_weight
        )
        
        return {
            "instrument": "ML Compound Identification",
            "method": "Multi-instrument spectral matching (cosine similarity + peak matching)",
            "result": result.model_dump() if hasattr(result, 'model_dump') else result
        }

    def _compare_compounds(self, compound_a: str, compound_b: str) -> dict:
        a = get_compound(compound_a)
        b = get_compound(compound_b)
        
        if not a:
            return {"error": f"Compound '{compound_a}' not found"}
        if not b:
            return {"error": f"Compound '{compound_b}' not found"}
        
        comparison = {
            "compound_a": {
                "id": compound_a,
                "name": a["name"],
                "molecular_weight": a["molecular_weight"],
                "formula": a.get("formula", ""),
                "category": a.get("category", ""),
                "therapeutic_class": a.get("therapeutic_class", "")
            },
            "compound_b": {
                "id": compound_b,
                "name": b["name"],
                "molecular_weight": b["molecular_weight"],
                "formula": b.get("formula", ""),
                "category": b.get("category", ""),
                "therapeutic_class": b.get("therapeutic_class", "")
            },
            "differences": []
        }
        
        # UV-Vis comparison
        a_uv = a.get("uvvis", {}).get("peaks", [])
        b_uv = b.get("uvvis", {}).get("peaks", [])
        if a_uv and b_uv:
            a_lmax = max(a_uv, key=lambda p: p["epsilon"])["center"]
            b_lmax = max(b_uv, key=lambda p: p["epsilon"])["center"]
            comparison["uvvis"] = {
                "a_lambda_max": a_lmax,
                "b_lambda_max": b_lmax,
                "difference_nm": abs(a_lmax - b_lmax),
                "distinguishable": abs(a_lmax - b_lmax) > 5
            }
            if abs(a_lmax - b_lmax) > 5:
                comparison["differences"].append(
                    f"UV-Vis: λmax differs by {abs(a_lmax - b_lmax)}nm ({a['name']}: {a_lmax}nm vs {b['name']}: {b_lmax}nm)")
        
        # Molecular weight comparison
        mw_diff = abs(a["molecular_weight"] - b["molecular_weight"])
        comparison["molecular_weight_difference"] = round(mw_diff, 2)
        if mw_diff > 1:
            comparison["differences"].append(
                f"Molecular weight: {a['name']} ({a['molecular_weight']}) vs {b['name']} ({b['molecular_weight']})")
        
        # FTIR comparison — unique peaks
        a_ftir = a.get("ftir", {}).get("peaks", [])
        b_ftir = b.get("ftir", {}).get("peaks", [])
        if a_ftir and b_ftir:
            a_wn = set(p["wavenumber"] for p in a_ftir)
            b_wn = set(p["wavenumber"] for p in b_ftir)
            unique_a = a_wn - b_wn
            unique_b = b_wn - a_wn
            if unique_a or unique_b:
                comparison["differences"].append(
                    f"FTIR: {a['name']} has unique peaks at {sorted(unique_a)} cm⁻¹; "
                    f"{b['name']} has unique peaks at {sorted(unique_b)} cm⁻¹")
        
        comparison["total_differences"] = len(comparison["differences"])
        comparison["easily_distinguishable"] = len(comparison["differences"]) >= 2
        
        return comparison

    def _summarize_result(self, tool_name: str, result: dict) -> str:
        """Create a brief text summary of a tool result for the execution log."""
        if "error" in result:
            return f"Error: {result['error']}"
        
        compound = result.get("compound", "unknown")
        instrument = result.get("instrument", tool_name)
        
        if tool_name == "search_compound":
            return f"Found {result.get('total', 0)} compounds"
        elif tool_name == "run_uvvis":
            return f"UV-Vis of {compound}: λmax={result.get('lambda_max', '?')}nm"
        elif tool_name == "run_ftir":
            return f"FTIR of {compound}: {result.get('total_peaks', 0)} peaks identified"
        elif tool_name == "run_mass_spec":
            mw = result.get("molecular_weight", "?")
            return f"MS of {compound}: MW={mw}"
        elif tool_name == "compare_compounds":
            return f"Compared: {result.get('total_differences', 0)} differences found"
        elif tool_name == "identify_unknown":
            return f"ML identification completed"
        else:
            return f"{instrument} analysis of {compound} completed"

    def plan_experiment(self, goal: str, compound_ids: list[str] = None) -> dict:
        """Plan an experiment based on a high-level goal.
        
        This generates a structured plan that the AI can then execute step by step.
        The plan is deterministic (not AI-generated) to ensure scientific validity.
        """
        goal_lower = goal.lower()
        steps = []
        
        # Determine which compounds to work with
        compounds = []
        if compound_ids:
            for cid in compound_ids:
                comp = get_compound(cid)
                if comp:
                    compounds.append(comp)
        
        # Pattern matching on common goals
        if "identify" in goal_lower or "unknown" in goal_lower:
            steps = [
                {"step": 1, "tool": "run_uvvis", "reason": "UV-Vis provides initial chromophore identification and λmax"},
                {"step": 2, "tool": "run_ftir", "reason": "FTIR identifies functional groups for structural characterization"},
                {"step": 3, "tool": "run_mass_spec", "reason": "Mass Spec confirms molecular weight and fragmentation pattern"},
                {"step": 4, "tool": "identify_unknown", "reason": "ML matching combines all spectral data for identification"},
            ]
            plan_type = "compound_identification"
            
        elif "compare" in goal_lower or "vs" in goal_lower or "difference" in goal_lower:
            steps = [
                {"step": 1, "tool": "compare_compounds", "reason": "Side-by-side comparison of all available data"},
                {"step": 2, "tool": "run_uvvis", "reason": "UV-Vis comparison of absorption profiles"},
                {"step": 3, "tool": "run_mass_spec", "reason": "MS comparison of fragmentation patterns"},
            ]
            plan_type = "compound_comparison"
            
        elif "purity" in goal_lower or "quality" in goal_lower or "assay" in goal_lower:
            steps = [
                {"step": 1, "tool": "run_hplc", "reason": "HPLC determines purity and separation from impurities"},
                {"step": 2, "tool": "run_uvvis", "reason": "UV-Vis quantitative assay via calibration curve"},
                {"step": 3, "tool": "run_ftir", "reason": "FTIR confirms identity against reference"},
            ]
            plan_type = "quality_analysis"
            
        elif "chiral" in goal_lower or "optical" in goal_lower or "enantiomer" in goal_lower:
            steps = [
                {"step": 1, "tool": "run_polarimeter", "reason": "Polarimetry measures optical rotation for chiral analysis"},
                {"step": 2, "tool": "run_hplc", "reason": "Chiral HPLC for enantiomeric separation"},
                {"step": 3, "tool": "run_mass_spec", "reason": "MS confirms molecular identity"},
            ]
            plan_type = "chiral_analysis"
            
        elif "particle" in goal_lower or "formulation" in goal_lower or "size" in goal_lower:
            steps = [
                {"step": 1, "tool": "run_psa", "reason": "Particle size distribution analysis"},
                {"step": 2, "tool": "run_ftir", "reason": "FTIR confirms compound identity"},
            ]
            plan_type = "formulation_analysis"
            
        elif "volatile" in goal_lower or "solvent" in goal_lower or "residual" in goal_lower:
            steps = [
                {"step": 1, "tool": "run_gc", "reason": "GC for volatile/residual solvent analysis"},
                {"step": 2, "tool": "run_mass_spec", "reason": "GC-MS coupling for identification"},
            ]
            plan_type = "volatile_analysis"
            
        else:
            # Default: comprehensive analysis
            steps = [
                {"step": 1, "tool": "run_uvvis", "reason": "UV-Vis spectral profiling"},
                {"step": 2, "tool": "run_ftir", "reason": "FTIR functional group analysis"},
                {"step": 3, "tool": "run_mass_spec", "reason": "Mass spectrum and molecular weight"},
                {"step": 4, "tool": "run_hplc", "reason": "HPLC purity assessment"},
            ]
            plan_type = "comprehensive_analysis"
        
        return {
            "goal": goal,
            "plan_type": plan_type,
            "compounds": [{"id": c["id"], "name": c["name"]} for c in compounds],
            "steps": steps,
            "total_steps": len(steps),
            "estimated_time_seconds": len(steps) * 2,
            "created_at": datetime.utcnow().isoformat()
        }

    def execute_plan(self, plan: dict) -> dict:
        """Execute all steps in an experiment plan and return results.
        
        This runs each step sequentially, collecting results for the
        AI to interpret.
        """
        results = []
        compound_ids = [c["id"] for c in plan.get("compounds", [])]
        primary_compound = compound_ids[0] if compound_ids else None
        
        for step in plan["steps"]:
            tool_name = step["tool"]
            
            # Build arguments based on tool and available compounds
            args = {}
            if tool_name in ("run_uvvis", "run_ftir", "run_hplc", "run_gc", 
                            "run_mass_spec", "run_polarimeter", "run_psa"):
                if primary_compound:
                    args["compound_id"] = primary_compound
                else:
                    results.append({
                        "step": step["step"],
                        "tool": tool_name,
                        "skipped": True,
                        "reason": "No compound specified"
                    })
                    continue
                    
            elif tool_name == "compare_compounds":
                if len(compound_ids) >= 2:
                    args["compound_a"] = compound_ids[0]
                    args["compound_b"] = compound_ids[1]
                else:
                    results.append({
                        "step": step["step"],
                        "tool": tool_name,
                        "skipped": True,
                        "reason": "Need at least 2 compounds to compare"
                    })
                    continue
                    
            elif tool_name == "identify_unknown":
                # Use results from previous steps to feed into identification
                uvvis_peaks = None
                ftir_peaks = None
                ms_fragments = None
                mw = 0
                
                for prev in results:
                    prev_result = prev.get("result", {})
                    if prev.get("tool") == "run_uvvis" and "peaks_found" in prev_result:
                        uvvis_peaks = [
                            {"wavelength": p["wavelength_nm"], "absorbance": 1.0}
                            for p in prev_result["peaks_found"]
                        ]
                    elif prev.get("tool") == "run_ftir" and "functional_groups" in prev_result:
                        ftir_peaks = [
                            {"wavenumber": fg["wavenumber_cm1"]}
                            for fg in prev_result["functional_groups"]
                        ]
                    elif prev.get("tool") == "run_mass_spec":
                        if "fragments" in prev_result:
                            ms_fragments = prev_result["fragments"]
                        mw = prev_result.get("molecular_weight", 0)
                
                args = {
                    "uvvis_peaks": uvvis_peaks,
                    "ftir_peaks": ftir_peaks,
                    "ms_fragments": ms_fragments,
                    "molecular_weight": mw
                }
            
            # Execute
            result = self.execute_tool(tool_name, args)
            results.append({
                "step": step["step"],
                "tool": tool_name,
                "reason": step["reason"],
                "result": result,
                "success": "error" not in result
            })
        
        return {
            "goal": plan["goal"],
            "plan_type": plan["plan_type"],
            "results": results,
            "total_steps": len(results),
            "successful_steps": sum(1 for r in results if r.get("success", False)),
            "completed_at": datetime.utcnow().isoformat()
        }

    def full_analysis(self, goal: str, compound_ids: list[str] = None) -> dict:
        """Plan and execute a full analysis in one call.
        
        This is the highest-level autonomous operation:
        1. Plans the experiment
        2. Executes all steps
        3. Returns everything for AI interpretation
        """
        plan = self.plan_experiment(goal, compound_ids)
        execution = self.execute_plan(plan)
        
        return {
            "plan": plan,
            "execution": execution,
            "execution_log": self.execution_log[-len(plan["steps"]):],
            "summary": f"Completed {execution['successful_steps']}/{execution['total_steps']} steps "
                      f"for '{goal}'"
        }


# ---- Singleton Instance ----
lab_agent = LabAgent()
