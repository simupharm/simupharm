import re

with open("hplc_simulator_script.js", "r", encoding="utf-8") as f:
    text = f.read()

# Look for compound databases or mixtures
print("--- COMPOUND / MIXTURE SEARCH ---")
matches = re.findall(r"name:\s*[\"']([^\"']+)[\"']", text)
print("Total name occurrences:", len(matches))
unique_names = sorted(list(set(matches)))
print("First 30 names:", unique_names[:30])

# Look for fault definitions
print("\n--- FAULT DEFINITIONS ---")
fault_matches = re.findall(r"['\"]?([a-zA-Z_]+)['\"]?\s*:\s*\{[^}]*type:\s*['\"]fault['\"]", text)
print("Fault matches:", fault_matches)
for match in re.finditer(r"(const|let|var)\s+([a-zA-Z0-9_]*fault[a-zA-Z0-9_]*)\s*=", text, re.I):
    print("Fault var:", match.group(0))

# Look for ES6 arrow functions or object methods
arrow_funcs = re.findall(r"(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(?:\([^)]*\)|[a-zA-Z0-9_]+)\s*=>", text)
print("Arrow functions found:", len(arrow_funcs))
chem_arrows = [fn for fn in arrow_funcs if any(k in fn.lower() for k in ['retention', 'deemter', 'plate', 'pressure', 'peak', 'fault', 'simulate', 'calculate', 'noise', 'run'])]
print("Chem/simulation arrow functions:", chem_arrows)

# Look for object keys
obj_methods = re.findall(r"([a-zA-Z0-9_]+)\s*\([^)]*\)\s*\{", text)
print("Object methods found:", len(obj_methods))
chem_methods = [fn for fn in obj_methods if any(k in fn.lower() for k in ['retention', 'deemter', 'plate', 'pressure', 'peak', 'fault', 'simulate', 'calculate', 'noise', 'run'])]
print("Chem/simulation methods:", chem_methods[:25])

