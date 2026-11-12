"""Wydanie nowej wersji na GitHubie – po nim w WordPressie parafii pojawia się „Aktualizuj”.
Użycie:  python narzedzia/wydanie.py 1.2.0 "Co się zmieniło (pokaże się w kokpicie WordPressa)"
Kroki: numer wersji w wp_build.py → make_page.py → wp_build.py → commit + tag v1.2.0 → push →
wydanie z plikami parafia.zip, brenna.zip, parafia-dokumenty.zip, wersje.json.
Wymaga: zalogowanego gh (gh auth login) i czystego drzewa gita (wszystkie zmiany zapisane).
Python ze Sklepu Microsoft nie widzi logowania gh – wtedy uruchom z Git Basha tak:
  GH_TOKEN=$(gh auth token) python narzedzia/wydanie.py 1.2.0 "opis zmian\""""
import re, sys, shutil, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding='utf-8', errors='replace')   # konsola Windows (cp1250) nie zna „→”
if len(sys.argv) < 3 or not re.fullmatch(r'\d+\.\d+\.\d+', sys.argv[1]):
    sys.exit(__doc__)
ver, notes = sys.argv[1], sys.argv[2]
GH = shutil.which('gh') or r'C:\Program Files\GitHub CLI\gh.exe'
run = lambda *a, cwd=ROOT: subprocess.run(a, cwd=cwd, check=True)
out = lambda *a: subprocess.run(a, cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()

if out('git', 'status', '--porcelain'):
    sys.exit('Najpierw zapisz zmiany (git commit) – wydanie robi się z czystego drzewa.')
if out('git', 'tag', '-l', 'v' + ver):
    sys.exit(f'Wersja {ver} już była. Podaj wyższą.')
if subprocess.run([GH, 'auth', 'status'], capture_output=True).returncode != 0:
    sys.exit('gh nie widzi logowania do GitHuba. Uruchom z Git Basha:\n  GH_TOKEN=$(gh auth token) python narzedzia/wydanie.py ' + ver + ' "…"')

wb = ROOT / 'narzedzia' / 'wp_build.py'
wb.write_text(re.sub(r"^VERSION = '[^']+'", f"VERSION = '{ver}'", wb.read_text(encoding='utf-8'), count=1, flags=re.M), encoding='utf-8')
run(sys.executable, 'make_page.py', cwd=ROOT / 'src')
run(sys.executable, str(wb))
# wersje.json: dla WordPressa także numer, opis i data wydania (wtyczka nie pyta api.github.com – limit na wspólnym hostingu)
import json, datetime
wj = ROOT / 'dist' / 'wersje.json'
w = json.loads(wj.read_text(encoding='utf-8'))
w.update({'tag': 'v' + ver, 'notes': notes, 'date': datetime.date.today().isoformat()})
wj.write_text(json.dumps(w, ensure_ascii=False), encoding='utf-8')
run('git', 'add', '-A')
run('git', 'commit', '-q', '-m', f'Wydanie {ver}\n\n{notes}')
run('git', 'tag', '-a', 'v' + ver, '-m', f'Wersja {ver}')
run('git', 'push', '-q', 'origin', 'HEAD', '--follow-tags')
d = ROOT / 'dist'
run(GH, 'release', 'create', 'v' + ver, str(d / 'parafia.zip'), str(d / 'brenna.zip'), str(d / 'parafia-dokumenty.zip'),
    str(d / 'wersje.json'), '--title', f'Wersja {ver}', '--notes', notes)
print(f'\nGotowe: wersja {ver} na GitHubie. W WordPressie: Kokpit → Aktualizacje → „Sprawdź ponownie” → Aktualizuj.')
