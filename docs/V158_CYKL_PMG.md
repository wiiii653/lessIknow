# V158 — cykl efektów PMG po Trevora

Od końca bitki, tick 32909, do wejścia finałowego chłopca w 59085,
rotator/tunel prezentują kolejno:

1. Dużą obracającą piłkę tunelu.
2. Mniejszą piłkę rzutu z kolorowymi panelami.
3. Miejskie fajerwerki.
4. Komiksowe BANG/BAM.
5. Rozchodzące się i kurczące chmurki.
6. Krążące gwiazdki finału.
7. Pęd powietrza i fajerwerki wyrzutu.
8. Rozprysk odłamków tablicy.

Każdy tryb trwa 512 ticków playera (około 2,57 s); pętla 4096 ticków
(około 20,54 s). Fazy zmieniają się co 16 ticków. Szarfy nie są częścią
cyklu. Nie zmieniono granic aktów, muzyki ani obrazów tła; dodatek nie
zastępuje brakujących scen fabularnych i plansz credits/greetz.

## Zasłonięcie środka

Player 0 pozostaje małą, pełną piłką na środku obrazu, również podczas
zmiany trybu. Zasłania cały otwór tunelu niezależnie od pozostałej animacji.
Pozostałe trzy players i cztery missiles pokazują efekty. Kształty źródłowe
są dopasowane do tego budżetu: duża piłka ma trzy warstwy barw zamiast czterech,
a napisy używają kompaktowych glifów. Źródła piłek, fajerwerków, chmurek,
wiatru i gwiazdek pochodzą z istniejących efektów; to warianty ich inscenizacji.

Całe PMG przygotowuje się w nieaktywnym buforze `$08`/`$88`. Dopiero
w VCOUNT 124–127 następuje publikacja kompletnego obrazu i rejestrów.
Stary obraz pozostaje widoczny podczas przygotowania i oczekiwania.

Wcześniejszy rotator aktu 2 i przebitka po wyrzucie zachowują oryginalną
piłkę v150. Wejście finału i powroty do wcześniejszych scen odtwarzają
właściwe maski i ustawienia.

## Pamięć

Audyt referencji potwierdził, że stare artwork/kod `trevor_awakens` w banku
loadera 2 nie renderowały już Trevora: jego produkcyjny kod używa banków
polished 24–39 i 49. Bank 2 był wywoływany tylko dla helpera piłki `$7800`.
Ten helper pozostał; po Trevora przekierowuje do nowego renderera.
Historyczny generator pozostaje jako `legacy_bank()`; źródła i stare
numerowane XEX nie są usunięte.

- `$4000–$41D4`: renderer cyklu, 469 B.
- `$4400–$63FF`: 64 klatki masek, 8192 B.
- `$6400–$693F`: metadane pozycji, rozmiarów i kolorów, 1344 B.
- `$6A00–$6AFF`: tablice adresów, 256 B.
- `$6B00–$6B0F`: nieprzezroczysta maska środka, 16 B.
- `$7800–$7FFF`: dotychczasowy renderer wcześniejszych scen, 2048 B.

[ODCZYT] Bank zajmuje 12 325 B zamiast 14 881 B, odzysk 2556 B.
Nadal 64 banki, main 2546 B z 14 B zapasu. Netto względem v141:
15 461 B (15,10 KiB). Dane/kod pozostałych banków nie rosną.

## Walidacja

Test wszystkich 64 klatek sprawdza kolejność trybów, pełną zgodność masek
players i missiles z danymi, stały rdzeń i zasłonięcie każdego piksela
centralnego otworu tunelu. Osobne testy obejmują nieaktywny bufor, przejścia
trybów, wcześniejsze sceny i finał, późny VCOUNT ze sztucznym zatrzymaniem
CPU oraz rzeczywiste wstrzykiwane NMI dekodera i przywracanie PORTB.

[ODCZYT] `make check`: 122 testy, 119 zaliczonych, 3 pominięte
(brak archiwalnego v126), 90,811 s.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
14 202 576 identycznych bajtów względem v035, objęty cały utwór.
Bez odsłuchu i testu na fizycznym Atari. py65 nie modeluje DMA ANTIC
ani rzeczywistego FPS; testy nie ustalają stabilności rastra na sprzęcie.

## Wydanie

`build/visual-prototype-v158.xex` i JSON.
`build/v158-pmg-cycle.gif` pokazuje pełną pętlę. `v158-cycle-a.png`
i `v158-cycle-b.png` zestawiają osiem trybów. Podglądy po callbacku 6502,
z przybliżonym tempem/paletą; nie są nagraniem emulatora.

SHA-256 XEX: `41bf7d50144ba3737ceda6c9edc9ac331b0bc4482e5bf420b699c28e34be450d`.
Numerowane pliki XEX/JSON są identyczne z roboczym dev.
