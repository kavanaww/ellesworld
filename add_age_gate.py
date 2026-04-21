import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('c:/Users/timot/ellesworld/pages/shop.html', 'r', encoding='utf-8') as f:
    c = f.read()

body_idx = c.find('<body')
print(c[body_idx:body_idx+200].encode('ascii', errors='replace').decode())
print('...')
gate_idx = c.find('ew-age-gate')
print(f'Gate found at char {gate_idx}')
end_gate = c.find('END EW AGE GATE')
print(f'Gate ends at char {end_gate}')
print(f'localStorage check present: {"ew_confirmed" in c}')
print(f'ewEnterSite present: {"ewEnterSite" in c}')
