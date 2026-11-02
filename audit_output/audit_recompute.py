import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('phase3_simulation_outputs.csv')
p3_stats = pd.read_csv('phase3_validation_statistics.csv')

print('--- INDEPENDENT STATISTICAL RECOMPUTATION ---')
recomputed_rows = []

domain_map = [
    ("Isocratic 50% B Standard Conditions", df[(df['mode']=='isocratic') & (df['percentB']==50) & (df['flow_rate']==1.0) & (df['temp_C']==30) & (df['fault']=='none')]),
    ("Isocratic Flow Sweep (0.5 - 2.0 mL/min)", df[df['run_id'].str.contains('FLOW')]),
    ("Isocratic Temp Sweep (25 - 50 C)", df[df['run_id'].str.contains('TEMP')]),
    ("Gradient Elution (10% to 70% B over 8-12 min)", df[df['run_id'].str.contains('GRAD') & (df['fault']=='none')]),
    ("All Nominal Baseline Runs (No Faults)", df[df['fault']=='none']),
    ("Fault Injected Runs", df[df['fault']!='none']),
    ("Entire Dataset (All 108 Simulated Peaks)", df)
]

for dom_name, sub in domain_map:
    exp = sub['exp_tR_min'].values
    sim = sub['sim_tR_min'].values
    n = len(sub)
    diff = sim - exp
    abs_diff = np.abs(diff)
    pct_err = (diff / exp) * 100.0
    abs_pct_err = np.abs(pct_err)
    
    mae = float(np.mean(abs_diff))
    mse = float(np.mean(diff**2))
    rmse = float(np.sqrt(mse))
    mape = float(np.mean(abs_pct_err))
    med_ae = float(np.median(abs_diff))
    med_pe = float(np.median(abs_pct_err))
    max_ae = float(np.max(abs_diff))
    bias = float(np.mean(diff))
    sd_diff = float(np.std(diff, ddof=1)) if n > 1 else 0.0
    cv_pct = float((sd_diff / np.mean(exp)) * 100.0) if np.mean(exp) > 0 else 0.0
    
    if n > 1 and np.std(exp) > 0 and np.std(sim) > 0:
        pearson_r, _ = stats.pearsonr(exp, sim)
        spearman_rho, _ = stats.spearmanr(exp, sim)
        r2 = float(pearson_r**2)
    else:
        pearson_r, spearman_rho, r2 = 1.0, 1.0, 1.0
        
    # Bland-Altman
    loa_lower = bias - 1.96 * sd_diff
    loa_upper = bias + 1.96 * sd_diff
    
    # TOST
    theta = 0.10 * float(np.mean(exp))
    se = sd_diff / np.sqrt(n) if n > 1 and sd_diff > 0 else 0.001
    t1 = (bias - (-theta)) / se
    t2 = (theta - bias) / se
    p_tost = float(max(1 - stats.t.cdf(t1, df=max(1, n-1)), 1 - stats.t.cdf(t2, df=max(1, n-1)))) if n > 1 else 0.05
    
    recomputed_rows.append({
        'domain': dom_name,
        'n': n,
        'mean_exp': float(np.mean(exp)),
        'mean_sim': float(np.mean(sim)),
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'mape': mape,
        'med_ae': med_ae,
        'med_pe': med_pe,
        'max_ae': max_ae,
        'bias': bias,
        'sd_diff': sd_diff,
        'cv_pct': cv_pct,
        'loa_lower': loa_lower,
        'loa_upper': loa_upper,
        'r2': r2,
        'pearson_r': pearson_r,
        'spearman_rho': spearman_rho,
        'tost_p': p_tost
    })

df_recomp = pd.DataFrame(recomputed_rows)
print(df_recomp[['domain', 'n', 'mae', 'rmse', 'mape', 'bias', 'r2', 'tost_p']].to_string())
