"""Zrzuty całej strony w trzech szerokościach (1440, 768, 390) + kontrola przewijania w bok.
Użycie:  python3 narzedzia/zrzuty.py [plik.html]   (domyślnie src/brenna-strona.html)
Wynik:   zrzuty/strona-<szerokosc>.png"""
import sys, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
page = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'src' / 'brenna-strona.html'
out = ROOT / 'zrzuty'; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 768, 390):
        pg = b.new_page(viewport={'width': w, 'height': 900})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(page.resolve().as_uri()); pg.wait_for_timeout(4000)
        # działy mają content-visibility:auto – do zrzutu wymuszamy rysowanie wszystkiego
        pg.add_style_tag(content='html{scroll-behavior:auto!important}*{content-visibility:visible!important}')
        pg.wait_for_timeout(300)
        f = out / f'strona-{w}.png'; pg.screenshot(path=str(f), full_page=True)
        sw = pg.evaluate('document.documentElement.scrollWidth')
        print(f'{w}px: {f.name}  przewijanie w bok: {"TAK (" + str(sw) + "px)" if sw > w else "nie"}  błędy JS: {errs or "brak"}')
    b.close()
