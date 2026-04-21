path = 'c:/Users/timot/ellesworld/pages/shop.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

OLD = '<div class="footer-disclaimer">All products available on this site are strictly designated for research use only. They are not intended for human or veterinary administration, and no diagnostic, therapeutic, or clinical application is implied, warranted, or permitted.</div>'

NEW = '<div class="footer-disclaimer">All products sold by Elle\'s World Research are strictly for in-vitro research and laboratory use only. These compounds are not intended for human or animal consumption, and no therapeutic, diagnostic, or clinical use is implied or permitted. You must be 21 or older to purchase. By placing an order you confirm you are a qualified researcher and agree to our Research Use Only Agreement.</div>'

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print('Footer disclaimer updated.')
else:
    print('WARNING: old disclaimer not found exactly')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
