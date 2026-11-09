"""Test ścieżki proboszcza na lokalnym WordPressie (Playground na :9400, blueprint.json z tego folderu).
gość → stara strona; stały link → nowa; logowanie redaktora; edycja tekstu, nabożeństw, wpisu, dokumentu; odświeżenie → zapisane."""
import json, re, sys, pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).parent; OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE
B = 'http://127.0.0.1:9400'
bp = json.loads((HERE / 'blueprint.json').read_text(encoding='utf-8'))
php = bp['steps'][-1]['code']
USER = re.search(r"'user_login'=>'([^']+)'", php).group(1); PASS = re.search(r"'user_pass'=>'([^']+)'", php).group(1)
TOKEN = re.search(r"update_option\('parafia_token','([^']+)'", php).group(1)
ok = lambda c, m: print(('OK   ' if c else 'BŁĄD ') + m)

with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    # 1. gość
    g = b.new_page(); g.goto(B + '/'); ok(not g.query_selector('.rose'), 'gość widzi starą stronę'); g.close()
    # 2. stały link
    c = b.new_context(viewport={'width': 1440, 'height': 900}); pg = c.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(B + '/?nowa=' + TOKEN); pg.wait_for_timeout(2500)
    ok(bool(pg.query_selector('.rose')) and '?nowa' not in pg.url, 'stały link pokazuje nową stronę i znika z adresu')
    ok(pg.evaluate('!!window.PARAFIA && !window.PARAFIA.canEdit'), 'dane wtyczki są, bez prawa edycji')
    ok(pg.evaluate("document.querySelectorAll('#aktualnosci article.post').length") >= 3, 'aktualności z wpisów WordPressa')
    ok(pg.evaluate("document.fonts.check('bold 30px \"PT Sans Narrow\"')"), 'czcionki z serwera motywu')
    # 3. logowanie
    pg.goto(B + '/#edycja'); pg.wait_for_timeout(1500)
    pg.fill('dialog.login [name=u]', USER); pg.fill('dialog.login [name=p]', PASS); pg.click('dialog.login .go')
    pg.wait_for_timeout(4000)
    ok(pg.evaluate("window.PARAFIA.canEdit && document.body.classList.contains('editing')"), 'po zalogowaniu od razu tryb edycji')
    # 4a. tekst
    lead = pg.query_selector('[data-key="tekst-1"]'); lead.click(); pg.keyboard.press('End'); pg.keyboard.type(' Zapraszamy!')
    pg.wait_for_timeout(3500); ok('Zapisano' in pg.inner_text('.editbar'), 'tekst zapisany automatycznie')
    # 4b. nabożeństwa: dodaj wiersz
    n0 = pg.evaluate("document.querySelector('[data-key=nabozenstwa]').tBodies[0].rows.length")
    pg.click('.addrow'); pg.keyboard.type('Niedziela testowa'); pg.keyboard.press('Enter'); pg.wait_for_timeout(3500)
    # 4c. wpis przez okno edytora
    pg.click('.addpost'); pg.wait_for_timeout(600)
    pg.fill('.ped-title input, .ped input[name=t], .ped-title', 'Wpis z testu') if pg.query_selector('.ped-title input') else None
    pg.keyboard.press('Escape')
    # 4d. dokument
    pg.goto(B + '/#dokumenty'); pg.wait_for_timeout(1500); pg.evaluate("document.body.classList.add('editing')")
    pg.set_input_files('#dokumenty .docs-g:nth-child(2) input[type=file]', files=[{'name': 'Klauzula_RODO.pdf', 'mimeType': 'application/pdf', 'buffer': b'%PDF-1.4\n%test\n' * 200}])
    pg.wait_for_timeout(5000)
    href = pg.evaluate("[...document.querySelectorAll('#dokumenty a.doc-n')].map(a=>a.href).find(h=>/Klauzula/i.test(h))||''")
    ok(href.startswith(B + '/wp-content/uploads/'), 'dokument w bibliotece mediów: ' + href[-40:])
    pg.screenshot(path=str(OUT / 'wp-docs.png'), full_page=True)
    # 5. odświeżenie – czy zostało
    pg.goto(B + '/'); pg.wait_for_timeout(2500)
    ok('Zapraszamy!' in pg.inner_text('[data-key="tekst-1"]'), 'tekst po odświeżeniu')
    ok(pg.evaluate("document.querySelector('[data-key=nabozenstwa]').tBodies[0].rows.length") == n0 + 1, 'nowy wiersz nabożeństw po odświeżeniu')
    ok(pg.evaluate("[...document.querySelectorAll('[data-key=nabozenstwa] td')].some(t=>/Niedziela testowa/.test(t.textContent))"), 'nazwa w wierszu po odświeżeniu')
    pg.goto(B + '/#dokumenty'); pg.wait_for_timeout(1500)
    ok(pg.evaluate("[...document.querySelectorAll('#dokumenty a.doc-n')].some(a=>/uploads/.test(a.href))"), 'dokument na liście po odświeżeniu')
    # 6. wpis przez API wtyczki (jak przy zapisie z okna edytora)
    r = pg.evaluate("PARAFIA.call('posts',{body:{title:'Wpis z testu',date:'2026-11-09',html:'<p>Test zapisu wpisu.</p>',main:null,gallery:[]}})")
    pg.goto(B + '/'); pg.wait_for_timeout(2500)
    ok(pg.evaluate("[...document.querySelectorAll('#aktualnosci article.post h3')].some(h=>h.textContent==='Wpis z testu')"), 'nowy wpis widoczny (wp=%s)' % r.get('wp'))
    pg.screenshot(path=str(OUT / 'wp-home.png'))
    # 7. wylogowanie
    pg.goto(B + '/'); pg.wait_for_timeout(1500); pg.evaluate("document.body.classList.add('editing')")
    with pg.expect_navigation(): pg.click('.editbar .out')
    pg.wait_for_load_state('load'); pg.wait_for_timeout(1000)
    ok(pg.evaluate('!window.PARAFIA || !window.PARAFIA.canEdit'), 'po wylogowaniu brak edycji')
    ok(not errs, 'brak błędów JS ' + ('' if not errs else str(errs[:3])))
    b.close()
