"""Sceny świąteczne w nagłówku: renderuje wybrane daty roku liturgicznego.
Użycie:  python3 narzedzia/sceny.py [nazwa ...]   np. sceny.py zielone reformacja
Wynik:   zrzuty/scena-<nazwa>.png (prawa część nagłówka, 2x)"""
import sys, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'src' / 'naglowek-kompakt.html'
DATES = [('2026-12-06','adwent2',12),('2026-12-24','wigilia',12),('2026-12-30','boze30',12),('2027-01-06','epifania',12),
 ('2027-03-21','palmowa',12),('2027-03-25','wczwartek',12),('2027-03-26','wpiatek',12),('2027-03-27','wsobota',12),
 ('2027-03-28','wielkanoc',20),('2027-05-06','wniebo',12),('2027-05-16','zielone',22),('2026-09-27','zniwa',12),
 ('2026-10-31','reformacja',27),('2026-11-01','zmarli',12),('2026-11-22','wiecznosc',12)]
only = sys.argv[1:]
out = ROOT / 'zrzuty'; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(PAGE.resolve().as_uri()); pg.wait_for_timeout(1500)
    for d, n, t in DATES:
        if only and n not in only: continue
        # seek() przewija zegar animacji; FX.t0 = chwila startu sceny
        pg.evaluate(f"SIMDATE='{d}';applyDate(today());seek(FX.t0+{t},true)"); pg.wait_for_timeout(300)
        nm = pg.evaluate("document.getElementById('fname')?.value")
        pg.screenshot(path=str(out / f'scena-{n}.png'), clip={'x': 900, 'y': 0, 'width': 540, 'height': 330})
        print(n, d, '→', nm)
    print('błędy JS:', errs or 'brak'); b.close()
