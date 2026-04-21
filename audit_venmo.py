import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = 'c:/Users/timot/ellesworld'
FILES = [
    'index.html', 'shop.html',
    'pages/shop.html', 'pages/about.html', 'pages/contact.html',
    'pages/product.html', 'pages/faq.html', 'pages/shipping-info.html',
    'pages/privacy-policy.html', 'pages/shipping-policy.html',
    'pages/terms-of-service.html', 'pages/return-policy.html',
    'pages/research-agreement.html',
]

KEYWORDS = ['venmo', 'zelle', 'EllesWorldResearch', '291-9669', '707']

for rel in FILES:
    path = ROOT + '/' + rel
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    hits = []
    for kw in KEYWORDS:
        idx = 0
        while True:
            found = c.lower().find(kw.lower(), idx)
            if found == -1:
                break
            hits.append((found, kw, c[max(0,found-30):found+120]))
            idx = found + 1
    if hits:
        print(f'\n=== {rel} ===')
        for pos, kw, ctx in hits:
            print(f'  [{kw}] at {pos}: {ctx.encode("ascii",errors="replace").decode()}')
