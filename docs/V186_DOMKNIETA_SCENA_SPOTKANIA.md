# V186 — zsynchronizowana i domknięta scena spotkania

## Zachowanie i grafika

- Chłopiec patrzy przed siebie w pierwszych ujęciach. Przy mijaniu dziewczyny
  w 4488 ogląda się za nią.
- W 4862 jednocześnie pojawiają się dziubek i pierwsza nuta przy ustach.
  Gwizd trwa przez oba ujęcia oddalania dziewczyny.
- W 5610 dziewczyna dochodzi do drzwi. Melodia jest wygaszona, PMG wyłączone,
  a chłopiec wraca do spokojnej, odwróconej pozy.
- Zachowano kadrowanie v175, dokładne klatki bocznego spaceru oraz wszystkie
  cztery skale i tor dziewczyny z v181. Dalsze sceny zachowują swoje ticki.

Nuty i klucz wiolinowy są pełnymi, czytelnymi kształtami players. Dwie
skończone fale emitują je kolejno, co sześć faz. Każdy znak ma własny
zakrzywiony tor, łagodnie odpływa od ust w górę i w lewo, ma oderwany ślad
missiles i barwy przechodzące przez paletę Atari. Ostatnie dziesięć faz lotu
stopniowo zmniejsza jasność do 2. Ostatnia fala gaśnie około 0,14 s przed
dojściem dziewczyny do drzwi; znaki nie są ucinane w połowie kolejnego obiegu.

W portrecie gwizdania wyczyszczono resztki promieni starej grafiki poza
twarzą i narysowano usta w logicznych pikselach, żeby dziubek był wyraźny
w rozdzielczości 160×64. Maski włosów i kurtki pozostają kryjące.

## Pamięć i wynik

- `build/visual-prototype-v186.xex` i JSON; dev identyczny.
- SHA-256: `659de1c7a5bf496653094946064912e0b99cb64496b5f8efddfb224bfaca7b37`.
- 298 wspólnych wierszy, 11 480 B danych wierszy, 2552 B kodu głównego.
- Helper PMG: 1119 B, $6A00–$6E5E w banku loadera 0. Do cleanup $6F00
  pozostaje 161 B. Banki 1–63 są identyczne bajt w bajt z v185.
- Istniejące dwa bufory PMG są przygotowywane poza aktywnym obrazem
  i przełączane w dolnym blankingu. PORTB jest przywracany.

## Sprawdzenie i ograniczenia

[ODCZYT] 15 ukierunkowanych testów CPU/grafiki zaliczonych: równoczesne
usta i pierwsza nuta, skończone fale, odrębne tory, jasność końcowych faz,
brak PMG po dojściu do drzwi, bufory i PORTB, maski, kadry i panorama v175,
trajektoria do drzwi oraz regresje piłki.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 6 220 440 identycznych
bajtów względem v035, cały utwór. Emulator zainstalowany jako AppImage działa
z `APPIMAGE_EXTRACT_AND_RUN=1`; wcześniejsza przeszkoda FUSE została ominięta
standardowym trybem uruchomienia AppImage po rozpakowaniu.

[ODCZYT] `make check`: 139 testów, 126 zaliczonych, 10 niezaliczonych,
3 pominięte (brak archiwalnego v126). Log: `build/v186-check.log`.
Wszystkie dziesięć niezaliczonych testów odtworzono także na XEX-ie v185:
`build/v186-baseline-check.log` i `build/v186-baseline-check-extra.log`.
Dotyczą koszykówki (4), luk pamięci/dekodowanych klatek szarf (4), starej
granicy motywu aktu 5 (1) i limitu cykli callbacku (1).

Test limitu 21 000 cykli nie przechodził również przy wcześniejszym gwizdaniu:
dla 4862/5236 v185 zużywa 22 054/23 000 cykli, a v186 22 102/23 098.
To instrukcyjne koszty py65, a nie pomiar rzeczywistych terminów rastra
z DMA. Pełny zestaw nie jest zielony; ta scena ma zaliczone testy funkcjonalne
i zgodność muzyki. Nie wykonano oceny na fizycznym Atari.

Podglądy po wykonaniu callbacków 6502, z nałożonym PMG:
`build/v186-encounter.gif` i `build/v186-encounter-preview.png`.
Nie są przechwyceniem z emulatora i nie modelują DMA ANTIC.
