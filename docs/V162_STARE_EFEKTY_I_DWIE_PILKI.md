# V162 — wycofanie nowego cyklu i dwie istniejące piłki Trevora

## Rotator i tunel

Na żądanie użytkownika wycofano nowy zestaw PMG v158–v160: cykl, serce,
nowe gwiazdki, podmuchy i powielone maski. Rotator/tunel we wszystkich
swoich zakresach znów wywołują ten sam oryginalny `tunnel_ball` z wcześniejszych
scen: obracającą się kolorową piłkę i satelity missiles. Ta piłka zasłania
otwór tunelu. Nie ma dodatkowego obiektu osłaniającego ani nowej karuzeli.
Grafiki tła pozostają bez ditheringu, zgodnie z v161.

Kod i testy wycofanego eksperymentu są zachowane wyłącznie w
`docs/archive/pmg_showcase_v160.py` i `docs/archive/test_pmg_showcase_v160.py`.
Nie są importowane przez builder ani odkrywane przez testy produkcji.
Nie zajmują pamięci Atari. Starsze numerowane XEX pozostają zachowane.

## Bitka Trevora

BANG/BAM, chmurki i rozprysk odłamków są zachowane. Co trzeci cios, po
napisie, wypuszcza naprzemiennie:

- dużą piłkę tunelu — w lewo;
- kompaktową piłkę rzutu — w prawo.

Obie wykorzystują istniejące maski. Ten sam 512-bajtowy slot `$5E00–$5FFF`
w każdym banku akcji zawiera dwie fazy dużej piłki oraz dwie kompaktowej.
Nie dodano kolejnych bitmap piłek. Duża używa dwóch par rozstawionych
players; kompaktowa nakłada cztery barwne płaszczyzny w jednym miejscu.
Zachowane missiles nadal dostarczają rozchodzących się odłamków.

Czas efektu 80–135 ticków od ciosu, napisy i same ticki uderzeń bez zmian.
Nie zmieniono timeline’u ani źródeł ilustracji Trevora.

## Odzysk pamięci

[ODCZYT] Bank loadera 2 ma teraz całe `$4000–$77FF` wolne/wyzerowane:
**14 KiB ciągłego obszaru**. Jedyny pozostały payload to dotychczasowy
renderer piłki z danymi `$7800–$7FFF`, 2048 B.

Usunięto 12 657 B zajętości nowego cyklu. Kontroler Trevora wzrósł z 2556
do 2557 B, co w 17 kopiach zajmuje 17 B. Po usunięciu powielonych wpisów
palety, zbędnego bajtu stanu i zastąpieniu tabeli faz obliczeniem zachowano
zgodną animację BANG/BAM i zmieszczono oba kierunki w tym samym slocie.

Odzysk netto względem v161: **12 640 B = 12,34 KiB**.
Łącznie względem v141: **25 721 B = 25,12 KiB**. Nadal 64 banki.
Główny kod pozostaje 2546 B. Trevor kończy się na `$69FC`, z 3 B zapasu
przed danymi od `$6A00`.

## Walidacja i wydanie

Testy sprawdzają wyzerowane 14 KiB, zasłonięcie otworu oryginalną piłką,
oba rodzaje i wszystkie cztery płaszczyzny piłek bitki, przeciwne kierunki,
BANG/BAM, odłamki, nieaktywny bufor PMG, NMI i PORTB. Test późnego VCOUNT
odpowiada znów wcześniejszemu rendererowi piłki aktualizowanemu w blankingu.

[ODCZYT] `make check`: 121 testów, 118 zaliczonych, 3 pominięte
(brak archiwalnego v126), 90,643 s.
[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
15 383 304 identyczne bajty względem v035 przez cały utwór.

`build/visual-prototype-v162.xex` i odpowiadający JSON.
Podglądy: `build/v162-large-left.gif`, `build/v162-small-right.gif`.
Paleta i tempo podglądów po callbacku 6502 są przybliżone; nie jest to
nagranie emulatora ani pomiar FPS. py65 nie modeluje DMA ANTIC.
Bez odsłuchu i testu na fizycznym Atari.

SHA-256 XEX: `26349e9efc35072d335d1f96cf5f54a770e2a5089727fc0b4c982179d1a80dd6`.
Numerowane XEX/JSON są identyczne z plikami roboczymi dev.
