import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = 'c:/Users/timot/ellesworld/pages/shop.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Insert checkbox HTML above the submit button ───────────────────────────
OLD_SUBMIT = '        <button type="submit" class="checkout-btn" style="margin-bottom:10px;">Submit Order \U0001f4e6</button>'
NEW_SUBMIT = """        <div style="margin-bottom:14px;">
          <label style="display:flex;align-items:flex-start;gap:10px;font-size:13px;color:#1A1A1A;cursor:pointer;line-height:1.5;">
            <input type="checkbox" id="researchAgreementCheck" style="margin-top:3px;flex-shrink:0;width:16px;height:16px;cursor:pointer;" />
            I confirm that I am 21 or older and that all products are being purchased strictly for research purposes only. I understand these products are not intended for human or veterinary use.
          </label>
          <div id="researchAgreementError" style="display:none;color:#C0392B;font-size:12px;margin-top:6px;font-weight:600;">
            You must agree to the research use terms before placing an order.
          </div>
        </div>
        <button type="submit" class="checkout-btn" style="margin-bottom:10px;">Submit Order \U0001f4e6</button>"""

if OLD_SUBMIT in content:
    content = content.replace(OLD_SUBMIT, NEW_SUBMIT, 1)
    print('Checkbox HTML inserted.')
else:
    print('WARNING: submit button not found exactly — trying fallback')
    # Try without emoji
    alt = '        <button type="submit" class="checkout-btn" style="margin-bottom:10px;">Submit Order'
    idx = content.find(alt)
    if idx != -1:
        line_end = content.find('</button>', idx) + len('</button>')
        old_btn = content[idx:line_end]
        content = content[:idx] + NEW_SUBMIT + content[line_end:]
        print('Checkbox HTML inserted (fallback).')
    else:
        print('ERROR: could not find submit button')

# ── 2. Add checkbox validation at top of submit handler ──────────────────────
OLD_HANDLER = 'addEventListener("submit", function(e) {\n      e.preventDefault();'
NEW_HANDLER = '''addEventListener("submit", function(e) {
      e.preventDefault();
      const agreeBox = document.getElementById('researchAgreementCheck');
      const agreeErr = document.getElementById('researchAgreementError');
      if (agreeBox && !agreeBox.checked) {
        agreeErr.style.display = 'block';
        agreeBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }
      if (agreeErr) agreeErr.style.display = 'none';'''

if OLD_HANDLER in content:
    content = content.replace(OLD_HANDLER, NEW_HANDLER, 1)
    print('Validation logic added to submit handler.')
else:
    print('WARNING: submit handler not found exactly')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
