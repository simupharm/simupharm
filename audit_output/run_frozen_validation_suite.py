import os
import json
import csv
import numpy as np
from playwright.sync_api import sync_playwright

dir1 = r'c:\Users\dsant\OneDrive\simupro - Copy\audit_output'
dir2 = r'C:\Users\dsant\.gemini\antigravity\brain\55a75768-f2c0-4fa0-b387-5baedff096a9\audit_output'
os.makedirs(dir1, exist_ok=True)
os.makedirs(dir2, exist_ok=True)

html_url = 'file:///' + os.path.abspath('hplc_simulator.html').replace('\\', '/')

print("Starting Phase 3 Frozen Simulator Execution Suite via Playwright...")

simulation_results = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(html_url)
    page.wait_for_timeout(1000)

    # 1. Benchmark Execution: Analgesic Mixture (Paracetamol, Caffeine, Aspirin, Ibuprofen)
    # Conditions: Flow 1.0 mL/min, Temp 30C, Column C18, across various %B and Gradients
    
    test_runs = []
    
    # Isocratic test runs
    for pb in [30, 40, 50, 60, 70]:
        test_runs.append({
            'run_id': f'ISO_B{pb}_F1.0_T30',
            'type': 'isocratic',
            'flowRate': 1.0,
            'columnTemp': 30,
            'columnType': 'C18',
            'percentB': pb,
            'gradientProgram': [{'time': 0, 'percentB': pb}, {'time': 15, 'percentB': pb}],
            'fault': 'none'
        })
        
    # Flow rate variation runs (at 50% B)
    for flow in [0.5, 0.8, 1.2, 1.5, 2.0]:
        test_runs.append({
            'run_id': f'FLOW_F{flow}_B50_T30',
            'type': 'flow_variation',
            'flowRate': flow,
            'columnTemp': 30,
            'columnType': 'C18',
            'percentB': 50,
            'gradientProgram': [{'time': 0, 'percentB': 50}, {'time': 15, 'percentB': 50}],
            'fault': 'none'
        })

    # Temperature variation runs (at 50% B)
    for temp in [25, 35, 40, 50]:
        test_runs.append({
            'run_id': f'TEMP_T{temp}_B50_F1.0',
            'type': 'temp_variation',
            'flowRate': 1.0,
            'columnTemp': temp,
            'columnType': 'C18',
            'percentB': 50,
            'gradientProgram': [{'time': 0, 'percentB': 50}, {'time': 15, 'percentB': 50}],
            'fault': 'none'
        })
        
    # Gradient runs (10% to 70% B over 8, 10, 12 min)
    for t_g in [8, 10, 12]:
        test_runs.append({
            'run_id': f'GRAD_10to70_tG{t_g}_F1.0_T30',
            'type': 'gradient',
            'flowRate': 1.0,
            'columnTemp': 30,
            'columnType': 'C18',
            'percentB': 10,
            'gradientProgram': [{'time': 0, 'percentB': 10, 'curve': 'linear'}, {'time': t_g, 'percentB': 70, 'curve': 'linear'}],
            'fault': 'none'
        })

    # Fault injection runs (at 50% B isocratic, and gradient)
    for f_type in ['air_bubble', 'column_degradation', 'leak', 'contamination', 'lamp_failure']:
        test_runs.append({
            'run_id': f'FAULT_{f_type.upper()}_ISO50',
            'type': 'fault',
            'flowRate': 1.0,
            'columnTemp': 30,
            'columnType': 'C18',
            'percentB': 50,
            'gradientProgram': [{'time': 0, 'percentB': 50}, {'time': 15, 'percentB': 50}],
            'fault': f_type
        })
        test_runs.append({
            'run_id': f'FAULT_{f_type.upper()}_GRAD10',
            'type': 'fault',
            'flowRate': 1.0,
            'columnTemp': 30,
            'columnType': 'C18',
            'percentB': 10,
            'gradientProgram': [{'time': 0, 'percentB': 10, 'curve': 'linear'}, {'time': 10, 'percentB': 70, 'curve': 'linear'}],
            'fault': f_type
        })

    print(f"Executing {len(test_runs)} simulation conditions in SimuPharm...")

    for run in test_runs:
        run_data = page.evaluate('''(run) => {
            const sim = window.SimuPharma.simulation;
            const PE = window.SimuPharma.PhysicsEngine || window.PhysicsEngine;
            
            const params = {
                flowRate: run.flowRate,
                columnTemp: run.columnTemp,
                wavelength: 254,
                injectionVolume: 10,
                concentration: 100,
                columnType: run.columnType,
                sample: 'Mixture',
                gradientProgram: run.gradientProgram,
                currentFault: run.fault
            };
            
            const out = sim.generateChromatogramData(params);
            
            // Also calculate pressure for this condition
            const pressure = sim.PhysicsEngine 
                ? sim.PhysicsEngine.calculatePressure(run.flowRate, run.percentB, run.columnType, run.columnTemp, 'acetonitrile')
                : (window.PhysicsEngine ? window.PhysicsEngine.calculatePressure(run.flowRate, run.percentB, run.columnType, run.columnTemp, 'acetonitrile') : 0);
            
            return {
                run_id: run.run_id,
                type: run.type,
                flowRate: run.flowRate,
                columnTemp: run.columnTemp,
                columnType: run.columnType,
                percentB: run.percentB,
                fault: run.fault,
                pressure_bar: pressure,
                peaks: out.peaks.map(p => ({
                    name: p.name,
                    rt: p.rt,
                    peakWidth: p.peakWidth,
                    height: p.height,
                    area: p.area,
                    sigma: p.sigma,
                    asymmetry: p.asymmetry
                }))
            };
        }''', run)
        
        simulation_results.append(run_data)

    browser.close()

print(f"All {len(simulation_results)} runs executed successfully!")

# Save raw simulation outputs
json_path1 = os.path.join(dir1, "phase3_raw_simulation_results.json")
json_path2 = os.path.join(dir2, "phase3_raw_simulation_results.json")
for jp in [json_path1, json_path2]:
    with open(jp, 'w', encoding='utf-8') as f:
        json.dump(simulation_results, f, indent=2)

print("Saved raw simulation results to JSON.")
