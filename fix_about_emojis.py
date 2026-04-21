import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = 'c:/Users/timot/ellesworld/pages/about.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

for kw in ['Third-Party Tested', 'Discreet', 'Honest Communication', 'Trusted Sourcing', 'COA Available', 'Community First']:
    idx = c.find(kw)
    print(f'[{kw}]: {repr(c[idx-50:idx+4])}')
