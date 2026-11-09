<?php
/**
 * Aktualizacje jednym kliknięciem z wydań na GitHubie (repozytorium publiczne – bez tokenów).
 * Każde wydanie ma pliki: parafia.zip, brenna.zip, parafia-dokumenty.zip i wersje.json
 * ({"parafia":"1.2.0","brenna":"1.2.0","parafia-dokumenty":"1.0.0"}). WordPress porównuje wersje
 * z zainstalowanymi i w kokpicie pokazuje zwykły przycisk „Aktualizuj”.
 */
if (!defined('ABSPATH')) exit;

const PARAFIA_REPO = 'OWNER/brenna-strona';
const PARAFIA_PARTS = [   // nazwa w wersje.json => [rodzaj, plik wtyczki / katalog motywu, plik w wydaniu]
	'parafia'           => ['plugin', 'parafia/parafia.php', 'parafia.zip'],
	'parafia-dokumenty' => ['plugin', 'parafia-dokumenty/parafia-dokumenty.php', 'parafia-dokumenty.zip'],
	'brenna'            => ['theme', 'brenna', 'brenna.zip'],
];

// najnowsze wydanie: wersje części + adresy paczek (pamiętane 6 godzin; „Sprawdź ponownie” w kokpicie czyści)
function parafia_release() {
	$r = get_transient('parafia_release');
	if ($r !== false) return $r ?: null;
	$args = ['timeout' => 10, 'headers' => ['Accept' => 'application/vnd.github+json', 'User-Agent' => 'parafia-brenna-gorki']];
	$res = wp_remote_get('https://api.github.com/repos/' . PARAFIA_REPO . '/releases/latest', $args);
	$rel = is_wp_error($res) || wp_remote_retrieve_response_code($res) !== 200 ? null : json_decode(wp_remote_retrieve_body($res), true);
	$out = null;
	if ($rel && !empty($rel['assets'])) {
		$assets = [];
		foreach ($rel['assets'] as $a) $assets[$a['name']] = $a['browser_download_url'];
		$ver = [];
		if (!empty($assets['wersje.json'])) {
			$v = wp_remote_get($assets['wersje.json'], ['timeout' => 10, 'headers' => ['User-Agent' => 'parafia-brenna-gorki']]);
			if (!is_wp_error($v)) $ver = (array) json_decode(wp_remote_retrieve_body($v), true);
		}
		$out = ['tag' => $rel['tag_name'], 'url' => $rel['html_url'], 'notes' => (string) ($rel['body'] ?? ''), 'date' => $rel['published_at'] ?? '', 'assets' => $assets, 'ver' => $ver];
	}
	set_transient('parafia_release', $out ?: 0, $out ? 6 * HOUR_IN_SECONDS : HOUR_IN_SECONDS);
	return $out;
}
// pakiet do aktualizacji danej części albo null
function parafia_update_for($part, $installed) {
	$rel = parafia_release();
	[, , $zip] = PARAFIA_PARTS[$part];
	if (!$rel || empty($rel['ver'][$part]) || empty($rel['assets'][$zip])) return null;
	return version_compare($rel['ver'][$part], $installed, '>') ? ['version' => $rel['ver'][$part], 'package' => $rel['assets'][$zip], 'url' => $rel['url']] : null;
}

add_filter('pre_set_site_transient_update_plugins', function ($t) {
	if (!is_object($t) || empty($t->checked)) return $t;
	foreach (PARAFIA_PARTS as $part => [$kind, $file]) {
		if ($kind !== 'plugin' || !isset($t->checked[$file])) continue;
		$u = parafia_update_for($part, $t->checked[$file]);
		$item = (object) ['slug' => dirname($file), 'plugin' => $file, 'new_version' => $u ? $u['version'] : $t->checked[$file],
			'url' => $u['url'] ?? 'https://github.com/' . PARAFIA_REPO, 'package' => $u['package'] ?? ''];
		if ($u) $t->response[$file] = $item; else { unset($t->response[$file]); $t->no_update[$file] = $item; }
	}
	return $t;
});
add_filter('pre_set_site_transient_update_themes', function ($t) {
	if (!is_object($t) || empty($t->checked)) return $t;
	$theme = PARAFIA_PARTS['brenna'][1];
	if (isset($t->checked[$theme]) && ($u = parafia_update_for('brenna', $t->checked[$theme])))
		$t->response[$theme] = ['theme' => $theme, 'new_version' => $u['version'], 'url' => $u['url'], 'package' => $u['package']];
	return $t;
});
// „Zobacz szczegóły” przy wtyczce: opis zmian z wydania zamiast błędu „nie znaleziono w katalogu”
add_filter('plugins_api', function ($res, $action, $args) {
	if ($action !== 'plugin_information' || !in_array($args->slug ?? '', ['parafia', 'parafia-dokumenty'], true)) return $res;
	$rel = parafia_release();
	return (object) [
		'name' => $args->slug === 'parafia' ? 'Parafia Brenna-Górki' : 'Parafia Brenna-Górki – dokumenty', 'slug' => $args->slug,
		'version' => $rel['ver'][$args->slug] ?? '', 'author' => 'Jarosław Sajdok', 'homepage' => 'https://github.com/' . PARAFIA_REPO,
		'sections' => ['changelog' => $rel ? wpautop(esc_html($rel['notes'])) : 'Brak informacji o wydaniu.'],
		'download_link' => $rel['assets'][PARAFIA_PARTS[$args->slug][2]] ?? '',
	];
}, 10, 3);
// „Sprawdź ponownie” w Kokpit → Aktualizacje pyta GitHuba od razu
add_action('load-update-core.php', function () { if (!empty($_GET['force-check'])) delete_transient('parafia_release'); });
