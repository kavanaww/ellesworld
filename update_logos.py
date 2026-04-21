import re, os

ROOT = 'c:/Users/timot/ellesworld'

FILES = [
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

FAVICON = '<link rel="icon" type="image/png" href="/assets/logo.png">'
LOGO_IMG = '<img src="/assets/logo.png" alt="Elle\'s World Research" style="height:52px;width:auto;">'

# Footer brand variants we want to replace
FOOTER_BRAND_VARIANTS = [
    # index.html style
    "<div class=\"footer-brand-name\">Elle's <span>World</span> Research</div>",
    # pages style (same, but let's cover both quote styles)
    '<div class="footer-brand-name">Elle\'s <span>World</span> Research</div>',
]
FOOTER_BRAND_NEW = '<div class="footer-brand-name"><img src="/assets/logo.png" alt="Elle\'s World Research" style="height:52px;width:auto;"></div>'

for rel in FILES:
    path = ROOT + '/' + rel
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)
    changes = []

    # 1. Replace base64 nav img src with logo file path
    # Match src="data:image/png;base64,..." preserving other attributes
    new_content, n = re.subn(
        r'src="data:image/png;base64,[^"]*"',
        'src="/assets/logo.png"',
        content
    )
    if n:
        changes.append(f'nav img src replaced ({n}x)')
        content = new_content

    # 2. Replace footer brand name text with logo img
    replaced_footer = False
    for variant in FOOTER_BRAND_VARIANTS:
        if variant in content:
            content = content.replace(variant, FOOTER_BRAND_NEW, 1)
            replaced_footer = True
            changes.append('footer brand replaced')
            break
    if not replaced_footer:
        # Try regex fallback
        new_content, n = re.subn(
            r'<div class="footer-brand-name">.*?</div>',
            FOOTER_BRAND_NEW,
            content,
            count=1,
            flags=re.DOTALL
        )
        if n:
            content = new_content
            changes.append('footer brand replaced (regex)')
        else:
            changes.append('WARNING: footer brand not found')

    # 3. Add favicon to <head> if not already present
    if 'rel="icon"' not in content and "rel='icon'" not in content:
        # Insert after <head> or after first <meta charset>
        charset_idx = content.find('<meta charset')
        if charset_idx != -1:
            line_end = content.find('>', charset_idx) + 1
            content = content[:line_end] + '\n  ' + FAVICON + content[line_end:]
            changes.append('favicon added after charset meta')
        else:
            head_idx = content.find('<head>')
            if head_idx != -1:
                content = content[:head_idx + len('<head>')] + '\n  ' + FAVICON + content[head_idx + len('<head>'):]
                changes.append('favicon added after <head>')
            else:
                changes.append('WARNING: <head> not found')
    else:
        changes.append('favicon already present')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'{rel}: {"; ".join(changes)}  (size {original_len} -> {len(content)})')

print('\nDone.')
