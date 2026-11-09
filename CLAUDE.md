# Strona parafii Brenna-Górki – prototyp

Nowa strona Parafii Ewangelicko-Augsburskiej Brenna-Górki (brenna.luteranie.pl, Diecezja Cieszyńska).
Prowadzi: Jarosław Sajdok. Odbiorca: proboszcz „starej daty” i parafianie, często starsi.
Teraz: jeden plik HTML jako prototyp. Docelowo: WordPress na hostingu luteranie.pl (własny motyw + własna wtyczka), bez Railwaya.

## Zasady współpracy
- Odpowiadaj po polsku, konkretnie, bez korpomowy. Jak coś jest złym pomysłem – powiedz wprost.
- W tekstach nigdy „świątynia” – u ewangelików jest „kościół”.
- Nazwy świąt: „Epifania”, „Dzień Pokuty i Modlitwy” (zamiast Popielca), „Zesłanie Ducha Świętego” (nie „Zielone Świątki”), „Święto Reformacji”, „Niedziela Wieczności”.
- Nie wymyślaj treści udających prawdziwe (nagrania, opinie, liczby, nazwiska). Brakujące dane oznaczaj klasą `.todo` i wypisz w raporcie.
- Fakty o parafii sprawdzaj, zanim wpiszesz (adres kościoła w Górkach, diecezja, godziny).

## Czego NIE ruszamy
- **Nagłówek** (animowany rysunek kreską: kościoły, las, pory roku, sceny roku liturgicznego, menu w nagłówku) i **zielony pasek menu `.joint`**, który przykleja się u góry. Jarosław: „genialne w swej prostocie”. Wygląd i zachowanie zostają.
- Sceny świąteczne w nagłówku zmieniamy tylko na wyraźną prośbę parafii.
- Menu w nagłówku ma 6 pozycji (3 + 3 wokół kościoła); „Dokumenty” dopisuje `make_page.py` przy składaniu (plików nagłówka nie edytujemy).
- **Drzwi do spaceru 360°** (okrągłe drewniane drzwi z różą Lutra w dziale Aktualności, po prawej; na telefonie na górze działu) – jedyne miejsce, gdzie drewno ma zostać. Rysują się kreską, gdy pojawią się na ekranie; po kliknięciu odrysowują się (kolor schodzi, kreski się zwijają) i w kole zostaje spacer. „Pełny ekran” powiększa koło, „Zamknij pełny ekran”/Esc wraca. Skrzydła się nie obracają.
- Działu Kazania nie ma (transmisji i nagrań nie będzie).

## Kierunek wyglądu (poniżej nagłówka)
Strona ma nie wyglądać na zrobioną przez AI. Obowiązuje:
- Tło `#f3f3f0` (neutralny kamień), zieleń parafii `--spruce #2f5d45` / `--spruce-d #24493a` jako jedyny akcent, tusz `#1d1d1b`. Bez kremu, bez fioletu, bez gradientów.
- Pismo: PT Sans (tekst) + PT Sans Narrow (tytuły działów). Pięć rozmiarów: 14 · 17 · 20 · 30 · 52 px.
- Bez: drewnianych ramek i listew (poza drzwiami), falistych przejść, cieni na elementach w spoczynku, cienkich linii-dzielników (linie tylko w prawdziwych tabelach i polach formularzy), napisów wersalikami nad nagłówkami, strzałek „→” w linkach, emoji/znaków jako ikon (ikony = SVG, klasa `.ico`), kart z ikoną na górze, układu „jedno duże + cztery małe”.
- Działy oddziela przestrzeń i lekka zmiana tła (`--tone #e8ebe5`, zielony pas dla hasła tygodnia).
- Ruch: tylko nagłówek i rysowanie/odrysowanie drzwi. Żadnych „fade-in” każdego działu. Szanuj `prefers-reduced-motion`.
- Dostępność: kontrast ≥ 4,5:1, widoczny fokus, cele dotykowe ≥ 44 px, brak przewijania w bok przy 390/768/1440.

## Pliki (`src/`)
| Plik | Co to |
|---|---|
| `naglowek.html` | baza nagłówka (HTML+CSS) |
| `header2_js.txt` | JS nagłówka: układ, niebo/słońce/księżyc, liście (symulacja zegarowa, ksiądz grabi o :57), śnieg i pług (:59), zwierzęta, turyści |
| `feasts_js.txt` | rok liturgiczny: `easter()`, `advent1()`, `feastOf()`, `feastList()`, sceny (`wczwartek()`, `zielone()`, `reformacja()`, `groby()`…), `feastTick()`, `HARVEST` (ręczne daty Święta Żniw) |
| `make_compact.py` | składa `naglowek-kompakt.html` z powyższych |
| `page_content.html` | treść strony (działy pod nagłówkiem, stopka) |
| `page_style.css` | style działów (stara warstwa – jest w niej drewno; `calm.css` je nadpisuje) |
| `calm.css` | **aktualny kierunek wyglądu** – nadpisuje stare warstwy; ładowany jako ostatni |
| `bottom.css` | kontakt, mapa Google (przełącznik Brenna/Górki), formularz, stopka, okno logowania |
| `services_editor.js/.css` | tabela nabożeństw: przełącznik miesięcy nad tabelą (goście: miesiące z nabożeństwami; edycja: do 24 miesięcy naprzód, „+ Dodaj wszystkie niedziele miesiąca”), pełna data wiersza w `data-date` (RRRR-MM-DD; wpisane „8.11” dostaje rok według oglądanego miesiąca), edycja wierszy, sortowanie, dzień tygodnia, „najbliższe”, minione znikają; pasek „Najbliższe nabożeństwo” pod menu |
| `post_editor.js/.css` | aktualności: okno edycji (tytuł, data, zdjęcie główne z punktem kadru, treść, galeria), przeglądarka zdjęć |
| `login.js` | logowanie (róża Lutra w stopce lub `#edycja`; prototyp: `proboszcz` / `brenna`), tryb edycji, las w stopce, przełącznik mapy, flaga `?podglad` |
| `pano_viewer.js/.css` | dawna własna przeglądarka spaceru (CSS 3D) – nieużywana: przy dużym ekranie rozjeżdżała się w kwadraty; zastąpiona oryginalnym odtwarzaczem |
| `tour.js` | drzwi (rysowanie, odrysowanie po kliknięciu), spacer w kole i „Pełny ekran”: oryginalny odtwarzacz 3DVista z luteranie-wirtualne-muzea.pl w ramce (w kole wyższa niż koło, żeby pasek miniatur wypadł pod obręcz; na dotyku osłona przepuszcza przewijanie), `#media=N` otwiera od N-tego punktu (drzwi otwierają od 9 – nawa) |
| `wp.js` | łącznik z WordPressem (działa tylko, gdy wtyczka wstawi `window.PARAFIA`): wkleja zapisane bloki `[data-key]` i wiersze nabożeństw, w trybie edycji zapisuje sam po kilku sekundach, `PARAFIA.call/upload` dla pozostałych modułów |
| `docs.js` | podstrona Dokumenty (ochrona małoletnich, RODO, inne): w prototypie widok `#dokumenty` w tym samym pliku; w trybie edycji „+ Dodaj plik” |
| `make_page.py` | **składa `brenna-strona.html`** (nagłówek + treść + wszystkie CSS/JS + obrazy drzwi jako data URI) |
| `door/`, `door_svg.py`, `door_parts.html` | drzwi do spaceru (generator SVG drzwi wklejonych w `page_content.html`) |
| `dokumenty/` | PDF-y podstrony Dokumenty: standardy ochrony małoletnich (25.07.2024) + załączniki 1–15 (nazwy `zalacznik-NN.pdf`); w WordPressie jako osobna wtyczka `parafia-dokumenty` (`wp_build.py`) |
| `font/` | PT Sans i PT Sans Narrow (fontsource) – do wgrania na serwer w WordPressie |

## Budowanie i sprawdzanie
```bash
cd src
python3 make_compact.py      # po zmianach w naglowek.html / header2_js.txt / feasts_js.txt
python3 make_page.py         # po każdej zmianie – składa brenna-strona.html
cd ..
python3 narzedzia/zrzuty.py  # zrzuty 1440/768/390 do zrzuty/, wykrywa przewijanie w bok i błędy JS
python3 narzedzia/sceny.py zielone reformacja   # sceny świąteczne nagłówka
python3 narzedzia/wp_build.py # motyw + ZIP-y do WordPressa: dist/brenna.zip, dist/parafia.zip
python3 narzedzia/spakuj.py  # wersja pokazowa w jednym pliku: pokaz/brenna-strona-pokaz.html (czcionki i zdjęcia w środku, panele podglądu zawsze, przycisk „Edycja strony (pokaz)”; spacer i mapa wymagają internetu)
```
Komputer Jarosława to Windows: polecenie to `python` (albo `py`), nie `python3`.
Wymaga: Python 3 + `pip install playwright` + `python -m playwright install chromium`.
Do pomiaru „czy wygląda na AI” używaj skilla taste-skill (lint + inspect) i oglądaj zrzuty – nie oceniaj z samego kodu.
Przyciski podglądu (pora roku, święta, czas, telefon) pokazują się tylko z `?podglad` w adresie.

## WordPress (stan: wersja 1.2.0 na GitHubie, aktualizacje jednym kliknięciem przetestowane lokalnie)
- Wtyczka: `wordpress/parafia/parafia.php` (źródło). Motyw składa `narzedzia/wp_build.py` z `src/brenna-strona.html` → `dist/brenna/`, ZIP-y w `dist/` (poza gitem): `brenna.zip`, `parafia.zip`, `parafia-dokumenty.zip` (PDF-y z `src/dokumenty`, linki `{{DOCS}}`).
- Bloki edytowalne mają stałe klucze `data-key` (np. `tekst-1`, `nabozenstwa`) – **nie zmieniać ich**, bo pod nimi są zapisane treści proboszcza. Nowy blok = nowy klucz.
- Tryb próbny: nowy wygląd widzi redaktor parafii i ktoś ze stałym linkiem `/?nowa=klucz`; przełącznik „nowa strona dla wszystkich” w kokpicie → Parafia.
- Aktualności = zwykłe wpisy WP (te same co na starej stronie), zdjęcia i dokumenty w Mediach, teksty i nabożeństwa w opcjach wtyczki z historią (Parafia → Historia zmian).
- Test lokalny: `narzedzia/wp_test/` (blueprint Playground + `test_flow.py`; dane testowego konta w blueprint.json). Uruchomienie w Git Bash wymaga `MSYS_NO_PATHCONV=1`.
- Instrukcja wgrania: `WDROZENIE.md`.
- Repozytorium (publiczne): https://github.com/jaroslawsajdok-lab/brenna-strona. **Nowa wersja:** `GH_TOKEN=$(gh auth token) python narzedzia/wydanie.py X.Y.Z "opis"` (Python ze Sklepu Microsoft nie widzi logowania gh – stąd GH_TOKEN). Wydanie = ZIP-y + `wersje.json`; wtyczka (`aktualizacje.php`) pokazuje w WordPressie „Aktualizuj”. `DOCS_VERSION` w `wp_build.py` podnosić tylko przy zmianie PDF-ów.
- Test aktualizacji: `narzedzia/wp_test/blueprint_aktualizacja.json` (stare wersje rozpakowane z ZIP-ów; podpięte foldery `--mount` nie nadają się do testu aktualizacji – WordPress nie podmieni podpiętego folderu).

## Wiadome braki (stan na 29.10.2026)
- Brak prawdziwych zdjęć poza miniaturami aktualności (galeria, plakaty, duszpasterz puste). Potrzebne: kościół w Brennej, kościół w Górkach, ludzie, wnętrze – od parafii / z FB za zgodą proboszcza.
- Treści zastępcze do usunięcia lub uzupełnienia: nagrania kazań z wymyślonymi długościami, „Tu proboszcz wpisze…”, „imię i nazwisko” duszpasterza, hasło tygodnia (nieaktualne, powinno liczyć się samo z roku kościelnego), adres kościoła w Górkach, skład Zespołu Wsparcia (ochrona małoletnich, wyznacza go uchwała Rady Parafialnej), pliki RODO na podstronie Dokumenty (klauzula informacyjna, polityka prywatności).
- Do decyzji z proboszczem: czy zostają działy Kalendarz (dubluje tabelę i aktualności) i Galerie.
- Prototyp nie zapisuje zmian (po odświeżeniu znikają) – zapis będzie w WordPressie.

## Plan WordPressa
- Własny motyw z tym HTML/CSS/JS; własna wtyczka „Parafia”:
  - tabela nabożeństw (wiersze: data, nazwa, Brenna, Górki, święto) zapisywana przez REST API,
  - aktualności jako wpisy z obrazkiem wyróżniającym + galerią (biblioteka mediów),
  - bloki tekstu „data-edit” zapisywane jako opcje / meta,
  - podstrona `/dokumenty/` z plikami z biblioteki mediów (grupy: ochrona małoletnich, RODO, inne),
  - edycja na stronie (nie w panelu WP): logowanie przez `wp_signon`, rola „Redaktor parafii” z ograniczonymi uprawnieniami, nonce, rewizje,
  - panel do włączania/wyłączania animacji nagłówka (dla Jarosława, nie dla proboszcza).
- Bez importu z Facebooka i bez kalendarzy po API – proboszcz wpisuje wszystko ręcznie.
- Czcionki z własnego serwera, nie z Google.
