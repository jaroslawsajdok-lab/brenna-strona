<?php
/**
 * Plugin Name: Parafia Brenna-Górki
 * Description: Zapis treści edytowanych na stronie (teksty, nabożeństwa, aktualności, dokumenty), logowanie redaktora parafii, nowy wygląd w trybie próbnym (stały link) i przełącznik „nowa strona dla wszystkich”. Działa z motywem „Brenna-Górki”.
 * Version: 1.4.5
 * Requires at least: 6.4
 * Requires PHP: 7.4
 * Author: Jarosław Sajdok
 * Text Domain: parafia
 */
if (!defined('ABSPATH')) exit;

const PARAFIA_THEME = 'brenna';
const PARAFIA_CAP   = 'edit_parafia';
const PARAFIA_COOKIE = 'parafia_nowa';

require_once __DIR__ . '/aktualizacje.php';
require_once __DIR__ . '/haslo.php';          // hasło dnia z „Biblii na co dzień”   // aktualizacje jednym kliknięciem z wydań na GitHubie

/* ------------------------------------------------------------------
 * Włączenie / wyłączenie wtyczki: rola „Redaktor parafii”, prawo edycji dla administratora, klucz linku próbnego
 * ------------------------------------------------------------------ */
// role i uprawnienia: przy włączeniu wtyczki i przy każdej zmianie wersji (aktualizacja przez podmianę plików
// nie uruchamia haka włączenia). Prawo edycji strony parafii: Redaktor parafii, Administrator i wbudowany Redaktor WP.
const PARAFIA_ROLES_VER = 2;
function parafia_setup_roles() {
	if (!get_role('redaktor_parafii')) add_role('redaktor_parafii', 'Redaktor parafii', ['read' => true, 'upload_files' => true, PARAFIA_CAP => true]);
	foreach (['redaktor_parafii', 'administrator', 'editor'] as $r) if ($role = get_role($r)) $role->add_cap(PARAFIA_CAP);
	if (!get_option('parafia_token')) update_option('parafia_token', wp_generate_password(20, false), false);
	update_option('parafia_roles_ver', PARAFIA_ROLES_VER, false);
}
register_activation_hook(__FILE__, 'parafia_setup_roles');
add_action('init', function () { if ((int) get_option('parafia_roles_ver') < PARAFIA_ROLES_VER) parafia_setup_roles(); }, 0);
register_deactivation_hook(__FILE__, function () {
	// rola zostaje (żeby nie zgubić kont), ale wraca stary wygląd, jeśli nowy był włączony dla wszystkich
	if (get_option('stylesheet') === PARAFIA_THEME && ($prev = get_option('parafia_prev_theme'))) switch_theme($prev);
});

function parafia_can_edit() { return is_user_logged_in() && current_user_can(PARAFIA_CAP); }

/* ------------------------------------------------------------------
 * Tryb próbny: nowy wygląd widzi redaktor parafii i każdy, kto otworzył stały link (?nowa=klucz).
 * Pozostali odwiedzający widzą dotychczasowy motyw, dopóki administrator nie włączy nowej strony dla wszystkich.
 * ------------------------------------------------------------------ */
function parafia_preview() {
	static $on = null, $busy = false;
	if ($on !== null) return $on;
	if ($busy) return false;                       // get_option('stylesheet') niżej wywołuje ten sam filtr
	if (is_admin() || wp_doing_ajax() || (defined('REST_REQUEST') && REST_REQUEST) || !function_exists('wp_get_current_user') || !did_action('plugins_loaded')) return false;
	$busy = true;
	$active = get_option('stylesheet');
	$exists = wp_get_theme(PARAFIA_THEME)->exists();
	$token = get_option('parafia_token');
	$on = $active !== PARAFIA_THEME && $exists
		&& (parafia_can_edit() || ($token && isset($_COOKIE[PARAFIA_COOKIE]) && hash_equals($token, (string) $_COOKIE[PARAFIA_COOKIE])));
	$busy = false;
	return $on;
}
foreach (['pre_option_template', 'pre_option_stylesheet'] as $f)
	add_filter($f, function ($v) { return parafia_preview() ? PARAFIA_THEME : $v; });

// stały link: /?nowa=klucz zapamiętuje podgląd w tej przeglądarce na rok; /?nowa=0 wyłącza
add_action('init', function () {
	if (!isset($_GET['nowa']) || is_admin()) return;
	$v = sanitize_text_field(wp_unslash($_GET['nowa']));
	$token = get_option('parafia_token');
	$secure = is_ssl();
	if ($v === '0') setcookie(PARAFIA_COOKIE, '', time() - 3600, COOKIEPATH ?: '/', COOKIE_DOMAIN, $secure, true);
	elseif ($token && hash_equals($token, $v)) setcookie(PARAFIA_COOKIE, $token, time() + YEAR_IN_SECONDS, COOKIEPATH ?: '/', COOKIE_DOMAIN, $secure, true);
	nocache_headers();
	wp_safe_redirect(remove_query_arg('nowa'));
	exit;
}, 1);

// w trybie próbnym strona nie może trafić do pamięci podręcznej (inaczej goście zobaczyliby nowy wygląd)
add_action('send_headers', function () {
	if (parafia_preview()) { nocache_headers(); if (!defined('DONOTCACHEPAGE')) define('DONOTCACHEPAGE', true); }
});

// redaktor parafii zostaje zalogowany na rok, jeśli zaznaczy „Zapamiętaj mnie”
add_filter('auth_cookie_expiration', function ($len, $user_id, $remember) {
	return ($remember && user_can($user_id, PARAFIA_CAP)) ? YEAR_IN_SECONDS : $len;
}, 10, 3);

// redaktor parafii nie potrzebuje panelu WordPressa – po zalogowaniu w panelu trafia na stronę
add_filter('login_redirect', function ($to, $req, $user) {
	if (is_wp_error($user) || !$user || !user_can($user, PARAFIA_CAP)) return $to;
	// link „Zaloguj przez stronę logowania WordPressa” z okienka prosi o powrót na stronę (#edycja) – trzymamy się tego
	if ($req && wp_validate_redirect($req, false) && strpos($req, '/wp-admin') === false) return $req;
	return !user_can($user, 'edit_posts') ? home_url('/') : $to;
}, 10, 3);

/* ------------------------------------------------------------------
 * Dane dla strony (motyw wstawia je przed skryptami): zapisane teksty, nabożeństwa, aktualności, prawo edycji
 * ------------------------------------------------------------------ */
function parafia_img($id, $size = 'large') {
	$src = $id ? wp_get_attachment_image_url($id, $size) : '';
	return $src ?: '';
}
function parafia_post_data(WP_Post $p) {
	$main = null;
	if ($tid = get_post_thumbnail_id($p)) {
		$f = get_post_meta($p->ID, '_parafia_focus', true);
		[$fx, $fy] = is_string($f) && strpos($f, ',') ? array_map('floatval', explode(',', $f)) : [50, 50];
		$main = ['src' => parafia_img($tid), 'fx' => $fx, 'fy' => $fy, 'mid' => (int) $tid];
	}
	$gallery = [];
	foreach ((array) get_post_meta($p->ID, '_parafia_gallery', true) as $gid)
		if ($gid && ($src = parafia_img((int) $gid))) $gallery[] = ['src' => $src, 'mid' => (int) $gid];
	return [
		'wp' => $p->ID, 'title' => get_the_title($p), 'date' => get_the_date('Y-m-d', $p),
		'html' => apply_filters('the_content', $p->post_content), 'main' => $main, 'gallery' => $gallery,
	];
}
function parafia_boot() {
	$edit = parafia_can_edit();
	$posts = get_posts(['post_type' => 'post', 'post_status' => 'publish', 'numberposts' => 12, 'orderby' => 'date', 'order' => 'DESC']);
	$data = [
		'api' => esc_url_raw(rest_url('parafia/v1/')),
		'canEdit' => $edit,
		'nonce' => $edit ? wp_create_nonce('wp_rest') : '',
		'ajax' => $edit ? admin_url('admin-ajax.php') : '',
		'loginUrl' => wp_login_url(home_url('/#edycja')),
		'verse' => parafia_bncd(),                            // hasło dnia (null bez klucza)   // zwykłe logowanie WordPressa (działa też z CAPTCHA wtyczek bezpieczeństwa)
		'blocks' => (object) get_option('parafia_blocks', []),
		'services' => get_option('parafia_services', []),
		'posts' => array_map('parafia_post_data', $posts),
	];
	echo '<script>window.PARAFIA=' . wp_json_encode($data, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP) . ";</script>\n";
}

/* ------------------------------------------------------------------
 * REST API: /wp-json/parafia/v1/…
 * ------------------------------------------------------------------ */
add_action('rest_api_init', function () {
	$ns = 'parafia/v1';
	$editor = function () { return parafia_can_edit(); };

	register_rest_route($ns, '/login', ['methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'parafia_rest_login']);
	register_rest_route($ns, '/logout', ['methods' => 'POST', 'permission_callback' => 'is_user_logged_in', 'callback' => function () { wp_logout(); return ['ok' => true]; }]);

	register_rest_route($ns, '/blocks', ['methods' => 'POST', 'permission_callback' => $editor, 'callback' => function (WP_REST_Request $r) {
		$in = (array) $r->get_param('blocks');
		$all = get_option('parafia_blocks', []);
		foreach ($in as $k => $html) {
			$k = sanitize_key($k);
			if ($k === '' || !is_string($html) || strlen($html) > 200000) continue;
			// bez obcego formatowania (wklejonego z Worda): atrybuty style i znaczniki <font> precz
			$html = preg_replace(['/\sstyle\s*=\s*("[^"]*"|\'[^\']*\')/i', '#</?font[^>]*>#i'], '', $html);
			$all[$k] = wp_kses_post($html);
		}
		parafia_revision('blocks', get_option('parafia_blocks', []));
		update_option('parafia_blocks', $all, false);
		return ['ok' => true];
	}]);

	register_rest_route($ns, '/services', ['methods' => 'POST', 'permission_callback' => $editor, 'callback' => function (WP_REST_Request $r) {
		$rows = [];
		foreach (array_slice((array) $r->get_param('rows'), 0, 200) as $x) {
			$x = (array) $x;
			$rows[] = [
				'd' => preg_match('/^(\d{4}-\d{2}-\d{2}|\d{1,2}\.\d{1,2})$/', (string) ($x['d'] ?? '')) ? $x['d'] : '',   // pełna data albo dawne „8.11”
				'n' => sanitize_text_field($x['n'] ?? ''), 'b' => sanitize_text_field($x['b'] ?? ''),
				'g' => sanitize_text_field($x['g'] ?? ''), 'f' => !empty($x['f']),
			];
		}
		parafia_revision('services', get_option('parafia_services', []));
		update_option('parafia_services', $rows, false);
		return ['ok' => true];
	}]);

	register_rest_route($ns, '/posts', ['methods' => 'POST', 'permission_callback' => $editor, 'callback' => 'parafia_rest_save_post']);
	register_rest_route($ns, '/posts/(?P<id>\d+)', ['methods' => 'DELETE', 'permission_callback' => $editor, 'callback' => function (WP_REST_Request $r) {
		$p = get_post((int) $r['id']);
		if (!$p || $p->post_type !== 'post') return new WP_Error('parafia', 'Nie ma takiego wpisu.', ['status' => 404]);
		wp_trash_post($p->ID); // do kosza – da się przywrócić w panelu
		return ['ok' => true];
	}]);

	// PDF z innej strony (np. list biskupa na stronie innej parafii) dla podglądu na stronie: przeglądarka nie może
	// wczytać cudzego pliku (brak CORS), więc podajemy go stąd. Tylko https, tylko PDF, do 20 MB; wp_safe_remote_get
	// nie pobiera z adresów wewnętrznych/prywatnych. Pamiętane 12 godzin.
	register_rest_route($ns, '/pdf', ['methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => function (WP_REST_Request $r) {
		$url = esc_url_raw((string) $r->get_param('u'), ['https']);
		$word = (bool) preg_match('#\.docx$#i', (string) strtok($url, '?#'));   // PDF albo Word (.docx)
		if (!$url || !preg_match('#^https://[^/]+/.+\.(pdf|docx)$#i', strtok($url, '?#')))
			return new WP_Error('parafia', 'To nie jest adres dokumentu PDF ani Worda.', ['status' => 400]);
		$key = 'parafia_pdf_' . md5($url);
		$pdf = get_transient($key);
		if ($pdf === false) {
			$res = wp_safe_remote_get($url, ['timeout' => 20, 'redirection' => 3, 'limit_response_size' => 20 * MB_IN_BYTES, 'headers' => ['User-Agent' => 'parafia-brenna-gorki']]);
			$pdf = is_wp_error($res) || wp_remote_retrieve_response_code($res) !== 200 ? '' : wp_remote_retrieve_body($res);
			if (strncmp($pdf, $word ? "PK\x03\x04" : '%PDF', 4) !== 0) return new WP_Error('parafia', 'Nie udało się pobrać dokumentu.', ['status' => 502]);
			if (strlen($pdf) < 5 * MB_IN_BYTES) set_transient($key, $pdf, 12 * HOUR_IN_SECONDS);   // większych nie trzymamy w bazie
		}
		nocache_headers();
		header('Content-Type: ' . ($word ? 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' : 'application/pdf'));
		header('Content-Disposition: inline; filename="' . sanitize_file_name(basename(strtok($url, '?#'))) . '"');
		header('Content-Length: ' . strlen($pdf));
		header('X-Content-Type-Options: nosniff');
		echo $pdf;
		exit;
	}]);

	register_rest_route($ns, '/media', ['methods' => 'POST', 'permission_callback' => function () { return parafia_can_edit() && current_user_can('upload_files'); }, 'callback' => function () {
		require_once ABSPATH . 'wp-admin/includes/file.php';
		require_once ABSPATH . 'wp-admin/includes/media.php';
		require_once ABSPATH . 'wp-admin/includes/image.php';
		if (empty($_FILES['file'])) return new WP_Error('parafia', 'Brak pliku.', ['status' => 400]);
		$id = media_handle_upload('file', 0);
		if (is_wp_error($id)) return new WP_Error('parafia', $id->get_error_message(), ['status' => 400]);
		$full = ($_POST['size'] ?? '') === 'full';   // plakaty: pełny rozmiar, żeby dało się przeczytać drobny druk
		$url = wp_attachment_is_image($id) ? parafia_img($id, $full ? 'full' : 'large') : wp_get_attachment_url($id);
		return ['id' => $id, 'url' => $url];
	}]);
});

function parafia_rest_login(WP_REST_Request $r) {
	$ip = sanitize_text_field($_SERVER['REMOTE_ADDR'] ?? '');
	$key = 'parafia_fail_' . md5($ip);
	$fails = (int) get_transient($key);
	if ($fails >= 5) return new WP_Error('parafia', 'Zbyt wiele prób. Spróbuj ponownie za kilka minut.', ['status' => 429]);
	$user = wp_signon([
		'user_login' => sanitize_user((string) $r->get_param('u')),
		'user_password' => (string) $r->get_param('p'),
		'remember' => (bool) $r->get_param('r'),
	], is_ssl());
	if (is_wp_error($user)) {
		// złe dane – ogólny komunikat; inny powód (np. CAPTCHA albo blokada wtyczki bezpieczeństwa) – jego treść,
		// żeby było wiadomo, że trzeba użyć zwykłej strony logowania WordPressa
		$plain = ['invalid_username', 'incorrect_password', 'invalid_email', 'empty_username', 'empty_password'];
		$codes = $user->get_error_codes();
		if (array_intersect($codes, $plain) || !$codes) {
			set_transient($key, $fails + 1, 10 * MINUTE_IN_SECONDS);
			return new WP_Error('parafia', 'Nieprawidłowy login lub hasło.', ['status' => 403]);
		}
		$why = trim(wp_strip_all_tags($user->get_error_message()));
		return new WP_Error('parafia', 'Logowanie zablokowała ochrona strony' . ($why ? ' („' . $why . '”)' : '') . '. Użyj strony logowania WordPressa (link poniżej).', ['status' => 403]);
	}
	if (!user_can($user, PARAFIA_CAP)) {
		wp_logout();
		$roles = array_map(function ($r) { return translate_user_role(wp_roles()->roles[$r]['name'] ?? $r); }, (array) $user->roles);
		return new WP_Error('parafia', 'To konto nie ma prawa edycji strony parafii' . ($roles ? ' (rola: ' . implode(', ', $roles) . ')' : '') . '. Administrator może zmienić rolę na „Redaktor parafii” w Użytkownicy → Edytuj.', ['status' => 403]);
	}
	delete_transient($key);
	return ['ok' => true];
}

function parafia_rest_save_post(WP_REST_Request $r) {
	$id = (int) $r->get_param('wp');
	if ($id && (!($old = get_post($id)) || $old->post_type !== 'post')) return new WP_Error('parafia', 'Nie ma takiego wpisu.', ['status' => 404]);
	$date = preg_match('/^\d{4}-\d{2}-\d{2}$/', (string) $r->get_param('date')) ? $r->get_param('date') : current_time('Y-m-d');
	$arr = [
		'post_type' => 'post', 'post_status' => 'publish',
		'post_title' => sanitize_text_field((string) $r->get_param('title')),
		'post_content' => wp_kses_post((string) $r->get_param('html')),
		// dzisiejsza lub przyszła data = opublikuj teraz (inaczej WordPress ukryłby wpis jako zaplanowany)
		'post_date' => $date >= current_time('Y-m-d') ? current_time('mysql') : $date . ' 12:00:00',
	];
	if ($id) { $arr['ID'] = $id; $arr['edit_date'] = true; }
	else $arr['post_author'] = get_current_user_id();
	$id = $id ? wp_update_post($arr, true) : wp_insert_post($arr, true);
	if (is_wp_error($id)) return new WP_Error('parafia', $id->get_error_message(), ['status' => 400]);

	$main = $r->get_param('main');
	if (is_array($main) && !empty($main['id'])) {
		set_post_thumbnail($id, (int) $main['id']);
		update_post_meta($id, '_parafia_focus', round((float) ($main['fx'] ?? 50), 1) . ',' . round((float) ($main['fy'] ?? 50), 1));
	} elseif (!$main) delete_post_thumbnail($id);
	update_post_meta($id, '_parafia_gallery', array_values(array_filter(array_map('intval', (array) $r->get_param('gallery')))));
	return ['ok' => true, 'wp' => $id];
}

// prosta historia zmian: 20 ostatnich wersji tekstów i nabożeństw (do przywrócenia w razie pomyłki).
// Zapis automatyczny działa co kilka sekund, więc zmiany tej samej osoby w ciągu 10 minut to jedna sesja:
// zostaje stan sprzed jej początku.
function parafia_revision($what, $value) {
	$h = get_option('parafia_history', []);
	$who = get_current_user_id();
	foreach (array_reverse($h) as $e) {
		if ($e['what'] !== $what) continue;
		if ($e['who'] === $who && strtotime(current_time('mysql')) - strtotime($e['touched'] ?? $e['when']) < 10 * MINUTE_IN_SECONDS) {
			$h[array_search($e, $h, true)]['touched'] = current_time('mysql');
			update_option('parafia_history', $h, false);
			return;
		}
		break;
	}
	$h[] = ['what' => $what, 'when' => current_time('mysql'), 'touched' => current_time('mysql'), 'who' => $who, 'value' => $value];
	update_option('parafia_history', array_slice($h, -20), false);
}

/* ------------------------------------------------------------------
 * Panel „Parafia” w kokpicie: stały link, przełącznik nowej strony, redaktorzy, historia zmian
 * ------------------------------------------------------------------ */
add_action('admin_menu', function () {
	add_menu_page('Parafia', 'Parafia', 'manage_options', 'parafia', 'parafia_admin_page', 'dashicons-admin-home', 3);
});
add_action('admin_post_parafia', function () {
	if (!current_user_can('manage_options')) wp_die('Brak uprawnień.');
	check_admin_referer('parafia');
	$do = sanitize_key($_POST['do'] ?? '');
	if ($do === 'live' && wp_get_theme(PARAFIA_THEME)->exists() && get_option('stylesheet') !== PARAFIA_THEME) {
		update_option('parafia_prev_theme', get_option('stylesheet'), false);
		switch_theme(PARAFIA_THEME);
	} elseif ($do === 'old' && ($prev = get_option('parafia_prev_theme'))) {
		switch_theme($prev);
	} elseif ($do === 'bncd') {
		$k = trim(sanitize_text_field(wp_unslash($_POST['key'] ?? '')));
		if ($k !== '') update_option('parafia_bncd_key', $k, false);   // puste pole = klucz bez zmian
		delete_transient('parafia_bncd');
		parafia_bncd();
	} elseif ($do === 'token') {
		update_option('parafia_token', wp_generate_password(20, false), false);
	} elseif ($do === 'restore') {
		$i = (int) ($_POST['i'] ?? -1);
		$h = get_option('parafia_history', []);
		if (isset($h[$i])) update_option($h[$i]['what'] === 'blocks' ? 'parafia_blocks' : 'parafia_services', $h[$i]['value'], false);
	}
	wp_safe_redirect(admin_url('admin.php?page=parafia&ok=1'));
	exit;
});
function parafia_admin_page() {
	$live = get_option('stylesheet') === PARAFIA_THEME;
	$has = wp_get_theme(PARAFIA_THEME)->exists();
	$link = add_query_arg('nowa', get_option('parafia_token'), home_url('/'));
	$btn = function ($do, $label, $primary = false, $extra = '') {
		echo '<form method="post" action="' . esc_url(admin_url('admin-post.php')) . '" style="display:inline-block;margin:0 8px 8px 0">';
		wp_nonce_field('parafia');
		echo '<input type="hidden" name="action" value="parafia"><input type="hidden" name="do" value="' . esc_attr($do) . '">' . $extra;
		submit_button($label, $primary ? 'primary' : 'secondary', 'submit', false);
		echo '</form>';
	};
	echo '<div class="wrap"><h1>Parafia Brenna-Górki</h1>';
	if (!empty($_GET['ok'])) echo '<div class="notice notice-success is-dismissible"><p>Zrobione.</p></div>';
	if (!$has) echo '<div class="notice notice-error"><p>Wgraj motyw <b>Brenna-Górki</b> (Wygląd → Motywy → Dodaj nowy → Wyślij motyw na serwer). Nie trzeba go włączać.</p></div>';

	echo '<h2>Nowa strona</h2>';
	if ($live) {
		echo '<p><b>Nowa strona jest włączona dla wszystkich odwiedzających.</b></p>';
		if (get_option('parafia_prev_theme')) $btn('old', 'Wróć do starej strony');
	} else {
		echo '<p>Teraz odwiedzający widzą starą stronę. Nowy wygląd widzą tylko zalogowani redaktorzy parafii oraz osoby, które otworzą poniższy link.</p>';
		echo '<p><b>Stały link do nowej strony</b> (do wysłania proboszczowi; działa w danej przeglądarce przez rok):<br><input type="text" readonly value="' . esc_attr($link) . '" style="width:100%;max-width:640px" onclick="this.select()"></p>';
		$btn('token', 'Zmień link (stary przestanie działać)');
		echo '<p>Kiedy treści będą gotowe:</p>';
		if ($has) $btn('live', 'Włącz nową stronę dla wszystkich', true);
	}

	// wersje i aktualizacje z GitHuba
	if (!function_exists('get_plugin_data')) require_once ABSPATH . 'wp-admin/includes/plugin.php';
	$docs_file = WP_PLUGIN_DIR . '/parafia-dokumenty/parafia-dokumenty.php';
	$inst = ['parafia' => get_plugin_data(__FILE__, false, false)['Version'] ?? '',
		'brenna' => $has ? wp_get_theme(PARAFIA_THEME)->get('Version') : '',
		'parafia-dokumenty' => is_readable($docs_file) ? (get_plugin_data($docs_file, false, false)['Version'] ?? '') : ''];
	$rel = parafia_release();
	$names = ['parafia' => 'Wtyczka „Parafia”', 'brenna' => 'Motyw „Brenna-Górki”', 'parafia-dokumenty' => 'Dokumenty (PDF)'];
	// hasło dnia: klucz API i stan ostatniego pobrania
	$bst = get_option('parafia_bncd_status');
	echo '<h2>Hasło dnia</h2><p>Zielony pas na stronie pokazuje hasło dnia z serwisu <a href="https://biblianacodzien.pl/" target="_blank" rel="noopener">Biblia na co dzień</a>. Klucz API jest przypisany do domeny tej strony.</p>';
	$has_key = (string) get_option('parafia_bncd_key', '') !== '';
	$btn('bncd', 'Zapisz klucz', false, '<input type="text" name="key" autocomplete="off" placeholder="' . ($has_key ? 'klucz zapisany – wpisz nowy, aby zmienić' : 'klucz API') . '" style="width:340px"> ');
	if ($bst) echo '<p>Ostatnie pobranie: ' . esc_html($bst['when']) . ' – ' . ($bst['ok'] ? '<b>udane</b>' : '<b>nieudane</b> (' . esc_html($bst['why'] ?? '') . ')') . '</p>';
	elseif (!$has_key) echo '<p>Bez klucza na stronie zostaje hasło wpisane ręcznie.</p>';

	echo '<h2>Wersje</h2><table class="widefat striped" style="max-width:640px"><thead><tr><th></th><th>zainstalowana</th><th>najnowsza</th></tr></thead><tbody>';
	foreach ($names as $k => $n) {
		$new = $rel['ver'][$k] ?? '';
		$mark = ($new && $inst[$k] && version_compare($new, $inst[$k], '>')) ? ' <b>– jest nowsza</b>' : '';
		echo '<tr><td>' . esc_html($n) . '</td><td>' . esc_html($inst[$k] ?: '—') . '</td><td>' . esc_html($new ?: '—') . $mark . '</td></tr>';
	}
	echo '</tbody></table><p><a class="button" href="' . esc_url(admin_url('update-core.php?force-check=1')) . '">Sprawdź aktualizacje</a> ';
	if ($rel) echo 'Ostatnie wydanie: <a href="' . esc_url($rel['url']) . '" target="_blank" rel="noopener">' . esc_html($rel['tag']) . '</a>';
	elseif ($err = get_option('parafia_release_err')) echo '<b>Nie udało się sprawdzić wersji</b> (' . esc_html($err['when'] . ' – ' . $err['why']) . '). Kolejna próba za kilkanaście minut albo przyciskiem obok.';
	echo '</p><p>Nowe wersje instalujesz w <b>Kokpit → Aktualizacje</b> przyciskiem „Aktualizuj” – bez wgrywania plików. Treści proboszcza zostają.</p>';

	echo '<h2>Redaktorzy</h2><p>Proboszcz potrzebuje konta z rolą <b>Redaktor parafii</b> (Użytkownicy → Dodaj nowego → Rola: Redaktor parafii). Loguje się na stronie: róża Lutra w stopce albo adres strony z <code>#edycja</code> na końcu. Zaznaczone „Zapamiętaj mnie” trzyma go zalogowanym przez rok. Administrator też może edytować.</p>';

	$h = get_option('parafia_history', []);
	echo '<h2>Historia zmian</h2>';
	if (!$h) echo '<p>Na razie brak zmian.</p>';
	else {
		echo '<p>Poprzednie wersje tekstów i tabeli nabożeństw (20 ostatnich). „Przywróć” wraca do stanu sprzed danej zmiany.</p><table class="widefat striped" style="max-width:760px"><tbody>';
		foreach (array_reverse($h, true) as $i => $e) {
			$u = get_userdata($e['who']);
			echo '<tr><td>' . esc_html($e['when']) . '</td><td>' . ($e['what'] === 'blocks' ? 'teksty' : 'nabożeństwa') . '</td><td>' . esc_html($u ? $u->display_name : '–') . '</td><td>';
			$btn('restore', 'Przywróć', false, '<input type="hidden" name="i" value="' . (int) $i . '">');
			echo '</td></tr>';
		}
		echo '</tbody></table>';
	}
	echo '</div>';
}
