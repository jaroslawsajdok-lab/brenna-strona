<?php
/**
 * Hasło dnia z serwisu „Biblia na co dzień” (biblianacodzien.pl) – oficjalne API z kluczem.
 * Klucz jest przypisany do domeny strony parafii; serwis sprawdza ją w nagłówku Origin, więc zapytanie
 * przedstawia się adresem tej strony (home_url). Pobieramy raz dziennie (do północy), ostatnie udane hasło
 * zostaje na zapas, gdyby serwis nie odpowiadał. Bez klucza – na stronie zostaje hasło wpisane ręcznie.
 */
if (!defined('ABSPATH')) exit;

const PARAFIA_BNCD_API = 'https://biblianacodzien.pl/bncd/api/open-node/';

function parafia_bncd() {
	$key = trim((string) get_option('parafia_bncd_key', ''));
	if ($key === '') return null;
	$today = current_time('Y-m-d');
	$cached = get_transient('parafia_bncd');
	if (is_array($cached) && ($cached['day'] ?? '') === $today) return $cached['data'];

	$home = wp_parse_url(home_url('/'));
	$origin = ($home['scheme'] ?? 'https') . '://' . ($home['host'] ?? '');
	$res = wp_remote_post(PARAFIA_BNCD_API, [
		'timeout' => 8,
		'headers' => ['Content-Type' => 'application/json', 'Origin' => $origin, 'Referer' => $origin . '/', 'User-Agent' => 'parafia-brenna-gorki'],
		'body' => wp_json_encode(['key' => $key]),
	]);
	$d = is_wp_error($res) ? null : json_decode(wp_remote_retrieve_body($res), true);
	$verse = null;
	if (is_array($d) && ($d['status'] ?? '') === 'ok' && !empty($d['first'])) {
		// wydawca wyróżnia pogrubieniem właściwy tekst wersetu – zostawiamy tylko <b>, resztę znaczników usuwamy
		$clean = function ($h) { return trim(wp_kses(preg_replace('#</?p[^>]*>#i', '', (string) $h), ['b' => [], 'i' => []])); };
		$verse = [
			'date' => (string) ($d['date'] ?? ''), 'day' => mb_strtolower((string) ($d['day'] ?? '')),
			'name' => !empty($d['is_name']) ? sanitize_text_field($d['name'] ?? '') : '',
			'first' => $clean($d['first']), 'first_s' => sanitize_text_field($d['first_s'] ?? ''),
			'second' => !empty($d['is_second']) ? $clean($d['second']) : '', 'second_s' => sanitize_text_field($d['second_s'] ?? ''),
		];
		update_option('parafia_bncd_last', $verse, false);
		update_option('parafia_bncd_status', ['ok' => true, 'when' => current_time('mysql')], false);
	} else {
		$why = is_wp_error($res) ? $res->get_error_message() : (is_array($d) ? (string) ($d['message'] ?? $d['error'] ?? 'nieznany błąd') : 'brak odpowiedzi');
		update_option('parafia_bncd_status', ['ok' => false, 'when' => current_time('mysql'), 'why' => $why], false);
		$verse = get_option('parafia_bncd_last') ?: null;   // zapas: ostatnie udane hasło
	}
	// do północy (gdy się nie udało – ponowna próba za godzinę)
	$midnight = (new DateTime('tomorrow', wp_timezone()))->getTimestamp() - time();
	set_transient('parafia_bncd', ['day' => $today, 'data' => $verse], $d && ($d['status'] ?? '') === 'ok' ? max(600, $midnight) : HOUR_IN_SECONDS);
	return $verse;
}
