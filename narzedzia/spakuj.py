"""Pakuje stronę do jednego pliku do pokazania (mail, pendrive): czcionki i zdjęcia w środku.
Użycie:  python narzedzia/spakuj.py        (najpierw: cd src && python make_page.py)
Wynik:   pokaz/brenna-strona-pokaz.html
Bez internetu nie działają tylko spacer 360° i mapa Google (to ramki z innych stron)."""
import re, base64, tarfile, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / 'src' / 'brenna-strona.html', ROOT / 'pokaz' / 'brenna-strona-pokaz.html'
MAX_KB, WIDTH = 250, 900          # większe zdjęcia zmniejszane do tej szerokości (JPEG)

def b64(data, mime): return f'data:{mime};base64,' + base64.b64encode(data).decode()

# ---- czcionki z paczek fontsource (src/font): tylko latin + latin-ext (polskie litery) ----
def fonts():
    css = []
    for pkg, files in (('fontsource-pt-sans-5.3.0.tgz', ('400.css', '700.css')), ('fontsource-pt-sans-narrow-5.3.0.tgz', ('700.css',))):
        with tarfile.open(ROOT / 'src' / 'font' / pkg) as t:
            for f in files:
                for block in re.findall(r'@font-face\s*{[^}]*}', t.extractfile('package/' + f).read().decode()):
                    m = re.search(r"url\(\./files/([^)]+?-(?:latin|latin-ext)-\d+-normal\.woff2)\)", block)
                    if not m: continue
                    data = t.extractfile('package/files/' + m.group(1)).read()
                    css.append(re.sub(r'src:[^;]+;', f"src: url({b64(data, 'font/woff2')}) format('woff2');", block))
    return '<style>\n' + '\n'.join(css) + '\n</style>'

# ---- zdjęcia: pobrane i wklejone; duże zmniejszone przez Chrome (bez dodatkowych bibliotek) ----
def shrink(data, mime):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': WIDTH, 'height': 800})
        pg.set_content(f'<body style="margin:0"><img id="i" src="{b64(data, mime)}" style="display:block;width:{WIDTH}px"></body>')
        pg.wait_for_function('document.getElementById("i").complete')
        out = pg.query_selector('#i').screenshot(type='jpeg', quality=82); b.close()
    return out, 'image/jpeg'

def images(h):
    cache = {}
    def repl(m):
        url = m.group(1)
        if url not in cache:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                data = urllib.request.urlopen(req, timeout=30).read()
                ext = url.split('?')[0].rsplit('.', 1)[-1].lower()
                mime = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}[ext]
                if len(data) > MAX_KB * 1024: data, mime = shrink(data, mime)
                cache[url] = b64(data, mime); print(f'  {len(data)//1024:>4} KB  {url.split("/")[-1][:60]}')
            except Exception as e:
                cache[url] = url; print('  NIE POBRANO', url, e)
        return f'src="{cache[url]}"'
    return re.sub(r'src="(https?://[^"]+\.(?:jpe?g|png|webp)(?:\?[^"]*)?)"', repl, h)

h = SRC.read_text(encoding='utf-8')
h, n = re.subn(r'<link rel="preconnect"[^>]*>\s*<link rel="preconnect"[^>]*>\s*<link href="https://fonts\.googleapis\.com[^>]*>', fonts(), h, count=1)
assert n == 1, 'nie znaleziono linku do Google Fonts'
h = images(h)
OUT.parent.mkdir(exist_ok=True); OUT.write_text(h, encoding='utf-8')
print(f'ok  {OUT.relative_to(ROOT)}  {OUT.stat().st_size // 1024} KB')
