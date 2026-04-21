import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

root = 'c:/Users/timot/ellesworld'

with open(root + '/pages/shop.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Find the injected block
idx = c.find('Mobile additions')
print('pages/shop.html injection:')
print(c[idx:idx+500].encode('ascii', errors='replace').decode())
