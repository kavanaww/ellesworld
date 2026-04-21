import glob

ROOT = 'c:/Users/timot/ellesworld'

files = glob.glob(ROOT + '/**/*.html', recursive=True)

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    content = content.replace('/assets/logo.png" style="height:40px', '/assets/logo2.png" style="height:40px')
    content = content.replace('href="/assets/logo.png"', 'href="/assets/logo2.png"')
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Updated: {path}')
    else:
        print(f'No change: {path}')
