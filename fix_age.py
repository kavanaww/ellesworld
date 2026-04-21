import re, sys, io
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

REPLACEMENTS = [
    (r'18\+',        '21+'),
    (r'18 years',    '21 years'),
    (r'[Mm]ust be 18', lambda m: m.group(0).replace('18', '21')),
]

for rel in FILES:
    path = ROOT + '/' + rel
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original
    hits = []
    for pattern, repl in REPLACEMENTS:
        new, n = re.subn(pattern, repl, content, flags=re.IGNORECASE)
        if n:
            hits.append(f'{pattern!r} x{n}')
            content = new

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{rel}: {"; ".join(hits)}')
    else:
        print(f'{rel}: no matches')
