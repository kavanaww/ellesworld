import sys, io, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = 'c:/Users/timot/ellesworld'
files = sorted(glob.glob(ROOT + '/**/*.html', recursive=True))

PRODUCT_MOBILE_CSS = """
    @media (max-width: 768px) {
      .breadcrumb { padding: 12px 20px; }
      .product-main { grid-template-columns: 1fr !important; padding: 24px 20px; gap: 24px; }
      .product-info h1 { font-size: 24px; }
      .product-info .price { font-size: 28px; }
      .product-form { padding: 20px; }
      .research-links { padding: 20px; }
    }
    @media (max-width: 480px) {
      .product-info h1 { font-size: 20px; }
    }"""

INDEX_480_CSS = """
    @media (max-width: 480px) {
      .footer-inner { grid-template-columns: 1fr; padding: 32px 20px; gap: 24px; }
      .footer-disclaimer { padding: 14px 20px; font-size: 11px; }
      .footer-bottom { flex-direction: column; gap: 8px; padding: 14px 20px; font-size: 11px; }
    }"""

fixed = 0
for path in files:
    fname = path.replace(ROOT, '').lstrip('/').lstrip('\\')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    original = c

    # 1. Add overflow-x: hidden to html and body
    has_overflow = 'overflow-x: hidden' in c or 'overflow-x:hidden' in c
    if not has_overflow:
        # Add to body rule
        body_m = re.search(r'(body\s*\{)([^}]*)(})', c)
        if body_m and 'overflow-x' not in body_m.group(0):
            c = c[:body_m.start(2)] + body_m.group(2) + ' overflow-x: hidden;' + c[body_m.start(3):]
            print(fname + ': added overflow-x to body')
        # Add html { overflow-x: hidden } just after <style>
        style_idx = c.find('<style>')
        if style_idx != -1:
            after = c.find('\n', style_idx) + 1
            c = c[:after] + '    html { overflow-x: hidden; }\n' + c[after:]
            print(fname + ': added html overflow-x:hidden')

    # 2. Add img max-width:100% if not present
    if 'max-width: 100%' not in c and 'max-width:100%' not in c:
        style_idx = c.find('<style>')
        if style_idx != -1:
            after = c.find('\n', style_idx) + 1
            c = c[:after] + '    img, video, iframe { max-width: 100%; height: auto; }\n' + c[after:]
            print(fname + ': added img max-width:100%')

    # 3. Add box-sizing if missing
    if 'box-sizing: border-box' not in c and 'box-sizing:border-box' not in c:
        style_idx = c.find('<style>')
        if style_idx != -1:
            after = c.find('\n', style_idx) + 1
            c = c[:after] + '    *, *::before, *::after { box-sizing: border-box; }\n' + c[after:]
            print(fname + ': added box-sizing:border-box')

    # 4. Ensure cart-drawer has max-width:100vw in CSS
    if 'cart-drawer' in c and 'max-width: 100vw' not in c and 'max-width:100vw' not in c:
        # Add max-width to the cart-drawer CSS rule
        c = c.replace(
            '.cart-drawer {',
            '.cart-drawer { max-width: 100vw;'
        )
        if '.cart-drawer { max-width: 100vw;' in c:
            print(fname + ': added max-width:100vw to cart-drawer')

    # 5. Modal: ensure it can't overflow viewport width
    if 'modal-overlay' in c:
        # If modal doesn't have max-width:100% or similar protection
        if '.modal {' in c and 'width: 94%' not in c and 'width: 90%' not in c:
            # Add box-sizing to modal in 768px block - find last occurrence of .modal
            c = c.replace(
                '.modal { padding: 24px; }',
                '.modal { padding: 24px; max-width: 100%; box-sizing: border-box; }'
            )

    # 6. Page-specific
    is_product = fname.replace('\\', '/').endswith('pages/product.html')
    if is_product:
        if 'breadcrumb { padding: 12px' not in c and 'product-main { grid-template-columns: 1fr' not in c:
            style_close = c.rfind('</style>')
            if style_close != -1:
                c = c[:style_close] + PRODUCT_MOBILE_CSS + '\n  ' + c[style_close:]
                print(fname + ': added product mobile rules')

    is_index = fname.replace('\\', '/') == 'index.html'
    if is_index:
        if 'footer-inner { grid-template-columns: 1fr; padding: 32px 20px' not in c:
            style_close = c.rfind('</style>')
            if style_close != -1:
                c = c[:style_close] + INDEX_480_CSS + '\n  ' + c[style_close:]
                print(fname + ': added 480px footer rules')

    if c != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        fixed += 1

print('\nDone. Fixed ' + str(fixed) + ' files.')
