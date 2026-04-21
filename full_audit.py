import sys, io, os, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = 'c:/Users/timot/ellesworld'
PAGES = ROOT + '/pages'

FILES = {
    'index.html':                      ROOT + '/index.html',
    'shop.html':                       ROOT + '/shop.html',
    'pages/shop.html':                 PAGES + '/shop.html',
    'pages/product.html':              PAGES + '/product.html',
    'pages/about.html':                PAGES + '/about.html',
    'pages/contact.html':              PAGES + '/contact.html',
    'pages/faq.html':                  PAGES + '/faq.html',
    'pages/shipping-info.html':        PAGES + '/shipping-info.html',
    'pages/privacy-policy.html':       PAGES + '/privacy-policy.html',
    'pages/shipping-policy.html':      PAGES + '/shipping-policy.html',
    'pages/terms-of-service.html':     PAGES + '/terms-of-service.html',
    'pages/return-policy.html':        PAGES + '/return-policy.html',
    'pages/research-agreement.html':   PAGES + '/research-agreement.html',
}

ISSUES = []

def fail(check, file, detail):
    ISSUES.append((check, file, detail))
    print(f'  FAIL [{check}] {file}: {detail}')

def ok(check, detail=''):
    pass  # silent pass

# Load all files
contents = {}
for name, path in FILES.items():
    with open(path, 'r', encoding='utf-8') as f:
        contents[name] = f.read()

print('=' * 60)
print('AUDIT RESULTS')
print('=' * 60)

# ── 1. Favicon ────────────────────────────────────────────────
print('\n[1] Favicon')
for name, c in contents.items():
    if 'href="/assets/logo2.png"' not in c or 'rel="icon"' not in c:
        fail('favicon', name, 'Missing or wrong favicon href')
    else:
        ok('favicon')

# ── 2. Age gate ───────────────────────────────────────────────
print('\n[2] Age gate')
for name, c in contents.items():
    count = c.count('id="ew-age-gate"')
    if count == 0:
        fail('age-gate', name, 'Missing age gate')
    elif count > 1:
        fail('age-gate', name, f'Duplicate age gate ({count}x)')
    if "localStorage.getItem('ew_confirmed')" not in c:
        fail('age-gate', name, 'Missing localStorage check in gate')

# ── 3. Cart system ────────────────────────────────────────────
print('\n[3] Cart system')
for name, c in contents.items():
    missing = [el for el in ['id="cartCount"','id="cartOverlay"','id="cartDrawer"','id="modalOverlay"','onclick="openCart()"']
               if el not in c]
    if missing:
        fail('cart', name, f'Missing: {missing}')
    # Check for duplicate cart elements
    for el_id in ['cartCount', 'cartOverlay', 'cartDrawer', 'modalOverlay']:
        cnt = c.count(f'id="{el_id}"')
        if cnt > 1:
            fail('cart-dup', name, f'Duplicate id="{el_id}" ({cnt}x)')

# ── 4. sessionStorage (cart) ──────────────────────────────────
print('\n[4] Cart storage')
for name, c in contents.items():
    if "sessionStorage.setItem('ew_cart'" in c or "sessionStorage.getItem('ew_cart'" in c:
        fail('storage', name, 'Still uses sessionStorage for ew_cart')
    if "localStorage.setItem('ew_cart'" not in c and "localStorage.getItem('ew_cart'" not in c:
        fail('storage', name, 'No localStorage ew_cart found')

# ── 5. Research agreement checkbox ────────────────────────────
print('\n[5] Research agreement checkbox')
# Only pages with checkout modal need this
for name in ['pages/shop.html', 'pages/product.html', 'index.html', 'pages/about.html',
             'pages/contact.html', 'pages/faq.html', 'pages/shipping-info.html',
             'pages/privacy-policy.html', 'pages/shipping-policy.html',
             'pages/terms-of-service.html', 'pages/return-policy.html',
             'pages/research-agreement.html', 'shop.html']:
    c = contents[name]
    if 'id="modalOverlay"' in c and 'researchAgreementCheck' not in c:
        fail('research-checkbox', name, 'Has checkout modal but missing researchAgreementCheck')

# ── 6. 21+ language ───────────────────────────────────────────
print('\n[6] Age language')
for name, c in contents.items():
    matches = re.findall(r'18\+|18 years|[Mm]ust be 18', c)
    if matches:
        fail('age-lang', name, f'Found: {matches}')

# ── 7. Disclaimer bar in pages/shop.html ──────────────────────
print('\n[7] Disclaimer bar')
c = contents['pages/shop.html']
if 'disclaimer-bar' not in c:
    fail('disclaimer', 'pages/shop.html', 'Missing disclaimer-bar')
else:
    disc_idx = c.find('<div class="disclaimer-bar"')
    if disc_idx == -1:
        disc_idx = c.find('disclaimer-bar', c.find('<body'))
    disc_text = c[disc_idx:disc_idx+300]
    if '21+' not in disc_text:
        fail('disclaimer', 'pages/shop.html', '21+ not in disclaimer bar')
    if 'research-agreement.html' not in disc_text:
        fail('disclaimer', 'pages/shop.html', 'link to research-agreement.html missing from disclaimer')

# ── 8. Product card links (pages/shop.html) ───────────────────
print('\n[8] Product card links')
c = contents['pages/shop.html']
if 'product.html?id=' not in c:
    fail('product-links', 'pages/shop.html', 'No product.html?id= links found')

# ── 9. products.json absolute path ───────────────────────────
print('\n[9] products.json fetch path')
for name in ['pages/shop.html', 'pages/product.html']:
    c = contents[name]
    if 'fetch("../products.json")' in c or "fetch('../products.json')" in c:
        fail('fetch-path', name, 'Still uses relative ../products.json path')
    if 'fetch("/products.json")' not in c and "fetch('/products.json')" not in c:
        fail('fetch-path', name, 'No absolute /products.json fetch found')

# ── 10. No placeholder research links ────────────────────────
print('\n[10] products.json placeholders')
with open(ROOT + '/products.json', 'r', encoding='utf-8') as f:
    pj = json.load(f)
placeholder_found = []
for p in pj:
    for link in p.get('researchLinks', []):
        if link.get('url') == '#' or 'title here' in link.get('title','').lower():
            placeholder_found.append(p['id'])
if placeholder_found:
    fail('placeholders', 'products.json', f'Placeholder links in product ids: {placeholder_found}')

# ── 11. Footer: present, not duplicate ───────────────────────
print('\n[11] Footer')
for name, c in contents.items():
    footer_count = c.count('<footer')
    if footer_count == 0:
        fail('footer', name, 'Missing footer')
    elif footer_count > 1:
        fail('footer-dup', name, f'Duplicate footer ({footer_count}x)')
    if 'footer-disclaimer' not in c:
        fail('footer', name, 'Missing footer-disclaimer')
    if 'footer-bottom' not in c:
        fail('footer', name, 'Missing footer-bottom')

# ── 12. Duplicate navbars ─────────────────────────────────────
print('\n[12] Nav duplicates')
for name, c in contents.items():
    nav_count = len(re.findall(r'<nav\b', c))
    if nav_count > 1:
        fail('nav-dup', name, f'Duplicate nav ({nav_count}x)')
    if nav_count == 0:
        fail('nav-missing', name, 'No nav element')

# ── 13. About.html emojis ────────────────────────────────────
print('\n[13] About.html emojis')
c = contents['pages/about.html']
expected = ['\U0001f468\u200d\U0001f52c', '\U0001f4e6', '\U0001f932',
            '\U0001f30d', '\U0001f4c4']
for emoji in expected:
    if emoji not in c:
        fail('about-emoji', 'pages/about.html', f'Missing emoji: {repr(emoji)}')
if '/assets/logo2.png' not in c or 'Community First' not in c:
    fail('about-emoji', 'pages/about.html', 'Community First card missing logo2.png img')
else:
    # Check logo2.png is in the Community First card
    cf_idx = c.find('Community First')
    card_start = c.rfind('<div', 0, cf_idx)
    if '/assets/logo2.png' not in c[card_start:cf_idx+50]:
        fail('about-emoji', 'pages/about.html', 'logo2.png not in Community First card value-icon')

# ── 14. Logo references ───────────────────────────────────────
print('\n[14] Logo references')
# Nav logo should be /assets/logo.png on all pages
# Favicon should be /assets/logo2.png
# About Community First card: /assets/logo2.png
for name, c in contents.items():
    # Check favicon
    m = re.search(r'rel="icon"[^>]*href="([^"]+)"', c)
    if not m:
        m = re.search(r'href="([^"]+)"[^>]*rel="icon"', c)
    if m and m.group(1) != '/assets/logo2.png':
        fail('logo', name, f'Favicon uses {m.group(1)} instead of /assets/logo2.png')
    # Nav logo should use /assets/logo.png (or logo2)
    nav_start = c.find('<nav')
    nav_end = c.find('</nav>', nav_start)
    nav = c[nav_start:nav_end] if nav_start != -1 else ''
    if '/assets/logo' not in nav:
        fail('logo', name, 'Nav has no logo img')

# ── 15. Mobile responsiveness ────────────────────────────────
print('\n[15] Mobile responsiveness')
for name, c in contents.items():
    if '@media (max-width: 768px)' not in c:
        fail('mobile', name, 'No 768px media query')
    else:
        # Check for nav collapse
        m768_idx = c.find('@media (max-width: 768px)')
        region = c[m768_idx:m768_idx+500]
        if '.nav-links' not in region or 'display: none' not in region:
            fail('mobile', name, 'nav-links not hidden in 768px media query')

# ── 16. Venmo and Zelle together ─────────────────────────────
print('\n[16] Venmo + Zelle')
for name, c in contents.items():
    has_venmo = 'venmo' in c.lower()
    has_zelle = 'zelle' in c.lower()
    if has_venmo and not has_zelle:
        fail('payment', name, 'Venmo mentioned but Zelle is missing')
    # Check links on pages with payment display
    if 'venmo.com/EllesWorldResearch' in c:
        if 'tel:7072919669' not in c:
            fail('payment', name, '@EllesWorldResearch linked but Zelle tel: link missing')

# ── 17. Internal links ───────────────────────────────────────
print('\n[17] Internal links')
for name, c in contents.items():
    base_dir = os.path.dirname(ROOT + '/' + name)
    hrefs = re.findall(r'href="([^"#]+)"', c)
    for href in hrefs:
        # Skip external, tel:, mailto:, JS, template literals
        if href.startswith(('http','mailto:','tel:','javascript')):
            continue
        if '${' in href:
            continue
        # Skip query strings to product.html
        href_clean = href.split('?')[0]
        # Resolve relative to file location
        if href_clean.startswith('/'):
            target = ROOT + href_clean
        else:
            target = os.path.normpath(os.path.join(base_dir, href_clean))
        if not os.path.exists(target):
            fail('broken-link', name, f'Broken: {href} -> {target}')

# ── 18. CSS variables ────────────────────────────────────────
print('\n[18] CSS variables')
for name, c in contents.items():
    if '--red:' not in c and '--red :' not in c:
        fail('css-vars', name, 'Missing --red CSS variable definition')

# ── 19. Google Fonts ─────────────────────────────────────────
print('\n[19] Google Fonts')
for name, c in contents.items():
    if 'fonts.googleapis.com' not in c:
        fail('fonts', name, 'Missing Google Fonts link')
    elif 'Playfair' not in c:
        fail('fonts', name, 'Playfair Display not in fonts link')

# ── 20. Duplicate cart HTML elements ─────────────────────────
print('\n[20] Extra: cart HTML')
for name, c in contents.items():
    co = c.count('<div class="cart-overlay"')
    cd = c.count('<div class="cart-drawer"')
    mo = c.count('<div class="modal-overlay"')
    if co > 1: fail('cart-dup', name, f'Duplicate cart-overlay ({co}x)')
    if cd > 1: fail('cart-dup', name, f'Duplicate cart-drawer ({cd}x)')
    if mo > 1: fail('cart-dup', name, f'Duplicate modal-overlay ({mo}x)')

# ── Summary ───────────────────────────────────────────────────
print('\n' + '=' * 60)
if not ISSUES:
    print('ALL CHECKS PASSED - No issues found')
else:
    print(f'ISSUES FOUND: {len(ISSUES)}')
    print('=' * 60)
    for check, file, detail in ISSUES:
        print(f'  [{check}] {file}: {detail}')
