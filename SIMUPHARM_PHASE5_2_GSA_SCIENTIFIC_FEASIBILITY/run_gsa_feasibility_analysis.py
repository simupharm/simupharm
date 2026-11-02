"""
SimuPharm Phase 5.2 - GSA Scientific Feasibility, Falsification & Kill Sprint
Full Computational Analysis Pipeline

This script executes the entire empirical analysis for Phase 5.2 without modifying
the frozen SimuPharm engine code. All calls are made directly to backend.science.hplc.simulate_hplc.
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Ensure root is in sys.path
sys.path.insert(0, os.path.abspath('.'))
from backend.science.hplc import HPLCParams, ColumnParams, HPLCCompound, simulate_hplc, van_deemter

from SALib.sample import sobol as sobol_sample
from SALib.analyze import sobol as sobol_analyze
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.tree import DecisionTreeClassifier, export_text

# Target directories
BASE_DIR = 'SIMUPHARM_PHASE5_2_GSA_SCIENTIFIC_FEASIBILITY'
DIRS = {
    'audit': os.path.join(BASE_DIR, '02_ENGINE_AUDIT'),
    'params': os.path.join(BASE_DIR, '03_PARAMETER_SPACE'),
    'pilot': os.path.join(BASE_DIR, '04_PILOT_SOBOL'),
    'convergence': os.path.join(BASE_DIR, '05_CONVERGENCE'),
    'ofat': os.path.join(BASE_DIR, '06_OFAT_COMPARISON'),
    'interaction': os.path.join(BASE_DIR, '07_INTERACTION_ANALYSIS'),
    'failure': os.path.join(BASE_DIR, '08_FAILURE_BOUNDARY'),
    'repro': os.path.join(BASE_DIR, '13_REPRODUCIBILITY'),
    'report': os.path.join(BASE_DIR, '14_FINAL_REPORT')
}

for d in DIRS.values():
    os.makedirs(d, exist_ok=True)

# -------------------------------------------------------------
# 1. FORENSIC ENGINE AUDIT & ANALYTICAL DERIVATION
# -------------------------------------------------------------
def run_forensic_engine_audit():
    print("=== Running Forensic Engine Audit ===")
    comp1 = HPLCCompound(name='Paracetamol', retention_factor=1.8, peak_width_factor=1.0)
    comp2 = HPLCCompound(name='Caffeine', retention_factor=3.2, peak_width_factor=1.0)
    
    # Test Temperature sensitivity
    res_t25 = simulate_hplc(HPLCParams(compounds=[comp1, comp2], column=ColumnParams(temperature_c=25.0)))
    res_t60 = simulate_hplc(HPLCParams(compounds=[comp1, comp2], column=ColumnParams(temperature_c=60.0)))
    dt_temp = res_t60.peaks[1].retention_time - res_t25.peaks[1].retention_time
    dRs_temp = res_t60.peaks[1].resolution - res_t25.peaks[1].resolution
    
    # Test Internal Diameter sensitivity
    res_id21 = simulate_hplc(HPLCParams(compounds=[comp1, comp2], column=ColumnParams(internal_diameter_mm=2.1)))
    res_id46 = simulate_hplc(HPLCParams(compounds=[comp1, comp2], column=ColumnParams(internal_diameter_mm=4.6)))
    dt_id = res_id46.peaks[1].retention_time - res_id21.peaks[1].retention_time
    dRs_id = res_id46.peaks[1].resolution - res_id21.peaks[1].resolution

    # Test Injection Volume sensitivity
    res_iv5 = simulate_hplc(HPLCParams(compounds=[comp1, comp2], injection_volume_ul=5.0))
    res_iv50 = simulate_hplc(HPLCParams(compounds=[comp1, comp2], injection_volume_ul=50.0))
    dHeight_iv = res_iv50.peaks[0].peak_height - res_iv5.peaks[0].peak_height

    # Test Van Deemter Curve properties
    dp_um = 5.0
    flow_rates = np.linspace(0.1, 5.0, 50)
    H_vals = [van_deemter(dp_um, f) for f in flow_rates]
    
    # Calculate analytical minimum of Van Deemter:
    # A = 2 * dp, B = 0.05, C = 0.01 * dp^2
    # u_opt = sqrt(B / C)
    dp_cm = dp_um * 1e-4
    A_coeff = 2 * dp_cm
    B_coeff = 0.05
    C_coeff = 0.01 * (dp_cm ** 2)
    u_opt = np.sqrt(B_coeff / C_coeff)
    H_min = A_coeff + 2 * np.sqrt(B_coeff * C_coeff)

    # Resolution vs Flow rate test
    Rs_flow = []
    for f in [0.2, 0.5, 1.0, 1.5, 2.0]:
        r = simulate_hplc(HPLCParams(compounds=[comp1, comp2], flow_rate_ml_min=f))
        Rs_flow.append(r.peaks[1].resolution)

    # Tailing factor stochasticity test: run 50 times with identical inputs
    tailing_samples = [simulate_hplc(HPLCParams(compounds=[comp1, comp2])).peaks[0].tailing_factor for _ in range(50)]

    audit_summary = {
        'temperature_sensitivity_dtR': float(dt_temp),
        'temperature_sensitivity_dRs': float(dRs_temp),
        'internal_diameter_sensitivity_dtR': float(dt_id),
        'internal_diameter_sensitivity_dRs': float(dRs_id),
        'injection_volume_sensitivity_dHeight': float(dHeight_iv),
        'van_deemter_A_cm': float(A_coeff),
        'van_deemter_B_cm_ml_min': float(B_coeff),
        'van_deemter_C_cm_min_ml': float(C_coeff),
        'van_deemter_u_opt_ml_min': float(u_opt),
        'van_deemter_H_min_cm': float(H_min),
        'flow_rates_tested': [0.2, 0.5, 1.0, 1.5, 2.0],
        'Rs_at_flow_rates': [float(x) for x in Rs_flow],
        'tailing_mean': float(np.mean(tailing_samples)),
        'tailing_std': float(np.std(tailing_samples)),
        'tailing_is_stochastic_random': bool(np.std(tailing_samples) > 0.05)
    }

    with open(os.path.join(DIRS['audit'], 'engine_audit_summary.json'), 'w') as f:
        json.dump(audit_summary, f, indent=2)

    # Save Van Deemter plot
    plt.figure(figsize=(7, 4.5))
    plt.plot(flow_rates, H_vals, 'b-', lw=2, label='SimuPharm H(u)')
    plt.axvline(u_opt, color='r', linestyle='--', label=f'u_opt = {u_opt:.1f} mL/min (Theoretical)')
    plt.xlabel('Flow Rate u (mL/min)', fontsize=11)
    plt.ylabel('Plate Height H (cm)', fontsize=11)
    plt.title('Forensic Audit: Inverted Van Deemter Curve (B-term Dominance)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(DIRS['audit'], 'van_deemter_audit.png'), dpi=300)
    plt.close()

    print("Forensic Engine Audit complete. Saved to 02_ENGINE_AUDIT.")
    return audit_summary

# -------------------------------------------------------------
# 2. DEFINITION OF PARAMETER SPACE
# -------------------------------------------------------------
def define_parameter_problems():
    # Wide design space (Exploratory / Method Development)
    problem_wide = {
        'num_vars': 6,
        'names': ['L', 'F', 'dp', 'pctB', 'T', 'dc'],
        'bounds': [
            [5.0, 25.0],    # Column length (cm)
            [0.5, 2.0],     # Flow rate (mL/min)
            [1.8, 5.0],     # Particle size (um)
            [30.0, 80.0],   # % Organic modifier
            [20.0, 60.0],   # Temperature (C) [inactive in engine]
            [2.1, 4.6]      # Internal diameter (mm) [inactive in engine]
        ]
    }

    # Narrow robustness space (Analytical Quality by Design Method Robustness)
    problem_narrow = {
        'num_vars': 6,
        'names': ['L', 'F', 'dp', 'pctB', 'T', 'dc'],
        'bounds': [
            [12.0, 18.0],   # L around 15 cm (+/- 20%)
            [0.9, 1.1],     # F around 1.0 mL/min (+/- 10%)
            [3.0, 4.0],     # dp around 3.5 um (+/- 14%)
            [45.0, 55.0],   # %B around 50% (+/- 10% relative)
            [22.0, 28.0],   # T around 25 C (+/- 3 C)
            [4.0, 4.6]      # dc around 4.6 mm
        ]
    }
    
    # Save parameter tables
    df_params = pd.DataFrame({
        'Parameter': ['L (Column Length)', 'F (Flow Rate)', 'dp (Particle Size)', 'pctB (% Organic)', 'T (Temperature)', 'dc (Internal Diameter)'],
        'Symbol': ['L', 'F', 'dp', 'pctB', 'T', 'dc'],
        'Units': ['cm', 'mL/min', 'um', '% v/v', '°C', 'mm'],
        'Baseline': [15.0, 1.0, 3.5, 50.0, 25.0, 4.6],
        'Wide_Low': [5.0, 0.5, 1.8, 30.0, 20.0, 2.1],
        'Wide_High': [25.0, 2.0, 5.0, 80.0, 60.0, 4.6],
        'Narrow_Low': [12.0, 0.9, 3.0, 45.0, 22.0, 4.0],
        'Narrow_High': [18.0, 1.1, 4.0, 55.0, 28.0, 4.6],
        'Engine_Role': ['Active (t0, N)', 'Active (H, t0)', 'Active (H)', 'Active (k_adj)', 'Inactive (Schema only)', 'Inactive (Schema only)'],
        'Scientific_Justification': [
            'Standard analytical column lengths (USP)',
            'Standard analytical HPLC flow range',
            'Standard sub-2 um to 5 um packings',
            'Reverse phase gradient/isocratic range',
            'Standard thermostatted column range',
            'Narrow-bore to standard-bore columns'
        ]
    })
    df_params.to_csv(os.path.join(DIRS['params'], 'parameter_ranges.csv'), index=False)
    print("Parameter space defined. Saved to 03_PARAMETER_SPACE.")
    return problem_wide, problem_narrow

# -------------------------------------------------------------
# 3. HPLC MODEL EVALUATION WRAPPER
# -------------------------------------------------------------
def evaluate_model_batch(param_matrix):
    """
    Evaluates SimuPharm simulate_hplc for each row in param_matrix.
    param_matrix columns: [L, F, dp, pctB, T, dc]
    Returns dict of numpy arrays: Rs, tR2, N_plates, pressure_est
    """
    comp1 = HPLCCompound(name='Paracetamol', retention_factor=1.8, peak_width_factor=1.0)
    comp2 = HPLCCompound(name='Caffeine', retention_factor=3.2, peak_width_factor=1.0)
    
    n_samples = len(param_matrix)
    Rs_arr = np.zeros(n_samples)
    tR2_arr = np.zeros(n_samples)
    N_arr = np.zeros(n_samples)
    pressure_arr = np.zeros(n_samples) # Estimated backpressure in bar

    for i in range(n_samples):
        L, F, dp, pctB, T, dc = param_matrix[i]
        params = HPLCParams(
            compounds=[comp1, comp2],
            column=ColumnParams(
                length_cm=float(L),
                particle_size_um=float(dp),
                internal_diameter_mm=float(dc),
                temperature_c=float(T)
            ),
            flow_rate_ml_min=float(F),
            mobile_phase_organic_pct=float(pctB),
            run_time_min=max(35.0, float(L / (F * 10) * (1 + 3.2 * (100 - pctB)/40) * 1.5))
        )
        res = simulate_hplc(params)
        Rs_arr[i] = res.peaks[1].resolution
        tR2_arr[i] = res.peaks[1].retention_time
        N_arr[i] = res.peaks[1].plates
        
        # Estimate physical pressure via Kozeny-Carman for water-ACN mixture
        # eta ~ 0.85 mPa*s, phi ~ 700
        # u (cm/s) = (F / 60) / (pi * (dc_cm/2)^2 * 0.65)
        dc_cm = dc * 0.1
        u_linear = (F / 60.0) / (np.pi * ((dc_cm / 2.0) ** 2) * 0.65)
        dp_cm = dp * 1e-4
        # Delta P = (700 * 0.85e-3 * u_linear * L) / (dp_cm^2) in Pa -> / 1e5 for bar
        p_bar = (700 * 0.85e-3 * u_linear * L) / (dp_cm ** 2) / 1e5
        pressure_arr[i] = p_bar

    return {
        'Rs': Rs_arr,
        'tR2': tR2_arr,
        'N': N_arr,
        'pressure': pressure_arr
    }

# -------------------------------------------------------------
# 4. PILOT GSA & CONVERGENCE EXPERIMENTS
# -------------------------------------------------------------
def run_pilot_sobol_experiments(problem_wide):
    print("=== Running Pilot Sobol & Convergence Battery ===")
    sample_sizes = [256, 512, 1024, 2048]
    convergence_records = []
    
    # Test convergence across sample sizes with seed=42
    results_by_N = {}
    for N in sample_sizes:
        t0 = time.time()
        param_values = sobol_sample.sample(problem_wide, N, calc_second_order=True, seed=42)
        evals = evaluate_model_batch(param_values)
        t_eval = time.time() - t0
        
        sobol_rs = sobol_analyze.analyze(problem_wide, evals['Rs'], calc_second_order=True, seed=42)
        results_by_N[N] = (sobol_rs, evals)
        
        for idx, name in enumerate(problem_wide['names']):
            s_i = sobol_rs['S1'][idx]
            s_ti = sobol_rs['ST'][idx]
            s_diff = s_ti - s_i
            s_i_conf = sobol_rs['S1_conf'][idx]
            s_ti_conf = sobol_rs['ST_conf'][idx]
            convergence_records.append({
                'N': N,
                'Total_Evaluations': len(param_values),
                'Time_s': round(t_eval, 2),
                'Parameter': name,
                'S1': float(s_i),
                'S1_conf': float(s_i_conf),
                'ST': float(s_ti),
                'ST_conf': float(s_ti_conf),
                'ST_minus_S1': float(s_diff)
            })
        print(f"Sample N={N} ({len(param_values)} evaluations) finished in {t_eval:.2f}s")

    df_conv = pd.DataFrame(convergence_records)
    df_conv.to_csv(os.path.join(DIRS['convergence'], 'sobol_convergence_by_N.csv'), index=False)

    # -------------------------------------------------------------
    # 5. RANDOM SEED STABILITY EXPERIMENT (at N=1024)
    # -------------------------------------------------------------
    seeds = [42, 123, 456, 789]
    seed_records = []
    sobol_by_seed = {}

    for s in seeds:
        param_vals = sobol_sample.sample(problem_wide, 1024, calc_second_order=True, seed=s)
        evals = evaluate_model_batch(param_vals)
        res_sobol = sobol_analyze.analyze(problem_wide, evals['Rs'], calc_second_order=True, seed=s)
        sobol_by_seed[s] = res_sobol
        
        for idx, name in enumerate(problem_wide['names']):
            seed_records.append({
                'Seed': s,
                'Parameter': name,
                'S1': float(res_sobol['S1'][idx]),
                'ST': float(res_sobol['ST'][idx]),
                'ST_minus_S1': float(res_sobol['ST'][idx] - res_sobol['S1'][idx])
            })
    
    df_seed = pd.DataFrame(seed_records)
    df_seed.to_csv(os.path.join(DIRS['pilot'], 'sobol_seed_stability.csv'), index=False)

    # Compute seed stability stats (mean, std, CV)
    seed_stats = df_seed.groupby('Parameter')[['S1', 'ST', 'ST_minus_S1']].agg(['mean', 'std']).reset_index()
    seed_stats.columns = ['Parameter', 'S1_mean', 'S1_std', 'ST_mean', 'ST_std', 'Diff_mean', 'Diff_std']
    seed_stats.to_csv(os.path.join(DIRS['pilot'], 'sobol_seed_stability_stats.csv'), index=False)

    # Extract reference Sobol results at N=1024, seed=42
    ref_sobol, ref_evals = results_by_N[1024]
    
    # Save S1 and ST table
    ref_df = pd.DataFrame({
        'Parameter': problem_wide['names'],
        'S1': ref_sobol['S1'],
        'S1_conf': ref_sobol['S1_conf'],
        'ST': ref_sobol['ST'],
        'ST_conf': ref_sobol['ST_conf'],
        'ST_minus_S1': ref_sobol['ST'] - ref_sobol['S1']
    })
    ref_df.to_csv(os.path.join(DIRS['pilot'], 'sobol_indices_N1024_seed42.csv'), index=False)

    # Save second order pairwise interactions S2
    s2_matrix = ref_sobol['S2']
    s2_conf_matrix = ref_sobol['S2_conf']
    s2_records = []
    for i in range(len(problem_wide['names'])):
        for j in range(i + 1, len(problem_wide['names'])):
            p1 = problem_wide['names'][i]
            p2 = problem_wide['names'][j]
            s2_records.append({
                'Pair': f"{p1} x {p2}",
                'Param1': p1,
                'Param2': p2,
                'S2': float(s2_matrix[i, j]),
                'S2_conf': float(s2_conf_matrix[i, j])
            })
    df_s2 = pd.DataFrame(s2_records).sort_values(by='S2', ascending=False)
    df_s2.to_csv(os.path.join(DIRS['interaction'], 'pairwise_interactions_S2.csv'), index=False)

    # Generate Convergence Plot
    plt.figure(figsize=(9, 5))
    for name in ['pctB', 'F', 'L', 'dp', 'T', 'dc']:
        sub = df_conv[df_conv['Parameter'] == name]
        plt.errorbar(sub['N'], sub['ST'], yerr=sub['ST_conf'], marker='o', lw=1.5, capsize=4, label=f'{name} (ST)')
    plt.xlabel('Base Sample Size N', fontsize=11)
    plt.ylabel('Total Sobol Index ST', fontsize=11)
    plt.title('Sobol Index ST Convergence vs Sample Size N', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(ncol=2)
    plt.tight_layout()
    plt.savefig(os.path.join(DIRS['convergence'], 'convergence_plot_ST.png'), dpi=300)
    plt.close()

    # Generate Interaction Plot (S1 vs ST)
    plt.figure(figsize=(8, 4.5))
    x = np.arange(len(problem_wide['names']))
    width = 0.35
    plt.bar(x - width/2, ref_df['S1'], width, label='First-Order S1', color='#2b5c8f', yerr=ref_df['S1_conf'], capsize=3)
    plt.bar(x + width/2, ref_df['ST'], width, label='Total-Order ST', color='#d95f02', yerr=ref_df['ST_conf'], capsize=3)
    plt.xticks(x, problem_wide['names'], fontsize=11)
    plt.ylabel('Sensitivity Index', fontsize=11)
    plt.title('Global Sensitivity Analysis: S1 vs ST for Resolution Rs', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(DIRS['interaction'], 'sobol_S1_ST_barchart.png'), dpi=300)
    plt.close()

    return results_by_N, df_conv, seed_stats, df_s2, ref_evals

# -------------------------------------------------------------
# 6. OFAT BASELINE EXPERIMENT
# -------------------------------------------------------------
def run_ofat_baseline(problem_wide):
    print("=== Running OFAT Baseline Experiment ===")
    comp1 = HPLCCompound(name='Paracetamol', retention_factor=1.8, peak_width_factor=1.0)
    comp2 = HPLCCompound(name='Caffeine', retention_factor=3.2, peak_width_factor=1.0)
    
    baseline = {
        'L': 15.0,
        'F': 1.0,
        'dp': 3.5,
        'pctB': 50.0,
        'T': 25.0,
        'dc': 4.6
    }
    
    # Baseline Rs
    p_base = HPLCParams(
        compounds=[comp1, comp2],
        column=ColumnParams(length_cm=baseline['L'], particle_size_um=baseline['dp'], internal_diameter_mm=baseline['dc'], temperature_c=baseline['T']),
        flow_rate_ml_min=baseline['F'],
        mobile_phase_organic_pct=baseline['pctB']
    )
    rs_base = simulate_hplc(p_base).peaks[1].resolution

    ofat_records = []
    ofat_curves = []
    n_points = 21

    for idx, name in enumerate(problem_wide['names']):
        low, high = problem_wide['bounds'][idx]
        grid = np.linspace(low, high, n_points)
        rs_vals = []
        for val in grid:
            cur = dict(baseline)
            cur[name] = val
            p = HPLCParams(
                compounds=[comp1, comp2],
                column=ColumnParams(length_cm=cur['L'], particle_size_um=cur['dp'], internal_diameter_mm=cur['dc'], temperature_c=cur['T']),
                flow_rate_ml_min=cur['F'],
                mobile_phase_organic_pct=cur['pctB']
            )
            res = simulate_hplc(p)
            rs_val = res.peaks[1].resolution
            rs_vals.append(rs_val)
            ofat_curves.append({
                'Parameter': name,
                'Value': val,
                'Normalized_Value': (val - low) / (high - low),
                'Rs': rs_val
            })

        delta_rs = max(rs_vals) - min(rs_vals)
        ofat_records.append({
            'Parameter': name,
            'Baseline_Value': baseline[name],
            'Range_Low': low,
            'Range_High': high,
            'Min_Rs': min(rs_vals),
            'Max_Rs': max(rs_vals),
            'Delta_Rs': delta_rs,
            'Local_Sensitivity_Slope': (rs_vals[-1] - rs_vals[0]) / (high - low)
        })

    df_ofat = pd.DataFrame(ofat_records)
    total_delta = df_ofat['Delta_Rs'].sum()
    df_ofat['OFAT_Normalized_Importance'] = df_ofat['Delta_Rs'] / total_delta
    df_ofat['OFAT_Rank'] = df_ofat['OFAT_Normalized_Importance'].rank(ascending=False).astype(int)
    df_ofat = df_ofat.sort_values(by='OFAT_Rank')
    df_ofat.to_csv(os.path.join(DIRS['ofat'], 'ofat_baseline_results.csv'), index=False)

    df_curves = pd.DataFrame(ofat_curves)
    df_curves.to_csv(os.path.join(DIRS['ofat'], 'ofat_response_curves.csv'), index=False)

    # Plot OFAT sweeps
    plt.figure(figsize=(8, 4.5))
    for name in problem_wide['names']:
        sub = df_curves[df_curves['Parameter'] == name]
        plt.plot(sub['Normalized_Value'], sub['Rs'], lw=2, label=name)
    plt.xlabel('Normalized Parameter Value (0 = Low, 1 = High)', fontsize=11)
    plt.ylabel('Resolution Rs', fontsize=11)
    plt.title('OFAT Baseline Response Profiles (Held at Center Point)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(DIRS['ofat'], 'ofat_response_curves.png'), dpi=300)
    plt.close()

    print("OFAT baseline complete. Saved to 06_OFAT_COMPARISON.")
    return df_ofat, df_curves

# -------------------------------------------------------------
# 7. RESPONSE SURFACE METHODOLOGY (RSM) COMPARISON
# -------------------------------------------------------------
def run_rsm_comparison(problem_wide, N=1024):
    print("=== Running Response Surface Methodology (RSM) Comparison ===")
    # Generate Latin Hypercube / Uniform sample across problem_wide
    np.random.seed(42)
    n_rsm = 200 # Standard DoE sample size
    bounds = np.array(problem_wide['bounds'])
    X_doe = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(n_rsm, problem_wide['num_vars']))
    evals_doe = evaluate_model_batch(X_doe)
    y_doe = evals_doe['Rs']

    # 1. Fit Linear (Main effects only) model
    reg_linear = LinearRegression().fit(X_doe, y_doe)
    y_pred_lin = reg_linear.predict(X_doe)
    r2_lin = r2_score(y_doe, y_pred_lin)
    rmse_lin = np.sqrt(mean_squared_error(y_doe, y_pred_lin))

    # 2. Fit Quadratic + Interaction (Standard Response Surface) model
    poly = PolynomialFeatures(degree=2, include_bias=True)
    X_poly = poly.fit_transform(X_doe)
    reg_poly = LinearRegression().fit(X_poly, y_doe)
    y_pred_poly = reg_poly.predict(X_poly)
    r2_poly = r2_score(y_doe, y_pred_poly)
    rmse_poly = np.sqrt(mean_squared_error(y_doe, y_pred_poly))

    # Test on an independent test set of 1000 points
    X_test = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(1000, problem_wide['num_vars']))
    y_test = evaluate_model_batch(X_test)['Rs']
    X_test_poly = poly.transform(X_test)
    y_test_pred_poly = reg_poly.predict(X_test_poly)
    r2_test_poly = r2_score(y_test, y_test_pred_poly)
    rmse_test_poly = np.sqrt(mean_squared_error(y_test, y_test_pred_poly))

    rsm_summary = {
        'DoE_Sample_Size': n_rsm,
        'Independent_Test_Size': 1000,
        'Linear_Model_R2': float(r2_lin),
        'Linear_Model_RMSE': float(rmse_lin),
        'Quadratic_RSM_Train_R2': float(r2_poly),
        'Quadratic_RSM_Train_RMSE': float(rmse_poly),
        'Quadratic_RSM_Test_R2': float(r2_test_poly),
        'Quadratic_RSM_Test_RMSE': float(rmse_test_poly),
        'RSM_Captures_99_Pct_Variance': bool(r2_test_poly > 0.98)
    }

    with open(os.path.join(DIRS['interaction'], 'rsm_comparison_summary.json'), 'w') as f:
        json.dump(rsm_summary, f, indent=2)

    # Plot RSM fit vs Actual
    plt.figure(figsize=(6.5, 5))
    plt.scatter(y_test, y_test_pred_poly, alpha=0.4, color='#2b5c8f', edgecolors='none', s=20)
    plt.plot([0, max(y_test)], [0, max(y_test)], 'r--', lw=2, label='1:1 Ideal Line')
    plt.xlabel('SimuPharm Actual Rs', fontsize=11)
    plt.ylabel('2nd-Order Polynomial (RSM) Predicted Rs', fontsize=11)
    plt.title(f'Conventional RSM (2nd-Order DoE) Prediction vs Model (R² = {r2_test_poly:.4f})', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(DIRS['interaction'], 'rsm_actual_vs_predicted.png'), dpi=300)
    plt.close()

    print("RSM comparison complete. Saved to 07_INTERACTION_ANALYSIS.")
    return rsm_summary

# -------------------------------------------------------------
# 8. FAILURE-BOUNDARY & APPLICABILITY DOMAIN ANALYSIS
# -------------------------------------------------------------
def run_failure_boundary_analysis(problem_wide):
    print("=== Running Failure-Boundary Analysis ===")
    # 2D Grid Sweep: %B (30 to 80) vs Flow Rate (0.5 to 2.0)
    pctB_grid = np.linspace(30.0, 80.0, 50)
    flow_grid = np.linspace(0.5, 2.0, 50)
    B_mesh, F_mesh = np.meshgrid(pctB_grid, flow_grid)
    
    comp1 = HPLCCompound(name='Paracetamol', retention_factor=1.8, peak_width_factor=1.0)
    comp2 = HPLCCompound(name='Caffeine', retention_factor=3.2, peak_width_factor=1.0)
    
    Rs_mesh = np.zeros_like(B_mesh)
    for i in range(B_mesh.shape[0]):
        for j in range(B_mesh.shape[1]):
            p = HPLCParams(
                compounds=[comp1, comp2],
                column=ColumnParams(length_cm=15.0, particle_size_um=3.5, internal_diameter_mm=4.6, temperature_c=25.0),
                flow_rate_ml_min=float(F_mesh[i, j]),
                mobile_phase_organic_pct=float(B_mesh[i, j])
            )
            Rs_mesh[i, j] = simulate_hplc(p).peaks[1].resolution

    # Monte Carlo Failure Probability over Wide Design Space (N=5000)
    np.random.seed(999)
    bounds = np.array(problem_wide['bounds'])
    X_mc = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(5000, 6))
    evals_mc = evaluate_model_batch(X_mc)
    Rs_mc = evals_mc['Rs']
    P_fail_15 = np.mean(Rs_mc < 1.5)
    P_fail_10 = np.mean(Rs_mc < 1.0)

    # Train a shallow decision tree to identify the failure boundary logic
    dt = DecisionTreeClassifier(max_depth=3, random_state=42)
    dt.fit(X_mc, Rs_mc < 1.5)
    tree_rules = export_text(dt, feature_names=problem_wide['names'])

    failure_summary = {
        'P_failure_Rs_lt_1_5': float(P_fail_15),
        'P_severe_failure_Rs_lt_1_0': float(P_fail_10),
        'Primary_Boundary_Rules': tree_rules
    }
    with open(os.path.join(DIRS['failure'], 'failure_boundary_summary.json'), 'w') as f:
        json.dump(failure_summary, f, indent=2)

    # Plot 2D Failure Map
    plt.figure(figsize=(7.5, 5.5))
    cs = plt.contourf(B_mesh, F_mesh, Rs_mesh, levels=20, cmap='viridis')
    cbar = plt.colorbar(cs)
    cbar.set_label('Resolution Rs', fontsize=11)
    
    # Overlay Rs = 1.5 failure boundary contour
    plt.contour(B_mesh, F_mesh, Rs_mesh, levels=[1.5], colors='red', linewidths=2.5)
    plt.text(65, 0.7, 'FAIL REGION\n(Rs < 1.5)', color='white', weight='bold', fontsize=11,
             bbox=dict(boxstyle='round', facecolor='red', alpha=0.7))
    plt.text(40, 1.6, 'ROBUST REGION\n(Rs >= 1.5)', color='white', weight='bold', fontsize=11,
             bbox=dict(boxstyle='round', facecolor='green', alpha=0.7))
    
    plt.xlabel('Mobile Phase Organic Modifier %B', fontsize=11)
    plt.ylabel('Flow Rate F (mL/min)', fontsize=11)
    plt.title('Design Space Robustness & Failure Boundary (Red Line: Rs = 1.5)', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(DIRS['failure'], 'failure_boundary_contour.png'), dpi=300)
    plt.close()

    print("Failure-boundary analysis complete. Saved to 08_FAILURE_BOUNDARY.")
    return failure_summary

# -------------------------------------------------------------
# 9. ROBUSTNESS TO PARAMETER RANGE CHOICE (Wide vs Narrow)
# -------------------------------------------------------------
def run_range_robustness_experiment(problem_wide, problem_narrow):
    print("=== Running Robustness to Range Choice Experiment ===")
    N = 1024
    # Evaluate narrow range
    param_vals_narrow = sobol_sample.sample(problem_narrow, N, calc_second_order=True, seed=42)
    evals_narrow = evaluate_model_batch(param_vals_narrow)
    sobol_narrow = sobol_analyze.analyze(problem_narrow, evals_narrow['Rs'], calc_second_order=True, seed=42)

    # Load wide reference results
    df_wide = pd.read_csv(os.path.join(DIRS['pilot'], 'sobol_indices_N1024_seed42.csv'))

    df_compare = pd.DataFrame({
        'Parameter': problem_wide['names'],
        'Wide_S1': df_wide['S1'],
        'Wide_ST': df_wide['ST'],
        'Wide_Diff': df_wide['ST_minus_S1'],
        'Narrow_S1': sobol_narrow['S1'],
        'Narrow_ST': sobol_narrow['ST'],
        'Narrow_Diff': sobol_narrow['ST'] - sobol_narrow['S1']
    })
    df_compare.to_csv(os.path.join(DIRS['params'], 'wide_vs_narrow_sobol_comparison.csv'), index=False)

    # Plot Comparison
    plt.figure(figsize=(9, 4.5))
    x = np.arange(len(problem_wide['names']))
    width = 0.35
    plt.bar(x - width/2, df_compare['Wide_ST'], width, label='Wide Space ST (Method Dev)', color='#1b9e77')
    plt.bar(x + width/2, df_compare['Narrow_ST'], width, label='Narrow Space ST (AQbD Robustness)', color='#d95f02')
    plt.xticks(x, problem_wide['names'], fontsize=11)
    plt.ylabel('Total Sobol Index ST', fontsize=11)
    plt.title('GSA Robustness to Operational Range Choice (Wide vs Narrow Space)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(DIRS['params'], 'range_sensitivity_comparison.png'), dpi=300)
    plt.close()

    print("Range robustness experiment complete. Saved to 03_PARAMETER_SPACE.")
    return df_compare

# -------------------------------------------------------------
# 10. PHYSICAL PLAUSIBILITY AUDIT & PRESSURE FILTER
# -------------------------------------------------------------
def run_physical_plausibility_audit(problem_wide):
    print("=== Running Physical Plausibility Audit ===")
    np.random.seed(1234)
    bounds = np.array(problem_wide['bounds'])
    X = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(5000, 6))
    evals = evaluate_model_batch(X)
    
    pressures = evals['pressure']
    tR2 = evals['tR2']
    Rs = evals['Rs']

    # Physical plausibility criteria:
    # 1. Backpressure <= 400 bar (standard analytical HPLC upper limit)
    # 2. Backpressure <= 600 bar (UHPLC intermediate limit)
    # 3. Analysis time tR2 <= 30 min (practical QC method throughput)
    # 4. Analysis time tR2 <= 45 min
    p_viol_400 = np.mean(pressures > 400.0)
    p_viol_600 = np.mean(pressures > 600.0)
    t_viol_30 = np.mean(tR2 > 30.0)
    
    # Combined physically valid domain: Pressure <= 400 bar AND tR2 <= 30 min
    valid_mask = (pressures <= 400.0) & (tR2 <= 30.0)
    frac_valid = np.mean(valid_mask)
    frac_invalid = 1.0 - frac_valid

    plausibility_summary = {
        'Fraction_Pressure_gt_400bar': float(p_viol_400),
        'Fraction_Pressure_gt_600bar': float(p_viol_600),
        'Fraction_RunTime_gt_30min': float(t_viol_30),
        'Total_Sampled_Domain': 1.0,
        'Physically_Valid_Domain': float(frac_valid),
        'Physically_Invalid_Domain': float(frac_invalid),
        'Max_Estimated_Pressure_bar': float(np.max(pressures)),
        'Min_Estimated_Pressure_bar': float(np.min(pressures)),
        'Mean_Estimated_Pressure_bar': float(np.mean(pressures))
    }
    with open(os.path.join(DIRS['audit'], 'physical_plausibility_summary.json'), 'w') as f:
        json.dump(plausibility_summary, f, indent=2)

    # Plot Pressure vs Particle Size / Flow Rate
    plt.figure(figsize=(7, 4.5))
    sc = plt.scatter(X[:, 2], pressures, c=X[:, 1], cmap='plasma', alpha=0.4, s=15)
    plt.axhline(400, color='red', linestyle='--', lw=2, label='HPLC Pressure Limit (400 bar)')
    plt.colorbar(sc, label='Flow Rate F (mL/min)')
    plt.xlabel('Particle Size dp (µm)', fontsize=11)
    plt.ylabel('Estimated Backpressure ΔP (bar)', fontsize=11)
    plt.title('Physical Plausibility: Hydraulic Backpressure vs Particle Size', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(DIRS['audit'], 'hydraulic_pressure_audit.png'), dpi=300)
    plt.close()

    print("Physical plausibility audit complete. Saved to 02_ENGINE_AUDIT.")
    return plausibility_summary

# -------------------------------------------------------------
# MAIN EXECUTION ROUTINE
# -------------------------------------------------------------
if __name__ == '__main__':
    t_start = time.time()
    print("Starting SimuPharm Phase 5.2 Computational Battery...")
    
    # Step 1: Engine forensic audit
    audit_res = run_forensic_engine_audit()
    
    # Step 2: Define parameter problems
    prob_wide, prob_narrow = define_parameter_problems()
    
    # Step 3: Run pilot Sobol & convergence
    res_N, df_conv, seed_stats, df_s2, ref_evals = run_pilot_sobol_experiments(prob_wide)
    
    # Step 4: Run OFAT baseline
    df_ofat, df_curves = run_ofat_baseline(prob_wide)
    
    # Step 5: Run RSM comparison
    rsm_res = run_rsm_comparison(prob_wide)
    
    # Step 6: Run Failure boundary analysis
    fail_res = run_failure_boundary_analysis(prob_wide)
    
    # Step 7: Run Range robustness experiment
    df_range = run_range_robustness_experiment(prob_wide, prob_narrow)
    
    # Step 8: Run Physical plausibility audit
    plaus_res = run_physical_plausibility_audit(prob_wide)
    
    total_time = time.time() - t_start
    print(f"=== Entire Phase 5.2 Computational Pipeline Completed in {total_time:.2f} seconds ===")
