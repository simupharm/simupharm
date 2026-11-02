# Corrected Intervention Protocol
**Version:** REV2 / PHASE4.2  
**Date:** October 4, 2026  

---

## 1. Technical Environment & Setup
1. **Hardware:** Standard university computer laboratory desktop or student laptops running modern evergreen web browsers (Google Chrome 110+, Mozilla Firefox 110+, Microsoft Edge 110+, or Apple Safari 16+).
2. **Access Mode:** Zero-install client-side execution. The application is served over local network HTTP or opened directly via `index.html`.
3. **Display Requirements:** Minimum screen resolution: $1280 	imes 720$ pixels.
4. **Internet Dependency:** Zero runtime external dependencies; all scripts and assets execute 100% offline.

---

## 2. Standardized Lab Session Protocol (50 Minutes Total)

### Phase 1: Consent & Onboarding (Minutes 00:00 – 00:05)
- The instructor distributes the sealed participant envelope containing:
  - Participant Information Sheet (`participant_information_sheet.md`)
  - Informed Consent Form (`informed_consent_template.md`)
  - Diagnostic Pre-Test (`pretest.md`)
  - Practical Task Sheet (`practical_diagnostic_task.md`)
  - Diagnostic Post-Test (`posttest.md`)
  - Usability Questionnaire (`SUS_instrument.md` & `usability_questionnaire.md`)
- The instructor reviews the voluntary nature of the study and confirms zero impact on course grades.
- Students sign consent and verify their assigned anonymous Participant ID (`P01` to `P25`).

### Phase 2: Diagnostic Baseline Pre-Test (Minutes 00:05 – 00:15)
- Students open the pre-test section of their packet.
- 10 multiple-choice questions assessing foundational HPLC troubleshooting concepts (10 minutes, closed book, no browser access).
- Packets are collected or placed facedown upon completion.

### Phase 3: Standardized Simulator Exploration (Minutes 00:15 – 00:27)
- Students open the SimuPharm simulator in their browser.
- **Minutes 15–18:** Familiarization with solvent composition sliders (% B), flow rate, and temperature.
- **Minutes 18–21:** Normal baseline separation of the 4-component analgesic mixture.
- **Minutes 21–27:** Neutral guided exploration of the Fault Injection panel. Students sequentially toggle Fault 1, Fault 2, Fault 3, and Fault 4, observing changes in backpressure and chromatographic peaks without instructor cueing.

### Phase 4: Unknown Practical Diagnostic Tasks (Minutes 00:27 – 00:39)
- Students open the Practical Task module in SimuPharm and their physical task worksheet.
- Four blind unknown fault conditions are presented in fixed sequence:
  - **Scenario Alpha (Fitting Leak):** Backpressure drops from 90 to 60 bar; retention stretches +30%.
  - **Scenario Beta (Column Bed Void):** Peak split doublets appear; tailing factor increases to 2.4.
  - **Scenario Gamma (Pump Cavitation):** Cyclical pressure ripple ($\pm 20	ext{ bar}$) with negative baseline spikes.
  - **Scenario Delta (Mobile Phase Contamination):** Unassigned ghost peaks elute during gradient hold.
- For each scenario (3 minutes each), students record: (1) Fault Diagnosis, (2) Physical Reasoning, (3) Corrective Action, (4) Confidence Rating (1–5), and (5) Diagnostic Latency (seconds).

### Phase 5: Post-Test & Usability Evaluation (Minutes 00:39 – 00:49)
- Students complete the 10-item isomorphic post-test (closed book, 6 minutes).
- Students complete the 10-item canonical System Usability Scale (SUS) and 8-item targeted UX survey (4 minutes).
- Students provide open-ended qualitative comments regarding usability and learning challenges.

### Phase 6: Conclusion (Minutes 00:49 – 00:50)
- All materials are placed into the participant envelope, sealed, and deposited in the secure collection box.
