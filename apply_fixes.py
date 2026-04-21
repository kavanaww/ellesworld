ROOT  = 'c:/Users/timot/ellesworld'
PAGES = ROOT + '/pages'

# ── Shared footer CSS to inject into shop files ──────────────────────────────
FOOTER_CSS = """
    /* FOOTER */
    .footer { background: #1A1A1A; color: rgba(255,255,255,0.7); }
    .footer-inner { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 48px; padding: 60px 80px 48px; max-width: 1280px; margin: 0 auto; }
    .footer-brand-name { font-family: "Playfair Display", serif; font-size: 22px; font-weight: 700; color: #fff; margin-bottom: 10px; }
    .footer-brand-name span { color: var(--teal); }
    .footer-tagline { font-size: 13px; color: rgba(255,255,255,0.45); line-height: 1.7; margin-bottom: 20px; }
    .footer-subscribe { display: flex; margin-top: 4px; }
    .subscribe-input { flex: 1; padding: 10px 14px; font-size: 13px; font-family: "DM Sans", sans-serif; border: 1px solid rgba(255,255,255,0.15); background: rgba(255,255,255,0.07); color: #fff; border-radius: 3px 0 0 3px; outline: none; }
    .subscribe-input::placeholder { color: rgba(255,255,255,0.35); }
    .subscribe-btn { padding: 10px 18px; font-size: 12px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; background: var(--red); color: #fff; border: none; border-radius: 0 3px 3px 0; cursor: pointer; font-family: "DM Sans", sans-serif; transition: background 0.2s; }
    .subscribe-btn:hover { background: var(--red-dark); }
    .footer h4 { font-size: 10px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(255,255,255,0.35); margin-bottom: 16px; }
    .footer-col ul { display: flex; flex-direction: column; gap: 10px; }
    .footer-col a { font-size: 14px; color: rgba(255,255,255,0.65); transition: color 0.2s; }
    .footer-col a:hover { color: #fff; }
    .footer-disclaimer { border-top: 1px solid rgba(255,255,255,0.07); padding: 20px 80px; text-align: center; font-size: 11px; color: rgba(255,255,255,0.4); line-height: 1.7; }
    .footer-bottom { border-top: 1px solid rgba(255,255,255,0.07); padding: 16px 80px; text-align: center; font-size: 11px; color: rgba(255,255,255,0.28); letter-spacing: 0.04em; }"""

FOOTER_RESPONSIVE = """
    @media (max-width: 768px) {
      .footer-inner { grid-template-columns: 1fr 1fr; padding: 40px 24px; gap: 32px; }
      .footer-disclaimer { padding: 16px 24px; }
      .footer-bottom { padding: 16px 24px; }
    }
    @media (max-width: 480px) {
      .footer-inner { grid-template-columns: 1fr; }
    }"""

# Subpage footer HTML (pages/ relative paths)
FOOTER_HTML_SUB = """
<footer class="footer">
  <div class="footer-inner">
    <div class="footer-col footer-brand">
      <div class="footer-brand-name">Elle's <span>World</span> Research</div>
      <p class="footer-tagline">Research peptides for qualified researchers. Third-party tested. Not for human consumption.</p>
      <div class="footer-subscribe">
        <input type="email" class="subscribe-input" placeholder="Your email address" />
        <button class="subscribe-btn">Subscribe</button>
      </div>
    </div>
    <div class="footer-col">
      <h4>Quick Menu</h4>
      <ul>
        <li><a href="../index.html">Home</a></li>
        <li><a href="shop.html">Shop</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Information</h4>
      <ul>
        <li><a href="shipping-info.html">Shipping Info</a></li>
        <li><a href="about.html">Our Story</a></li>
        <li><a href="faq.html">FAQ</a></li>
        <li><a href="contact.html">Track Order</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Legal</h4>
      <ul>
        <li><a href="privacy-policy.html">Privacy Policy</a></li>
        <li><a href="shipping-policy.html">Shipping Policy</a></li>
        <li><a href="terms-of-service.html">Terms of Service</a></li>
        <li><a href="return-policy.html">Return Policy</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-disclaimer">All products available on this site are strictly designated for research use only. They are not intended for human or veterinary administration, and no diagnostic, therapeutic, or clinical application is implied, warranted, or permitted.</div>
  <div class="footer-bottom">&copy; 2026 Elle's World Research. All Rights Reserved.</div>
</footer>"""


def inject_footer_into_shop(path, footer_html):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject CSS before </style>
    style_close = content.rfind('</style>')
    if style_close == -1:
        print(f'  WARNING: </style> not found in {path}')
        return
    content = content[:style_close] + FOOTER_CSS + FOOTER_RESPONSIVE + '\n  ' + content[style_close:]

    # Inject footer HTML before </body>
    body_close = content.rfind('</body>')
    if body_close == -1:
        print(f'  WARNING: </body> not found in {path}')
        return
    content = content[:body_close] + footer_html + '\n\n' + content[body_close:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  Footer injected into {path}')


# ════════════════════════════════════════════════════════════════════════════
# FIX 1 — Shipping policy: remove incorrect rates, add placeholder
# ════════════════════════════════════════════════════════════════════════════
print('Fix 1: shipping-policy.html rates...')
with open(PAGES + '/shipping-policy.html', 'r', encoding='utf-8') as f:
    sp = f.read()

OLD_RATES = """  <ul>
    <li><strong>Standard Shipping:</strong> 3–5 business days — $8.00</li>
    <li><strong>Priority Shipping:</strong> 2–3 business days — $16.00</li>
    <li><strong>Free Standard Shipping:</strong> Automatically applied to orders over $100 (pre-discount subtotal)</li>
  </ul>"""
NEW_RATES = "  <p>Shipping rates and delivery times will be displayed at checkout.</p>"

if OLD_RATES in sp:
    sp = sp.replace(OLD_RATES, NEW_RATES, 1)
    print('  Rates section replaced')
else:
    print('  WARNING: rates section not found exactly')

with open(PAGES + '/shipping-policy.html', 'w', encoding='utf-8') as f:
    f.write(sp)


# ════════════════════════════════════════════════════════════════════════════
# FIX 2 — Add footer to pages/shop.html and root shop.html
# ════════════════════════════════════════════════════════════════════════════
print('\nFix 2: inject footer into shop files...')
inject_footer_into_shop(PAGES + '/shop.html', FOOTER_HTML_SUB)
inject_footer_into_shop(ROOT  + '/shop.html', FOOTER_HTML_SUB)


# ════════════════════════════════════════════════════════════════════════════
# FIX 3 — Stretched-link card clickability in pages/shop.html
# ════════════════════════════════════════════════════════════════════════════
print('\nFix 3: stretched-link product cards in pages/shop.html...')
with open(PAGES + '/shop.html', 'r', encoding='utf-8') as f:
    shop = f.read()

# 3a. Add position:relative to .product-card
OLD_CARD_CSS = '.product-card {\n      background: #fff; border: 1px solid var(--warm-gray); border-radius: 8px;\n      padding: 20px; transition: all 0.2s; display: flex; flex-direction: column; gap: 10px;\n    }'
NEW_CARD_CSS = '.product-card {\n      background: #fff; border: 1px solid var(--warm-gray); border-radius: 8px;\n      padding: 20px; transition: all 0.2s; display: flex; flex-direction: column; gap: 10px;\n      position: relative;\n    }'
if OLD_CARD_CSS in shop:
    shop = shop.replace(OLD_CARD_CSS, NEW_CARD_CSS, 1)
    print('  Added position:relative to .product-card')
else:
    print('  WARNING: .product-card CSS not found exactly')

# 3b. Add ::after stretched-link on .product-name, keep existing rules
OLD_NAME_CSS = '.product-name { font-family: "Playfair Display", serif; font-size: 18px; font-weight: 700; color: var(--text-dark); line-height: 1.3; text-decoration: none; display: block; }\n    .product-name:hover { color: var(--red); }'
NEW_NAME_CSS = '''.product-name { font-family: "Playfair Display", serif; font-size: 18px; font-weight: 700; color: var(--text-dark); line-height: 1.3; text-decoration: none; display: block; position: relative; z-index: 1; }
    .product-name::after { content: ""; position: absolute; inset: 0; z-index: 0; }
    .product-card:hover .product-name { color: var(--red); }'''
if OLD_NAME_CSS in shop:
    shop = shop.replace(OLD_NAME_CSS, NEW_NAME_CSS, 1)
    print('  Added stretched-link ::after to .product-name')
else:
    print('  WARNING: .product-name CSS not found exactly')

# 3c. Lift variant-select and add-btn above the overlay
OLD_VARIANT_CSS = '.variant-select {\n      width: 100%;\n      padding: 8px 12px;\n      border: 1.5px solid var(--warm-gray);\n      border-radius: 4px;\n      font-size: 14px;\n      font-family: "DM Sans", sans-serif;\n      color: var(--text-dark);\n      background: var(--off-white);\n      cursor: pointer;\n      transition: border-color 0.2s;\n      appearance: none;\n      background-image: url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'12\' height=\'8\' viewBox=\'0 0 12 8\'%3E%3Cpath d=\'M1 1l5 5 5-5\' stroke=\'%23888\' stroke-width=\'1.5\' fill=\'none\' stroke-linecap=\'round\'/%3E%3C/svg%3E");\n      background-repeat: no-repeat;\n      background-position: right 12px center;\n      padding-right: 32px;\n    }'
NEW_VARIANT_CSS = '.variant-select {\n      width: 100%;\n      padding: 8px 12px;\n      border: 1.5px solid var(--warm-gray);\n      border-radius: 4px;\n      font-size: 14px;\n      font-family: "DM Sans", sans-serif;\n      color: var(--text-dark);\n      background: var(--off-white);\n      cursor: pointer;\n      transition: border-color 0.2s;\n      appearance: none;\n      background-image: url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'12\' height=\'8\' viewBox=\'0 0 12 8\'%3E%3Cpath d=\'M1 1l5 5 5-5\' stroke=\'%23888\' stroke-width=\'1.5\' fill=\'none\' stroke-linecap=\'round\'/%3E%3C/svg%3E");\n      background-repeat: no-repeat;\n      background-position: right 12px center;\n      padding-right: 32px;\n      position: relative; z-index: 1;\n    }'
if OLD_VARIANT_CSS in shop:
    shop = shop.replace(OLD_VARIANT_CSS, NEW_VARIANT_CSS, 1)
    print('  Added z-index:1 to .variant-select')
else:
    print('  WARNING: .variant-select CSS not found exactly — trying simpler patch')
    shop = shop.replace(
        'padding-right: 32px;\n    }',
        'padding-right: 32px;\n      position: relative; z-index: 1;\n    }',
        1
    )
    print('  Applied fallback patch to .variant-select')

OLD_BTN_CSS = '.add-btn {\n      background: var(--red); color: #fff; border: none; border-radius: 4px;\n      padding: 11px; font-size: 13px; font-weight: 600; cursor: pointer;\n      width: 100%; transition: background 0.2s; font-family: "DM Sans", sans-serif;\n      letter-spacing: 0.04em; margin-top: auto;\n    }'
NEW_BTN_CSS = '.add-btn {\n      background: var(--red); color: #fff; border: none; border-radius: 4px;\n      padding: 11px; font-size: 13px; font-weight: 600; cursor: pointer;\n      width: 100%; transition: background 0.2s; font-family: "DM Sans", sans-serif;\n      letter-spacing: 0.04em; margin-top: auto;\n      position: relative; z-index: 1;\n    }'
if OLD_BTN_CSS in shop:
    shop = shop.replace(OLD_BTN_CSS, NEW_BTN_CSS, 1)
    print('  Added z-index:1 to .add-btn')
else:
    print('  WARNING: .add-btn CSS not found exactly')

# 3d. Also lift .product-price and .product-class above the overlay
OLD_PRICE_CSS = '.product-price { font-size: 22px; font-weight: 700; color: var(--red); }'
NEW_PRICE_CSS = '.product-price { font-size: 22px; font-weight: 700; color: var(--red); position: relative; z-index: 1; }'
if OLD_PRICE_CSS in shop:
    shop = shop.replace(OLD_PRICE_CSS, NEW_PRICE_CSS, 1)
    print('  Added z-index:1 to .product-price')

OLD_CLASS_CSS = '.product-class { font-size: 10px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--teal); }'
NEW_CLASS_CSS = '.product-class { font-size: 10px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--teal); position: relative; z-index: 1; }'
if OLD_CLASS_CSS in shop:
    shop = shop.replace(OLD_CLASS_CSS, NEW_CLASS_CSS, 1)
    print('  Added z-index:1 to .product-class')

with open(PAGES + '/shop.html', 'w', encoding='utf-8') as f:
    f.write(shop)
print('  pages/shop.html saved')

print('\nAll fixes applied.')
