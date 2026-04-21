import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = 'c:/Users/timot/ellesworld'

# ══════════════════════════════════════════════════════
# FIX 1: pages/shop.html — remove duplicate cart section + fix fetch path
# ══════════════════════════════════════════════════════
with open(ROOT + '/pages/shop.html', 'r', encoding='utf-8') as f:
    c = f.read()

original = c

# Remove duplicate: from second <div class="page-header"> (22380) to just before <div class="modal-overlay"
# The first page-header is earlier; the second one at 22380 is the dupe
second_ph = c.find('<div class="page-header">\n  <h1>Product Catalog</h1>', 20000)
modal_start = c.find('<div class="modal-overlay"')
print(f'Removing duplicate from {second_ph} to {modal_start}')
c = c[:second_ph] + c[modal_start:]

# Fix fetch path
c = c.replace('fetch("../products.json")', 'fetch("/products.json")')
c = c.replace("fetch('../products.json')", "fetch('/products.json')")

with open(ROOT + '/pages/shop.html', 'w', encoding='utf-8') as f:
    f.write(c)
print(f'pages/shop.html: removed {len(original)-len(c)} chars, fixed fetch path')

# ══════════════════════════════════════════════════════
# FIX 2: pages/product.html — add research checkbox + fix fetch path
# ══════════════════════════════════════════════════════
with open(ROOT + '/pages/product.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix fetch path
c = c.replace('fetch("../products.json")', 'fetch("/products.json")')
c = c.replace("fetch('../products.json')", "fetch('/products.json')")

# Add research agreement checkbox if missing
if 'researchAgreementCheck' not in c:
    CHECKBOX_HTML = '''<div style="margin-bottom:14px;">
      <label style="display:flex;align-items:flex-start;gap:10px;font-size:13px;color:#1A1A1A;cursor:pointer;line-height:1.5;">
        <input type="checkbox" id="researchAgreementCheck" style="margin-top:3px;flex-shrink:0;width:16px;height:16px;cursor:pointer;" />
        I confirm that I am 21 or older and that all products are being purchased strictly for research purposes only. I understand these products are not intended for human or veterinary use.
      </label>
      <div id="researchAgreementError" style="display:none;color:#C0392B;font-size:12px;margin-top:6px;font-weight:600;">
        You must agree to the research use terms before placing an order.
      </div>
    </div>'''

    # Find submit button in checkout modal Step 2
    submit_idx = c.find('<button type="submit"')
    if submit_idx != -1:
        c = c[:submit_idx] + CHECKBOX_HTML + '\n    ' + c[submit_idx:]
        print('pages/product.html: added research checkbox')
    else:
        print('WARN: pages/product.html: could not find submit button')

    # Add validation to submit handler
    submit_handler = "document.getElementById('checkoutForm').addEventListener('submit'"
    handler_idx = c.find(submit_handler)
    if handler_idx != -1:
        # Find the opening of the function body
        body_open = c.find('{', handler_idx) + 1
        validation_js = """
    const agreeBox = document.getElementById('researchAgreementCheck');
    const agreeErr = document.getElementById('researchAgreementError');
    if (agreeBox && !agreeBox.checked) {
      agreeErr.style.display = 'block';
      agreeBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }
    if (agreeErr) agreeErr.style.display = 'none';
"""
        c = c[:body_open] + validation_js + c[body_open:]
        print('pages/product.html: added checkbox validation')
    else:
        print('WARN: pages/product.html: could not find submit handler')

with open(ROOT + '/pages/product.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('pages/product.html: saved')

# ══════════════════════════════════════════════════════
# FIX 3: shop.html — fix broken links, add localStorage cart, add research checkbox
# ══════════════════════════════════════════════════════
with open(ROOT + '/shop.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix broken relative links (shop.html is at root, pages are in /pages/)
link_fixes = [
    ('href="../index.html"', 'href="/index.html"'),
    ('href="about.html"', 'href="/pages/about.html"'),
    ('href="contact.html"', 'href="/pages/contact.html"'),
    ('href="agreement.html"', 'href="/pages/research-agreement.html"'),
    ('href="faq.html"', 'href="/pages/faq.html"'),
    ('href="shipping-info.html"', 'href="/pages/shipping-info.html"'),
    ('href="privacy-policy.html"', 'href="/pages/privacy-policy.html"'),
    ('href="shipping-policy.html"', 'href="/pages/shipping-policy.html"'),
    ('href="terms-of-service.html"', 'href="/pages/terms-of-service.html"'),
    ('href="return-policy.html"', 'href="/pages/return-policy.html"'),
    ('href="shop.html"', 'href="/pages/shop.html"'),
]
for old, new in link_fixes:
    if old in c:
        c = c.replace(old, new)
        print(f'shop.html: {old} -> {new}')

# Add localStorage for ew_cart if missing (shop.html may use its own storage var)
# Check what storage variables it uses
if "localStorage.setItem('ew_cart'" not in c and "localStorage.getItem('ew_cart'" not in c:
    # Replace any sessionStorage ew_cart references
    if "sessionStorage.setItem('ew_cart'" in c or "sessionStorage.getItem('ew_cart'" in c:
        c = c.replace("sessionStorage.setItem('ew_cart'", "localStorage.setItem('ew_cart'")
        c = c.replace("sessionStorage.getItem('ew_cart'", "localStorage.getItem('ew_cart'")
        print('shop.html: converted sessionStorage -> localStorage')
    else:
        print('WARN: shop.html: no ew_cart storage found at all - may use different variable name')

# Add research agreement checkbox
if 'researchAgreementCheck' not in c and 'id="modalOverlay"' in c:
    CHECKBOX_HTML = '''<div style="margin-bottom:14px;">
      <label style="display:flex;align-items:flex-start;gap:10px;font-size:13px;color:#1A1A1A;cursor:pointer;line-height:1.5;">
        <input type="checkbox" id="researchAgreementCheck" style="margin-top:3px;flex-shrink:0;width:16px;height:16px;cursor:pointer;" />
        I confirm that I am 21 or older and that all products are being purchased strictly for research purposes only. I understand these products are not intended for human or veterinary use.
      </label>
      <div id="researchAgreementError" style="display:none;color:#C0392B;font-size:12px;margin-top:6px;font-weight:600;">
        You must agree to the research use terms before placing an order.
      </div>
    </div>'''

    submit_idx = c.find('<button type="submit"')
    if submit_idx != -1:
        c = c[:submit_idx] + CHECKBOX_HTML + '\n    ' + c[submit_idx:]
        print('shop.html: added research checkbox')

    submit_handler = "addEventListener('submit'"
    handler_idx = c.find(submit_handler)
    if handler_idx != -1:
        body_open = c.find('{', handler_idx) + 1
        validation_js = """
    const agreeBox = document.getElementById('researchAgreementCheck');
    const agreeErr = document.getElementById('researchAgreementError');
    if (agreeBox && !agreeBox.checked) {
      agreeErr.style.display = 'block';
      agreeBox.scrollIntoView({ behavior: '
