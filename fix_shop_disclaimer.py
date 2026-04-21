path = 'c:/Users/timot/ellesworld/pages/shop.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Verify disclaimer
idx = content.find('Must be')
print('Disclaimer:', repr(content[idx:idx+200]))
print()

# Verify footer
footer_start = content.rfind('<footer')
footer_end = content.rfind('</footer>') + len('</footer>')
print('Footer:')
print(content[footer_start:footer_end])
