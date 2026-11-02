# Corrected Study Design Protocol
**Version:** REV2 / PHASE4.2  
**Date:** October 4, 2026  

---

## 1. Study Classification & Pedagogical Framework
- **Design Type:** Single-group, pre-test / intervention / post-test exploratory pilot evaluation.
- **Pedagogical Model:** Cognitive Load Theory (Sweller) and Guided Discovery Learning (Mayer).
- **Target Population:** Third- and fourth-year undergraduate students enrolled in Pharmacy (B.Pharm) or Chemistry (B.Sc.) undertaking formal coursework in instrumental chemical analysis.
- **Planned Sample Size:** $N = 25$ participants (acceptable target range: $N = 20–30$), corresponding to a typical university laboratory section.

---

## 2. Temporal Study Flow (50-Minute Standardized Session)
The pilot is embedded within a standard 50-minute scheduled laboratory period:

```
[00:00 - 00:05] Phase 1: Consent & Orientation (5 min)
  ├── Plain-language study briefing
  └── Written informed consent administration

[00:05 - 00:15] Phase 2: Diagnostic Baseline Pre-Test (10 min)
  └── 10-item isomorphic multiple-choice test (Paper-and-pencil, timed)

[00:15 - 00:27] Phase 3: Standardized Neutral Simulator Exploration (12 min)
  ├── 3 min: Interface orientation (sliders, mobile phase, flow rate)
  ├── 3 min: Normal baseline chromatographic run
  └── 6 min: Neutral guided inquiry of 4 fault modes (Air Bubble, Leak, Void, Contamination)

[00:27 - 00:39] Phase 4: Unknown Practical Diagnostic Tasks (12 min)
  ├── Scenario Alpha (Fitting Leak) — 3 min
  ├── Scenario Beta (Column Void) — 3 min
  ├── Scenario Gamma (Air Bubble) — 3 min
  └── Scenario Delta (Contamination) — 3 min

[00:39 - 00:49] Phase 5: Post-Test & Usability Evaluation (10 min)
  ├── 10-item isomorphic diagnostic post-test (Paper-and-pencil)
  ├── 10-item canonical System Usability Scale (SUS)
  └── 8-item targeted UX survey & open-ended reflection

[00:49 - 00:50] Session Conclusion & Debriefing (1 min)
  └── Student submission of coded assessment packets
```

---

## 3. Methodological Safeguards & Bias Control
1. **Neutral Guided Inquiry:** The instructor follows a strictly standardized, non-directive verbal protocol. The instructor demonstrates *how* to operate controls but *never* provides answers, numerical shifts, or mechanistic explanations.
2. **Observer Fidelity Monitoring:** An independent observer evaluates instructor adherence using a 10-point fidelity checklist (`instructor_fidelity_checklist.md`).
3. **Double-Blind Scoring:** Assessment packets are coded with anonymous Participant IDs (`P01` to `P25`). Two independent faculty raters grade practical diagnostic tasks using the standardized 24-point rubric. Discrepancies $>1$ point are resolved via adjudicated consensus.
4. **Isomorphic Assessment Design:** Pre-test and post-test instruments evaluate identical diagnostic constructs and Bloom cognitive levels using distinct surface scenarios with randomized key distributions.
