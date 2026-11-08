# V148 — taniec, szybki wyrzut i pęd powietrza

[ODCZYT] Zgodnie z korektą użytkownika usunięto rozciągnięte przygotowanie
z v147. Od 17950 do 20475 (~12,66 s) grupa tańczy z szarfami: zmiany póz
co półuderzenie, zamiast długiego trzymania kolejnych faz. Pętla dotyczy
tańca; sam wyrzut pozostaje pojedynczy.

| Tick | Obraz |
|---:|---|
| 17950–20474 | Taniec grupy, kompozycje 8/9/35/10 |
| 20475 | Szybkie przykucnięcie, kompozycja 11 |
| 20521 | Wybicie w planie ogólnym od przodu, kompozycja 12 |
| 20568 | Cięcie do kamery nad dziewczyną, kompozycja 13 |
| 20615 | Szybkie zbliżenie ku obiektywowi, kompozycja 14 |
| 20662–20941 | Końcowe zbliżenie z ruchem powietrza i efektami, kompozycja 15 |
| 20942 | Dotychczasowe cięcie do koszykarza |

[ODCZYT] Od przykucnięcia do zbliżenia mija 187 ticków (~0,94 s).
Przywrócono widok wyrzutu z sali i pozostawiono końcowy widok z góry.
W obu planach lotu tło jest spokojne i czarne, bez kratki. Wcześniejszy
taniec korzysta z ilustracji sali. Nie zmieniono granic aktów, głównych
zakresów choreografii ani czterech aktualizacji muzyki na ramkę.

## Pęd na players i missiles

[ODCZYT] W obu planach lotu players 0/3 tworzą wąskie, przesuwające się
w dół smugi powietrza, przeciwne do ruchu bohaterki. Mają biel/cyjan
utrzymywane również po istniejących tickach muzyki. Players 1/2 pozostają
kolorowymi fajerwerkami. Cztery missiles mają normalną szerokość zamiast
podwójnej i rysują czterowierszowe kreski; ich pozycja pionowa zmienia się
co 4 ticki przy trzymanej bitmapie. Smugi i rozkwity są po bokach twarzy.

[ODCZYT] Dane i maski nadal powstają w nieaktywnym PMG. Kopie bitmap,
przygotowanie masek i bezpieczne okno publikacji zachowane. Helper barw
pozostaje niebankowany i reentrant, bez współdzielonego scratcha NMI.
Rysowanie smug zachowuje X na stosie; oryginalny dekoder może przerwać
ten kod, a wrapper przywraca PORTB i rejestry.

## Bilans pamięci

- Nowe kształty wiatru: 128 B, bank loadera 49, `$7F20–$7F9F`.
- Kontroler szarf/efektów: 2237 B (`$5400–$5CBC`), +34 B względem v147.
- Niebankowany helper barw: +21 B; główny kod ma 2515 B i kończy się
  na `$1DD2`, zostawiając 45 B do puli od `$1E00`.
- Kontroler finałowego chłopca: nadal 812 B, przeniesiony do
  `$5CD0–$5FFB`. Między kontrolerami pozostaje 19 B, przed `$6000` tylko 4 B.
- Nadal 36 kompozycji i 64 banki. Nowe banki ani źródłowe ilustracje
  nie były potrzebne. Odzysk netto względem v141: **24 771 B = 24,19 KiB**.

## Walidacja

[ODCZYT] `make check`: **115 testów, 112 zaliczonych, 3 pominięte**
(brak archiwalnego v126), 91,119 s. Testy sprawdzają ruchomy taniec w całym
odzyskanym zakresie, pojedynczy szybki wyrzut w obu planach, brak kratki
w locie, smugi players i ruchome kreski missiles, bezpieczne bufory i
przywracanie wcześniejszych efektów. Wstrzykiwanie NMI dekodera obejmuje
teraz także początek widoku wyrzutu z sali oraz ujęcie z góry.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: **15 331 536
identycznych bajtów** względem v035 przez cały utwór. Bez odsłuchu i testu
na fizycznym Atari. Testy py65 nie ustalają rzeczywistego FPS z DMA ANTIC.

## Wydanie i podglądy

- `build/visual-prototype-v148.xex` i JSON.
- `build/v148-dance-and-launch.gif`: cały zakres tańca i szybkiego wyrzutu.
- `build/v148-fast-launch.gif`: krótki fragment z wyrzutem, callback co 4 ticki.
- `build/v148-dynamic-launch.png`: taniec i oba plany lotu.

GIF-y odtwarzają się jednokrotnie. Paleta i tempo są przybliżone;
nie są nagraniem emulatora ani pomiarem terminów prezentacji.

SHA-256 XEX: `556dd9389fea101ab169bb867cc86e705ce76aab89016524e45fdccb8a7518d2`.
Numerowane wydanie i sprawdzony build roboczy są identyczne bajt w bajt.
