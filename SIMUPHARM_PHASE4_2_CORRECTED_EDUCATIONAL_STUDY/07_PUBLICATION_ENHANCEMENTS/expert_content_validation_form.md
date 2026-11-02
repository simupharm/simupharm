# Expert Content Review & Content-Validity Assessment Protocol
**Document ID:** P4.2.1-EXPERT-REVIEW-2026-REV2.1 (FINAL PROTOCOL FREEZE)  
**Target:** Independent Content Review by Analytical Chromatography Faculty & Industry Experts  
**Scope:** Content-validity assessment evaluating educational appropriateness, diagnostic plausibility, and symptom clarity from an expert perspective. (Does NOT constitute physical HPLC sensor or hardware validation).  
**Form Status:** **BLANK PROTOCOL TEMPLATE (Zero Fabricated Ratings)**  
**Target Panel:** 3 to 5 Independent Subject-Matter Experts (SMEs)  
**Rating Scale:** 1 = Not Relevant, 2 = Somewhat Relevant, 3 = Quite Relevant, 4 = Highly Relevant  

---

## 1. Expert Reviewer Demographics & Conflict-of-Interest Declaration
```
Reviewer Name:                   [ __________________________________________________ ]
Academic / Professional Title:   [ __________________________________________________ ]
Department & Institution:        [ __________________________________________________ ]
Years of HPLC Experience:        [ __________________________________________________ ]
Conflict-of-Interest Statement:  [ ] I declare no commercial or proprietary interest in SimuPharm.io.
Signature & Date:                [ __________________________________   DD / MM / YYYY ]
```

---

## 2. Evaluation Form

| Domain | Evaluated Dimension | 1<br/>NR | 2<br/>SR | 3<br/>QR | 4<br/>HR | Expert Qualitative Feedback |
| :--- | :--- | :-: | :-: | :-: | :-: | :--- |
| **D1: Symptom Representation** | Does the simulated air bubble produce pressure ripple and baseline noise characteristic of check valve cavitation from an expert perspective? | [ ] | [ ] | [ ] | [ ] | |
| **D2: Symptom Representation** | Does the simulated fitting leak represent the inverse relationship between volumetric flow loss and solute retention? | [ ] | [ ] | [ ] | [ ] | |
| **D3: Symptom Representation** | Does the simulated column bed void illustrate split doublet peaks and peak tailing characteristic of inlet voids? | [ ] | [ ] | [ ] | [ ] | |
| **D4: Symptom Representation** | Does the simulated ghost peak behavior represent contaminant accumulation during gradient re-equilibration? | [ ] | [ ] | [ ] | [ ] | |
| **D5: Curricular Relevance**   | Are the 4 simulated fault modes relevant and appropriate for undergraduate instrumental analysis instruction? | [ ] | [ ] | [ ] | [ ] | |
| **D6: Assessment Alignment**    | Do the pre-test, post-test, and practical rubric evaluate conceptual troubleshooting rather than rote memorization? | [ ] | [ ] | [ ] | [ ] | |

---

## 3. Content Validity Index (CVI) Formulation
- **Item Content Validity Index (I-CVI):** Proportion of experts awarding a rating of 3 or 4 on item $i$:
  $$\text{I-CVI}_i = \frac{N_{i(\text{rating } 3 \text{ or } 4)}}{N_{\text{total experts}}}$$
- **Scale-Level Content Validity Index (S-CVI/Ave):** Mean of all I-CVI values across the 6 dimensions:
  $$\text{S-CVI/Ave} = \frac{1}{6} \sum_{i=1}^6 \text{I-CVI}_i$$
- *Methodological Boundary:* CVI quantifies expert consensus on content appropriateness and symptom representation. It does **NOT** constitute physical HPLC experimental validation.
