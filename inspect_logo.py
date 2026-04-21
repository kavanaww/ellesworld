import os

files = [
    'index.html',
    'shop.html',
    'pages/shop.html',
    'pages/about.html',
    'pages/contact.html',
    'pages/product.html',
    'pages/faq.html',
    'pages/shipping-info.html',
    'pages/privacy-policy.html',
    'pages/shipping-policy.html',
    'pages/terms-of-service.html',
    'pages/return-policy.html',
    'pages/research-agreement.html',
]

root = 'c:/Users/timot/ellesworld'

for f in files:
    path = root + '/' + f
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()

    # Find nav logo area
    nav_idx = content.find('<nav')
    nav_end = content.find('</nav>', nav_idx) + len('</nav>') if nav_idx != -1 else -1
    nav_chunk = content[nav_idx:nav_end] if nav_idx != -1 else ''

    # Check for img tag in nav
    img_idx = nav_chunk.find('<img')
    img_end = nav_chunk.find('>', img_idx) + 1 if img_idx != -1 else -1
    img_tag = nav_chunk[img_idx:img_end] if img_idx != -1 else 'NO IMG'

    # Check for logo text/class in nav
    has_base64 = 'data:image/png;base64' in nav_chunk
    has_logo_class = 'nav-logo' in nav_chunk or 'logo' in nav_chunk.lower()

    # Check for favicon
    head_idx = content.find('<head>')
    head_end = content.find('</head>', head_idx) + len('</head>') if head_idx != -1 else -1
    head_chunk = content[head_idx:head_end] if head_idx != -1 else ''
    has_favicon = 'rel="icon"' in head_chunk or "rel='icon'" in head_chunk

    print(f'\n=== {f} ===')
    print(f'  Has base64 img in nav: {has_base64}')
    print(f'  Has logo class in nav: {has_logo_class}')
    print(f'  Has favicon: {has_favicon}')
    if img_idx != -1:
        # Just show first 120 chars of img tag
        print(f'  Nav img tag: {img_tag[:120]}')
    # Also check for nav-logo or logo div/span
    for kw in ['nav-logo', 'brand-name', 'footer-brand-name']:
        kidx = content.find(kw)
        if kidx != -1:
            print(f'  Found "{kw}" at char {kidx}: {repr(content[kidx:kidx+80])}')
