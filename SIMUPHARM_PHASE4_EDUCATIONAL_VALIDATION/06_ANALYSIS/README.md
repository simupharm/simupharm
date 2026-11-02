# ANALYSIS CODE & VERIFICATION SUITE
**Directory:** `SIMUPHARM_PHASE4_EDUCATIONAL_VALIDATION/06_ANALYSIS/`  

---

## CONTENTS
- `analysis_plan.md`: Formal mathematical plan for computing inferential statistics.
- `analysis_code/calculate_pre_post_stats.py`: Automated paired difference testing script.
- `analysis_code/calculate_sus_score.py`: Automated Brooke SUS calculation script.
- `analysis_code/calculate_hake_gain.py`: Automated Hake normalized gain script.
- `test_data/DEMO_DATA_NOT_REAL.csv`: Explicitly labeled synthetic test data used strictly to verify that Python analysis scripts run smoothly prior to real data collection.

## HOW TO RUN
To verify scripts using the demo dataset:
```bash
python analysis_code/calculate_pre_post_stats.py test_data/DEMO_DATA_NOT_REAL.csv
python analysis_code/calculate_sus_score.py test_data/DEMO_DATA_NOT_REAL.csv
python analysis_code/calculate_hake_gain.py test_data/DEMO_DATA_NOT_REAL.csv
```

When real participant data is collected, execute:
```bash
python analysis_code/calculate_pre_post_stats.py ../05_DATA_TEMPLATES/participant_data_template.csv
```
