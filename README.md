# Konwerter plików

Projekt 1 z Programowania V. Aplikacja okienkowa (Tkinter), która zamienia pliki między formatami CSV, JSON, TXT, DOCX, ODT i PDF.

## Wymagania

- Python 3.10 lub nowszy
- biblioteki z `requirements.txt` (`python-docx`, `pytest`)
- LibreOffice, potrzebny tylko do PDF i ODT ([libreoffice.org](https://www.libreoffice.org/download/))

Program sam szuka LibreOffice w PATH i w domyślnym miejscu instalacji (Windows, macOS). Jeśli jest zainstalowany gdzie indziej, ustaw zmienną `SOFFICE` na ścieżkę do pliku `soffice`.

## Instalacja i uruchomienie

```
pip install -r requirements.txt
python main.py
```

W oknie wybierz plik, format i folder zapisu, potem kliknij „Konwertuj”. Lista formatów pokazuje tylko te, na które da się zamienić wybrany plik. Jeśli plik wynikowy już istnieje, program pyta, czy go nadpisać.

Jest też wersja konsolowa:

```
python cli.py przyklady/dane.csv json .
```

W konsoli istniejący plik nie jest nadpisywany, wynik dostaje nazwę `dane (1).json`. Nadpisanie wymusza opcja `--nadpisz`.

## Obsługiwane konwersje

| Z | Na | Jak | Ograniczenia |
|---|---|---|---|
| CSV | JSON | moduł `csv` | wszystkie wartości są tekstem (`"30"`, nie `30`) |
| JSON | CSV | moduły `json`, `csv` | zagnieżdżone listy i obiekty trafiają do komórki jako tekst JSON |
| TXT | DOCX | python-docx | bez formatowania, każda linia to osobny akapit |
| DOCX | TXT | python-docx | tylko tekst akapitów, bez tabel i obrazków |
| DOCX | PDF | LibreOffice | układ stron może się lekko różnić od Worda |
| ODT | PDF | LibreOffice | jak wyżej |
| DOCX | ODT | LibreOffice | złożone formatowanie może się zmienić |
| ODT | DOCX | LibreOffice | jak wyżej |

Zasady dla CSV i JSON:

- pliki muszą być w UTF-8; wynikowy CSV ma BOM, żeby Excel dobrze pokazał polskie znaki,
- separator CSV (`;` albo `,`) jest wykrywany z pierwszego wiersza, wynikowy CSV używa `,`,
- pierwszy wiersz CSV to nagłówki; nazwy i kolejność kolumn są zachowane,
- JSON musi być listą obiektów albo jednym obiektem; kolumny CSV to wszystkie klucze w kolejności wystąpienia, brakująca wartość daje pustą komórkę.

Błędy są pokazywane w oknie i zapisywane do pliku `konwerter.log`.

## Przykładowe dane

W folderze `przyklady/`:

| Plik | Konwersja | Oczekiwany wynik |
|---|---|---|
| `dane.csv` | na JSON | lista 4 obiektów, polskie znaki i puste pola zachowane |
| `dane.json` | na CSV | te same kolumny w tej samej kolejności |
| `notatka.txt` | na DOCX | dokument, w którym każda linia jest akapitem |
| `notatka.docx`, `notatka.odt` | na PDF | PDF z tym samym tekstem |
| `zly.json` | na CSV | błąd „Zły JSON w linii 3…”, plik nie powstaje |
| `uszkodzony.docx` | na PDF lub TXT | błąd „plik jest uszkodzony…”, plik nie powstaje |

## Testy

```
python -m pytest -v
```

| Przypadek | Test | Wynik |
|---|---|---|
| Poprawny plik, dane | `test_csv_do_json`, `test_json_do_csv` | OK |
| Poprawny plik, tekst | `test_txt_do_docx`, `test_docx_do_txt` | OK |
| Poprawny plik, PDF | `test_docx_do_pdf` (pomijany, gdy nie ma LibreOffice) | OK |
| Błędny lub uszkodzony plik | `test_zly_json`, `test_csv_z_inna_liczba_pol`, `test_uszkodzony_docx` | OK |
| Nieobsługiwana para | `test_validate_nieobslugiwana_para`, `test_available_targets` | OK |
| Brak LibreOffice | `test_brak_libreoffice` | OK |
| Plik docelowy już istnieje | `test_istniejacy_plik_nie_jest_nadpisywany`, `test_nadpisanie_na_zyczenie` | OK |
| Polskie znaki i puste wartości | `test_csv_do_json`, `test_json_do_csv` | OK |
| Brak pliku lub katalogu | `test_validate_brak_pliku`, `test_validate_brak_katalogu` | OK |

Ręcznie w oknie sprawdzono: lista formatów zależy od wybranego pliku, przycisk „Konwertuj” jest zablokowany bez kompletu danych, przy istniejącym pliku pojawia się pytanie o nadpisanie, okno nie zawiesza się podczas konwersji.

## Struktura

```
main.py        start okna
cli.py         wersja konsolowa
core/          rejestr konwerterów, walidacja, błędy, log
converters/    data.py (CSV, JSON), text.py (TXT, DOCX), office.py (LibreOffice)
gui/           okno, dialogi, wątek konwersji, wygląd
tests/         testy pytest
przyklady/     dane testowe
```

Nowy format dodaje się jedną funkcją z dekoratorem `@register(".z", ".na")` w `converters/`. Okno samo pokaże go na liście.

## Źródła i narzędzia

- dokumentacja Pythona (`csv`, `json`, `subprocess`, `tkinter`, `logging`), python-docx, LibreOffice (parametry wiersza poleceń)
- przy pisaniu kodu i testów korzystałem z asystenta AI (Claude); 

## Autor

Maciej Pitulski 105476