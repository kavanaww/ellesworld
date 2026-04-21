import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = 'c:/Users/timot/ellesworld'

for fname in ['index.html', 'pages/faq.html']:
    path = ROOT + '/' + fname
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    print(f'\n{"="*55}')
    print(f'{fname} ({len(c)} chars)')
    print(f'{"="*55}')

    checks = {
        'cartCount in nav':    'id="cartCount"' in c,
        'cart-btn CSS':        '.cart-btn {' in c,
        'cart-overlay HTML':   'id="cartOverlay"' in c,
        'cart-drawer HTML':    'id="cartDrawer"' in c,
        'modal-overlay HTML':  'id="modalOverlay"' in c,
        'localStorage cart':   "localStorage.setItem('ew_cart'" in c,
        'sessionStorage cart': "sessionStorage.setItem('ew_cart'" in c,
        '/products.json':      'fetch("/products.json")' in c,
        '../products.json':    'fetch("../products.json")' in c,
        'renderShop guard':    'getElementById("shopMain")) renderShop' in c,
    }
    for k, v in checks.items():
        print(f'  {"OK" if v else "FAIL"} {k}')

    # Show nav section
    nav_idx = c.find('<nav')
    nav_end = c.find('</nav>', nav_idx) + len('</nav>')
    print('\n  Nav:')
    print(c[nav_idx:nav_end].encode('ascii', errors='replace').decode())
