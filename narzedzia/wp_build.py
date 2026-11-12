"""Składa motyw WordPressa „Brenna-Górki” z gotowej strony prototypu i pakuje motyw + wtyczkę do ZIP-ów.
Użycie:  python narzedzia/wp_build.py        (najpierw: cd src && python make_page.py)
Wynik:   dist/brenna/ (motyw), dist/brenna.zip, dist/parafia.zip, dist/parafia-dokumenty.zip (pliki PDF z src/dokumenty –
         osobna wtyczka wgrywana raz, żeby motyw był lekki przy aktualizacjach)
Motyw to ta sama strona co src/brenna-strona.html; WordPress wstawia w niej tylko swoje znaczniki
(wp_head, wp_footer) i dane wtyczki „Parafia” (zapisane teksty, nabożeństwa, aktualności, prawo edycji)."""
import re, shutil, tarfile, zipfile, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'src' / 'brenna-strona.html'
DIST = ROOT / 'dist'; THEME = DIST / 'brenna'; PLUGIN = ROOT / 'wordpress' / 'parafia'
VERSION = '1.3.0'        # motyw + wtyczka „Parafia” (zmienia narzedzia/wydanie.py)
DOCS_VERSION = '1.0.0'   # PDF-y – podnoś tylko, gdy zmienią się pliki w src/dokumenty (wtedy WordPress pobierze 8 MB)

STYLE = f"""/*
Theme Name: Brenna-Górki
Description: Strona Parafii Ewangelicko-Augsburskiej Brenna-Górki: animowany nagłówek, nabożeństwa, aktualności, spacer 360°. Edycja treści na stronie przez wtyczkę „Parafia Brenna-Górki”.
Author: Jarosław Sajdok
Version: {VERSION}
Requires at least: 6.4
Requires PHP: 7.4
Text Domain: brenna
*/
"""
FUNCTIONS = """<?php
// Motyw jednostronicowy: cała strona jest w page.html (składana z prototypu narzędziem wp_build.py).
if (!defined('ABSPATH')) exit;
add_filter('show_admin_bar', '__return_false');            // pasek WordPressa zasłaniałby przyklejone menu
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');
add_action('wp_enqueue_scripts', function () {             // style bloków Gutenberga nie są tu potrzebne
	foreach (['wp-block-library', 'wp-block-library-theme', 'classic-theme-styles', 'global-styles'] as $h) wp_dequeue_style($h);
}, 100);
"""
INDEX = """<?php
// Każdy adres pokazuje stronę parafii (jedna strona z działami i podstroną #dokumenty).
if (!defined('ABSPATH')) exit;
$html = file_get_contents(__DIR__ . '/page.html');
$grab = function ($fn) { ob_start(); $fn(); return ob_get_clean(); };
$html = str_replace('{{THEME}}', esc_url(get_template_directory_uri()), $html);
$html = str_replace('{{DOCS}}', esc_url(content_url('plugins/parafia-dokumenty/dokumenty')), $html);   // pliki z wtyczki „Parafia – dokumenty”
$html = str_replace('<!--WP_HEAD-->', $grab('wp_head'), $html);
$html = str_replace('<!--PARAFIA_BOOT-->', function_exists('parafia_boot') ? $grab('parafia_boot') : '', $html);
$html = str_replace('<!--WP_FOOTER-->', $grab('wp_footer'), $html);
echo $html;
"""

def fonts():
    """czcionki z src/font (latin + latin-ext) jako pliki motywu, @font-face zamiast Google Fonts"""
    (THEME / 'fonts').mkdir(parents=True, exist_ok=True); css = []
    for pkg, files in (('fontsource-pt-sans-5.3.0.tgz', ('400.css', '700.css')), ('fontsource-pt-sans-narrow-5.3.0.tgz', ('700.css',))):
        with tarfile.open(ROOT / 'src' / 'font' / pkg) as t:
            for f in files:
                for block in re.findall(r'@font-face\s*{[^}]*}', t.extractfile('package/' + f).read().decode()):
                    m = re.search(r"url\(\./files/([^)]+?-(?:latin|latin-ext)-\d+-normal\.woff2)\)", block)
                    if not m: continue
                    (THEME / 'fonts' / m.group(1)).write_bytes(t.extractfile('package/files/' + m.group(1)).read())
                    css.append(re.sub(r'src:[^;]+;', f"src: url({{{{THEME}}}}/fonts/{m.group(1)}) format('woff2');", block))
    return '<style>\n' + '\n'.join(css) + '\n</style>'

if THEME.exists(): shutil.rmtree(THEME)
THEME.mkdir(parents=True)
h = SRC.read_text(encoding='utf-8')
h, n = re.subn(r'<link rel="preconnect"[^>]*>\s*<link rel="preconnect"[^>]*>\s*<link href="https://fonts\.googleapis\.com[^>]*>', fonts(), h, count=1)
assert n == 1, 'nie znaleziono linku do Google Fonts'
assert h.count('<script>') == 1, 'oczekiwany jeden główny skrypt'
h = h.replace('</head>', '<!--WP_HEAD-->\n</head>', 1)
h = h.replace('<script>', '<!--PARAFIA_BOOT-->\n<script>', 1)
i = h.rfind('</body>'); h = h[:i] + '<!--WP_FOOTER-->\n' + h[i:]
h = h.replace('href="dokumenty/', 'href="{{DOCS}}/')
(THEME / 'page.html').write_text(h, encoding='utf-8')
(THEME / 'style.css').write_text(STYLE, encoding='utf-8')
(THEME / 'functions.php').write_text(FUNCTIONS, encoding='utf-8')
(THEME / 'index.php').write_text(INDEX, encoding='utf-8')
shutil.copytree(ROOT / 'src' / 'vendor', THEME / 'vendor')   # PDF.js do podglądu dokumentów (ładowany dopiero przy otwarciu PDF-a)
shot = ROOT / 'zrzuty' / 'motyw.png'
if shot.exists(): shutil.copy(shot, THEME / 'screenshot.png')

def zipdir(folder, out):
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in sorted(folder.rglob('*')):
            if f.is_file(): z.write(f, f'{folder.name}/{f.relative_to(folder).as_posix()}')
    print(f'ok  {out.relative_to(ROOT)}  {out.stat().st_size // 1024} KB')
zipdir(THEME, DIST / 'brenna.zip')
# wersja wtyczki z jednego miejsca (VERSION) – nagłówek parafia.php poprawiany przy każdym budowaniu
pp = PLUGIN / 'parafia.php'
pp.write_text(re.sub(r'(\* Version: )\S+', r'\g<1>' + VERSION, pp.read_text(encoding='utf-8'), count=1), encoding='utf-8')
zipdir(PLUGIN, DIST / 'parafia.zip')

# pliki dokumentów (standardy ochrony małoletnich itd.) jako osobna wtyczka
DOCS = DIST / 'parafia-dokumenty'
if DOCS.exists(): shutil.rmtree(DOCS)
shutil.copytree(ROOT / 'src' / 'dokumenty', DOCS / 'dokumenty')
(DOCS / 'parafia-dokumenty.php').write_text("""<?php
/**
 * Plugin Name: Parafia Brenna-Górki – dokumenty
 * Description: Pliki PDF do podstrony Dokumenty (standardy ochrony małoletnich z załącznikami). Wystarczy, że jest wgrana – włączać nie trzeba.
 * Version: """ + DOCS_VERSION + """
 * Author: Jarosław Sajdok
 */
if (!defined('ABSPATH')) exit;
""", encoding='utf-8')
zipdir(DOCS, DIST / 'parafia-dokumenty.zip')

# wersje części – plik w każdym wydaniu na GitHubie; z niego WordPress wie, co jest do aktualizacji
import json
(DIST / 'wersje.json').write_text(json.dumps({'parafia': VERSION, 'brenna': VERSION, 'parafia-dokumenty': DOCS_VERSION}), encoding='utf-8')
print(f'ok  dist/wersje.json  motyw i wtyczka {VERSION}, dokumenty {DOCS_VERSION}')
