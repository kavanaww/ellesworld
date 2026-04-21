import sys, io, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = 'c:/Users/timot/ellesworld'

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Extract components from pages/shop.html
# ══════════════════════════════════════════════════════════════════════════════
with open(ROOT + '/pages/shop.html', 'r', encoding='utf-8') as f:
    SHOP = f.read()

# ── Cart CSS (from .cart-btn to just before /* FOOTER */) ────────────────────
style_block = SHOP[422:14493]
cart_css_off = style_block.find('.cart-btn')
footer_css_off = style_block.find('/* FOOTER */')
CART_CSS = style_block[cart_css_off:footer_css_off].strip()

# ── Cart HTML — second cart-overlay + full checkout modal ────────────────────
second_cart_start = SHOP.find('<div class="cart-overlay"', SHOP.find('<div class="cart-overlay"') + 1)
script_start = SHOP.rfind('<script', 0, SHOP.rfind('</body>'))
modal_end = SHOP.rfind('</div>', second_cart_start, script_start) + len('</div>')
CART_HTML = SHOP[second_cart_start:modal_end]

# ── Cart JS — full script block with modifications ───────────────────────────
script_end = SHOP.rfind('</script>', 0, SHOP.rfind('</body>')) + len('</script>')
raw_script = SHOP[script_start:script_end]

# Modify for site-wide use:
# 1. sessionStorage → localStorage
cart_js = raw_script.replace("sessionStorage.setItem('ew_cart'", "localStorage.setItem('ew_cart'")
cart_js = cart_js.replace("sessionStorage.getItem('ew_cart'", "localStorage.getItem('ew_cart'")
# 2. Relative products.json path → absolute
cart_js = cart_js.replace('fetch("../products.json")', 'fetch("/products.json")')
cart_js = cart_js.replace("fetch('../products.json')", "fetch('/products.json')")
# 3. Guard renderShop so it only runs on shop pages
cart_js = cart_js.replace(
    '    renderShop("all");',
    '    if (document.getElementById("shopMain")) renderShop("all");'
)

# ── Cart button HTML ──────────────────────────────────────────────────────────
# Extract exact cart button from shop nav (preserving emoji character)
btn_idx = SHOP.find('class="cart-btn"')
btn_end = SHOP.find('</button>', btn_idx) + len('</button>')
CART_BTN = SHOP[btn_idx - 8 : btn_end]  # include the <button tag open

print(f'Cart CSS: {len(CART_CSS)} chars')
print(f'Cart HTML: {len(CART_HTML)} chars')
print(f'Cart JS: {len(cart_js)} chars')
print(f'Cart BTN: {repr(CART_BTN[:80].encode("ascii", errors="replace").decode())}')

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Update existing cart pages to use localStorage
# ══════════════════════════════════════════════════════════════════════════════
EXISTING_CART_PAGES = ['pages/shop.html', 'pages/product.html', 'shop.html']

for rel in EXISTING_CART_PAGES:
    path = ROOT + '/' + rel
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    content = content.replace("sessionStorage.setItem('ew_cart'", "localStorage.setItem('ew_cart'")
    content = content.replace("sessionStorage.getItem('ew_cart'", "localStorage.getItem('ew_cart'")
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated storage: {rel}')
    else:
        print(f'No storage change needed: {rel}')

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Inject cart into pages that don't have it
# ══════════════════════════════════════════════════════════════════════════════
all_files = sorted(glob.glob(ROOT + '/**/*.html', recursive=True))

NAV_TOGGLE_PATTERN = '<button class="nav-toggle"'

for path in all_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip pages that already have the cart
    if 'id="cartCount"' in content:
        print(f'SKIP (has cart): {path}')
        continue

    changes = []

    # ── A. Inject cart CSS before </style> ──────────────────────────────────
    style_close = content.rfind('</style>')
    if style_close != -1:
        css_block = '\n    /* ── Cart & Checkout CSS ── */\n    ' + CART_CSS.replace('\n', '\n    ') + '\n  '
        content = content[:style_close] + css_block + content[style_close:]
        changes.append('CSS')
    else:
        changes.append('WARN: no </style>')

    # ── B. Wrap nav-toggle with cart btn in a flex div ───────────────────────
    toggle_idx = content.find(NAV_TOGGLE_PATTERN)
    if toggle_idx != -1:
        toggle_end = content.find('</button>', toggle_idx) + len('</button>')
        toggle_html = content[toggle_idx:toggle_end]
        # Build the replacement: cart btn + toggle wrapped in flex div
        wrapped = (
            '<div style="display:flex;align-items:center;gap:12px;">\n    '
            + CART_BTN + '\n    '
            + toggle_html
            + '\n  </div>'
        )
        content = content[:toggle_idx] + wrapped + content[toggle_end:]
        changes.append('nav btn')
    else:
        changes.append('WARN: no nav-toggle found')

    # ── C. Inject cart HTML + script before </body> ──────────────────────────
    body_close = content.rfind('</body>')
    if body_close != -1:
        inject = '\n\n<!-- SITE-WIDE CART -->\n' + CART_HTML + '\n\n' + cart_js + '\n'
        content = content[:body_close] + inject + content[body_close:]
        changes.append('HTML+JS')
    else:
        changes.append('WARN: no </body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Injected [{", ".join(changes)}]: {path}')

print('\nDone.')
