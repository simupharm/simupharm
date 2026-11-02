import re

with open('hplc_simulator_script.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Find COMPOUND_LIBRARY section
start = text.find('const COMPOUND_LIBRARY = {')
end = text.find('};', start)
lib_text = text[start:end+2]

matches = re.findall(r'(\w+):\s*\{\s*name:\s*[\'"]([^\'"]+)', lib_text)
print(f"Total compounds in COMPOUND_LIBRARY in hplc_simulator_script.js: {len(matches)}")
for k, name in matches:
    print(f"  Key: {k:<15} Name: {name}")

# Also check backend/compounds/database.py
with open('backend/compounds/database.py', 'r', encoding='utf-8', errors='ignore') as f:
    db_text = f.read()

db_matches = re.findall(r'[\'"]([^\'"]+)[\'"]:\s*\{', db_text)
print(f"\nTotal compounds in backend/compounds/database.py: {len(db_matches)}")
for name in db_matches:
    print(f"  DB: {name}")
