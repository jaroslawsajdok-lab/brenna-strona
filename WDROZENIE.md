# Wgranie nowej strony na brenna.luteranie.pl

Trzy pliki z folderu `dist/`: **`parafia.zip`** (wtyczka), **`brenna.zip`** (motyw) i **`parafia-dokumenty.zip`**
(pliki PDF: standardy ochrony małoletnich z załącznikami, ok. 8 MB).
Nowa strona startuje w **trybie próbnym**: odwiedzający dalej widzą starą stronę, a nową widzą tylko
redaktorzy parafii i osoby ze stałym linkiem. Zmiana na nową stronę dla wszystkich to jeden przycisk.

## 0. Kopia zapasowa (zawsze przed wgraniem)
Wtyczki → Dodaj nową → wyszukaj „UpdraftPlus” → Zainstaluj → Włącz → Ustawienia → UpdraftPlus →
„Utwórz kopię teraz”. Pobierz kopię na komputer.

## 1. Wtyczka
Wtyczki → Dodaj nową → **Wyślij wtyczkę na serwer** → wybierz `parafia.zip` → Zainstaluj → **Włącz**.
W menu kokpitu pojawi się pozycja **Parafia**.

## 1a. Dokumenty (raz)
Wtyczki → Dodaj nową → Wyślij wtyczkę na serwer → `parafia-dokumenty.zip` → Zainstaluj. **Włączać nie trzeba** –
to tylko pliki PDF, do których prowadzą linki na podstronie Dokumenty.
Jeśli WordPress odpowie, że plik jest za duży (limit wgrywania na hostingu bywa 8 MB), rozpakuj ZIP u siebie
i wgraj folder `parafia-dokumenty` przez FTP do `wp-content/plugins/`.

## 2. Motyw
Wygląd → Motywy → Dodaj nowy → **Wyślij motyw na serwer** → wybierz `brenna.zip` → Zainstaluj.
**Nie klikaj „Włącz”** – motyw ma tylko leżeć na serwerze. Włącza go przycisk w panelu Parafia (krok 5).

## 3. Konto proboszcza
Użytkownicy → Dodaj nowego → login (np. nazwisko), e-mail, silne hasło → Rola: **Redaktor parafii** → Dodaj.
Redaktor parafii może tylko edytować stronę parafii i wgrywać zdjęcia/pliki – nie zmieni ustawień WordPressa.

## 4. Link dla proboszcza
Kokpit → **Parafia** → skopiuj „Stały link do nowej strony” i wyślij proboszczowi.
- Link otwiera nowy wygląd (w tej przeglądarce przez rok).
- Edycja: róża Lutra w stopce strony (albo adres z `#edycja` na końcu) → login i hasło →
  **zaznaczone „Zapamiętaj mnie”** = zalogowany przez rok. Potem wystarczy otworzyć link i klikać w teksty.
- Zmiany zapisują się same po kilku sekundach (na pasku edycji: „Zapisano”).
- Gdyby link trafił w niepowołane ręce: Parafia → „Zmień link” (stary przestaje działać). Sam link i tak
  nie pozwala edytować – do edycji potrzebne jest logowanie.

## 5. Zmiana na nową stronę dla wszystkich
Kokpit → **Parafia** → **„Włącz nową stronę dla wszystkich”**. Powrót: „Wróć do starej strony”.

## Co jest zapisywane gdzie
| Na stronie | W WordPressie |
|---|---|
| Aktualności (tytuł, data, treść, zdjęcie główne, galeria) | zwykłe **Wpisy** – te same, co na starej stronie; zdjęcia w **Mediach** |
| Usunięcie aktualności | wpis trafia do **Kosza** (Wpisy → Kosz → Przywróć) |
| Teksty, kalendarz, grupy, pytania, kontakt, lista dokumentów | ustawienia wtyczki; **Parafia → Historia zmian → Przywróć** |
| Tabela nabożeństw | ustawienia wtyczki; historia jak wyżej |
| Pliki na podstronie Dokumenty | standardy z załącznikami – wtyczka „Parafia – dokumenty”; pliki dodane przez proboszcza – **Media** |

## Gdyby coś nie działało
- **Po zalogowaniu nic się nie dzieje / „Nie zapisano”** – wtyczka bezpieczeństwa (np. Wordfence,
  iThemes) może blokować REST API. W jej ustawieniach zezwól na `/wp-json/parafia/v1/`.
- **Goście widzą nowy wygląd przed włączeniem** – wtyczka przyspieszająca (cache: WP Super Cache,
  W3 Total Cache, LiteSpeed) podała zapamiętaną stronę. Wyczyść jej pamięć; tryb próbny wyłącza
  zapamiętywanie, ale stare kopie trzeba usunąć raz ręcznie.
- **Coś poszło źle** – Wtyczki → „Parafia Brenna-Górki” → Wyłącz. Strona wraca do starego wyglądu
  (wszystkie dotychczasowe wpisy i zdjęcia zostają). W ostateczności: kopia z kroku 0.

## Aktualizacja (nowa wersja motywu lub wtyczki)
U Jarosława: `cd src && python make_page.py`, potem `python narzedzia/wp_build.py` → nowe ZIP-y w `dist/`.
Na stronie: wgraj ZIP tak samo (`parafia-dokumenty.zip` tylko wtedy, gdy zmieniły się PDF-y) jak za pierwszym razem – WordPress zapyta „Zastąpić bieżącą wersję?” → Tak.
Treści proboszcza są w bazie, więc aktualizacja ich nie rusza.
