import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = 'c:/Users/timot/ellesworld/pages/shop.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the old duplicate block:
# It starts with the old disclaimer-bar (containing "Must be 18+")
# and ends with the closing </div> of the second filter-bar.

# 1. Find the old disclaimer-bar start (rfind before the second filter-bar)
second_fb_start = content.find('<div class="filter-bar"', 15177 + 1)  # skip first filter-bar
old_disc_start = content.rfind('<div class="disclaimer-bar"', 0, second_fb_start)

# 2. Find the end of the second filter-bar
second_fb_end = content.find('</div>', second_fb_start) + len('</div>')

# Also consume leading whitespace before old_disc_start
while old_disc_start > 0 and content[old_disc_start - 1] in ('\n', '\r', ' '):
    old_disc_start -= 1

print(f'Removing chars {old_disc_start} to {second_fb_end}')
print(f'Block to remove ({second_fb_end - old_disc_start} chars):')
print(content[old_disc_start:second_fb_end].encode('ascii', errors='replace').decode())

# Perform removal
new_content = content[:old_disc_start] + content[second_fb_end:]
print(f'\nFile: {len(content)} -> {len(new_content)} chars')

# Verify: only one filter-bar remains
count = new_content.count('<div class="filter-bar"')
print(f'filter-bar count after fix: {count}')
count_disc = new_content.count('<div class="disclaimer-bar"')
print(f'disclaimer-bar count after fix: {count_disc}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Saved.')
