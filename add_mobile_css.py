import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = 'c:/Users/timot/ellesworld'

def inject_css(path, css_block):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    style_close = content.rfind('</style>')
    if style_close == -1:
        print(f'  WARNING: no </style> in {path}')
        return
    content = content[:style_close] + css_block + '\n  ' + content[style_close:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Updated: {path}')

# ─── pages/shop.html ─────────────────────────────────────────────────────────
SHOP_CSS = """
    /* ── Mobile additions ── */
    @media (max-width: 768px) {
      .product-grid { grid-template-columns: repeat(2, 1fr); }
      .page-header h1 { font-size: 28px; }
      .filter-bar { overflow-x: auto; flex-wrap: nowrap; }
      .filter-btn { flex-shrink: 0; }
      .modal input, .modal select, .modal textarea {
        width: 100%; box-sizing: border-box;
      }
      .modal button { width: 100%; }
      .checkout-btn { width: 100%; }
    }
    @media (max-width: 480px) {
      .product-grid { grid-template-columns: 1fr; }
      .filter-btn { font-size: 11px; padding: 6px 10px; }
      .modal { border-radius: 8px; }
    }"""

# ─── pages/product.html ──────────────────────────────────────────────────────
PRODUCT_CSS = """
    /* ── Mobile additions ── */
    @media (max-width: 768px) {
      .modal input, .modal select, .modal textarea {
        width: 100%; box-sizing: border-box;
      }
      .modal button { width: 100%; }
      .checkout-btn { width: 100%; }
    }
    @media (max-width: 480px) {
      .modal { border-radius: 8px; }
    }"""

# ─── index.html ──────────────────────────────────────────────────────────────
INDEX_CSS = """
    /* ── Mobile additions ── */
    @media (max-width: 768px) {
      .hero h1 { font-size: clamp(28px, 7vw, 40px); }
      .hero-sub { font-size: 14px; }
      .section h2 { font-size: 24px; }
      .cta-btn { width: 100%; text-align: center; }
    }"""

# ─── Simple policy/info pages (shared template) ──────────────────────────────
SIMPLE_CSS = """
    /* ── Mobile additions ── */
    @media (max-width: 480px) {
      .page-header h1 { font-size: 26px; }
      .content { padding: 32px 16px; }
    }"""

# ─── about.html ──────────────────────────────────────────────────────────────
ABOUT_CSS = """
    /* ── Mobile additions ── */
    @media (max-width: 480px) {
      .page-header h1 { font-size: 26px; }
      .footer-inner { grid-template-columns: 1fr; }
    }"""

# ─── contact.html ────────────────────────────────────────────────────────────
CONTACT_CSS = """
    /* ── Mobile additions ── */
    @media (max-width: 480px) {
      .page-header h1 { font-size: 26px; }
      .footer-inner { grid-template-columns: 1fr; }
      input, select, textarea { width: 100%; box-sizing: border-box; }
      button[type="submit"] { width: 100%; }
    }"""

# ─── research-agreement.html ─────────────────────────────────────────────────
AGREEMENT_CSS = """
    /* ── Mobile additions ── */
    @media (max-width: 480px) {
      .page-header h1 { font-size: 26px; }
      .footer-inner { grid-template-columns: 1fr; }
    }"""

print('Injecting mobile CSS...')
inject_css(ROOT + '/pages/shop.html', SHOP_CSS)
inject_css(ROOT + '/pages/product.html', PRODUCT_CSS)
inject_css(ROOT + '/index.html', INDEX_CSS)
inject_css(ROOT + '/pages/about.html', ABOUT_CSS)
inject_css(ROOT + '/pages/contact.html', CONTACT_CSS)
inject_css(ROOT + '/pages/research-agreement.html', AGREEMENT_CSS)

SIMPLE_PAGES = [
    'pages/faq.html',
    'pages/shipping-info.html',
    'pages/privacy-policy.html',
    'pages/shipping-policy.html',
    'pages/terms-of-service.html',
    'pages/return-policy.html',
]
for p in SIMPLE_PAGES:
    inject_css(ROOT + '/' + p, SIMPLE_CSS)

# shop.html (root, old copy) — same as pages/shop.html treatment
inject_css(ROOT + '/shop.html', SHOP_CSS)

print('\nDone.')
