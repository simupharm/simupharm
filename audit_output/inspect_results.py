import json

with open('audit_output/phase3_raw_simulation_results.json', 'r') as f:
    data = json.load(f)

print(f"Total runs: {len(data)}")
for d in data[:10]:
    print(f"\nRun: {d['run_id']} | Type: {d['type']} | P = {d['pressure_bar']} bar")
    for p in d['peaks'][:4]:
        print(f"   {p['name']:<30} tR = {p['rt']:.3f} min | w = {p['peakWidth']:.4f} min | As = {p['asymmetry']:.2f}")
