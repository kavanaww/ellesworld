import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('c:/Users/timot/ellesworld/pages/shop.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('<div class="footer-disclaimer">')
print(c[idx:idx+400].encode('ascii', errors='replace').decode())
