# Przeniesienie projektu do Claude Code – krok po kroku

## 1. Rozpakuj i przygotuj folder
```bash
unzip brenna-code.zip -d ~/Projekty/
cd ~/Projekty/brenna-code
git init && git add -A && git commit -m "Prototyp strony Brenna-Górki – start w Claude Code"
```
Git daje historię zmian: każdą rundę poprawek można cofnąć.

## 2. Zainstaluj narzędzia do zrzutów
```bash
pip install playwright
playwright install chromium
```
Node 22 lub nowszy jest potrzebny dla inspektora taste-skill (`node -v`).

## 3. Uruchom Claude Code w tym folderze
```bash
claude
```
Claude Code sam przeczyta `CLAUDE.md`: zasady, mapę plików, czego nie ruszać, braki, plan WordPressa.
`.claude/settings.json` pozwala mu budować stronę i robić zrzuty bez pytania. Blokuje edycję plików nagłówka (`naglowek.html`, `header2_js.txt`). Sceny świąteczne w `feasts_js.txt` może zmieniać, ale tylko gdy go poprosisz.

## 4. Zainstaluj skille (wpisz w Claude Code, po kolei)
```
/plugin marketplace add pbakaus/impeccable
/plugin install impeccable@impeccable

/plugin marketplace add Leonxlnx/taste-skill
/plugin install taste-skill@taste-skill

/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill

/plugin marketplace add anthropics/claude-plugins-official
/plugin install frontend-design@claude-plugins-official
```
Jeśli któryś katalog już jest dodany, Claude Code to zgłosi i nic się nie stanie. Po instalacji zrestartuj Claude Code (`/exit`, potem `claude`).
Uwaga: Impeccable przy pierwszym użyciu pobiera własny program-detektor. Claude Code zapyta o zgodę.

## 5. Pierwszy prompt (skopiuj w całości)

```
Przeczytaj CLAUDE.md. Pracujemy nad prototypem strony parafii Brenna-Górki w src/.
Nagłówka i paska menu .joint NIE ruszamy (wygląd i zachowanie zostają). Drzwi do spaceru 360° też zostają.

Zadanie: pętla poprawek wyglądu wszystkiego poniżej nagłówka, aż strona przestanie wyglądać na zrobioną przez AI.
Każda runda:
1. cd src && python3 make_page.py
2. taste-skill: lint + inspect na src/brenna-strona.html (1440/768/390), potem obejrzyj zrzuty i oceń według references/critique.md (format RUNDA n).
3. Impeccable: /impeccable critique na tę samą stronę – porównaj wnioski z taste-skill.
4. Popraw trzy najważniejsze problemy (kolejność: idea → hierarchia → kompozycja → typografia → obrazy → kolor → detale → ruch). Korzystaj z ui-ux-pro-max jako listy kontrolnej dostępności i UX, ale NIE bierz jego palety ani czcionek – kierunek jest w CLAUDE.md.
5. git commit z opisem rundy.
Maksymalnie 5 rund. Nie wymyślaj treści: braki oznacz .todo i wypisz.
Na koniec raport po polsku: oceny z ostatniej rundy, co poprawione, czego nie da się poprawić bez zdjęć i decyzji proboszcza, oraz które uwagi inspektora świadomie zostają (nagłówek, menu).
```

## 6. Kolejne kroki (osobne prompty, gdy będziesz gotów)
- **Zdjęcia:** wrzuć je do `src/zdjecia/` i napisz: „Wstaw zdjęcia z src/zdjecia do galerii, plakatów i działu Parafia; zrób rundę taste-skill”.
- **Treści od proboszcza:** „Uzupełnij treści z pliku …, usuń .todo, usuń dział Kalendarz” (albo co ustalicie).
- **WordPress:** „Zgodnie z planem w CLAUDE.md zbuduj motyw i wtyczkę ‘Parafia’ w folderze wordpress/ – zacznij od tabeli nabożeństw przez REST API”.
