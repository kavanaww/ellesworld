import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = 'c:/Users/timot/ellesworld'

for fname, checks in [
    ('pages/shop.html', ['venmo-note">', '@EllesWorldResearch</a>', '291-9669</a>', 'step2', 'on Venmo to complete', 'via Zelle to']),
    ('shop.html',       ['venmo-note">', '@EllesWorldResearch</a>', 'on Venmo']),
    ('index.html',      ['Preferred payment']),
]:
    with open(ROOT + '/' + fname, 'r', encoding='utf-8') as f:
        c = f.read()
    print(f'\n=== {fname} ===')
    for kw in checks:
        idx = c.find(kw)
        if idx != -1:
            print(f'  [{kw}]: {repr(c[idx:idx+160].encode("ascii", errors="replace").decode())}')
        else:
            print(f'  [{kw}]: NOT FOUND')
