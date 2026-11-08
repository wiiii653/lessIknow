# V163 — Trevor odbija gotową piłkę z satelitami

## Obraz i zachowanie

Co trzeci cios Trevora po napisie wypuszcza kompletną piłkę z rotatora:
16 faz obrotu, oryginalny cykl czterech kolorów i obie orbity satelitów,
każda z pary missiles. Cały efekt przesuwa się razem ku bliższej krawędzi.
Lewa dłoń (4) odbija w lewo, prawa (2) w prawo; kierunek wynika z pozy,
nie z naprzemiennego numerowania ciosów.

[ODCZYT] BANG/BAM pozostają przez pierwsze 80 ticków. Lot zajmuje
niezmienione ticki wieku 80–135. Pozostałe ciosy zachowują rozchodzące się
chmurki i odłamki. Nie zmieniono ticków ciosów, granic scen ani muzyki.
Piłka zaczyna ze środkiem x=48 lub x=112 w logicznym kadrze 160 pikseli,
następnie przesuwa się o jeden piksel na tick. Obrót i satelity nadal
korzystają z ticka playera. Wcześniejsze i późniejsze rotatory/tunele
zachowują dotychczasowy tor i osłonę otworu, bez nowej karuzeli PMG.

## Wspólny renderer i sprzęt

Nie skopiowano kolejnych masek. Kontroler Trevora przez istniejący
niebankowany trampoline wywołuje adapter w banku loadera 2, który uruchamia
oryginalny `tunnel_ball` pod `$7800`. Zagnieżdżone wywołanie przywraca PORTB,
a kontroler przywraca operand banku i adres docelowy trampoline.

Adapter zachowuje pozę, przekazuje specjalną pozę 96 i podpisane
przesunięcie x w `$83EA`. Oryginalny renderer dodaje to przesunięcie do
pozycji piłki oraz satelitów przed zapisaniem ich do GTIA, w swoim
zwykłym oknie blankingu. Po powrocie adapter odtwarza pozę Trevora.

[ODCZYT] Rejestry HPOS `$D000–$D007` są tylko do zapisu; odczyt z tych
adresów zwraca zatrzaski kolizji GTIA. Usunięto próbę odczytywania pozycji
po publikacji. Regresja wykonuje oba kierunki z modelem, który odrzuca
każdy odczyt tych adresów przez CPU. Zapobiega to sytuacji, w której
prosty model RAM w py65 przepuszcza błędny kod sprzętowy.

## Pamięć

[ODCZYT] Usunięto 16 kopii po 512 B masek (`$5E00–$5FFF` banków akcji
24–39): 8192 B odzysku. Bank 49 pozostaje nietknięty w tym obszarze,
ponieważ mieści kontroler finałowego chłopca.

Kontroler Trevora zmalał z 2557 do 2466 B: 91 B × 17 kopii = 1547 B.
Kończy się na `$69A1`, pozostawiając 94 B przed `$6A00`.
Adapter w banku 2 zajmuje 44 B (`$4000–$402B`). Wolne i wyzerowane
`$402C–$77FF` daje 14 292 B ciągłego obszaru; oryginalny renderer z danymi
nadal zajmuje 2048 B pod `$7800–$7FFF`. Dodatkowa obsługa przesunięcia
mieści się w istniejącym wyrównaniu tego helpera.

Dodatkowy odzysk netto względem v162: **8192 + 1547 − 44 = 9695 B
(9,47 KiB)**. Łącznie względem v141: **35 416 B (34,59 KiB)**.
Nadal 64 banki; main nadal 2546 B, 14 B przed `$1E00`.

## Weryfikacja

Testy porównują wszystkie cztery płaszczyzny gotowej piłki z maskami
rotatora, pozycje i pięciowierszowe maski obu satelitów, kierunki obu dłoni,
BANG/BAM i chmurki pozostałych ciosów. Sprawdzają przywrócenie PORTB,
powrót przez NMI muzyki, brak odczytów HPOS, zasłanianie otworu tunelu
i wykonanie zapisu PMG w oknie przed kolejnymi satelitami.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
13 910 544 identyczne bajty względem v035, około 3874,9 s emulacji,
obejmujące cały utwór. To porównanie danych rejestrów, bez odsłuchu.

Podglądy `build/v163-rebound-left.gif`, `build/v163-rebound-right.gif`
i `build/v163-complete-rebounds.png` wykonano po callbackach 6502.
Ich kolory i tempo są przybliżone; nie są nagraniem emulatora.
[WNIOSEK] Wyniki py65 i porównania POKEY nie potwierdzają rzeczywistego
FPS, terminów DMA ANTIC ani stabilności rastra na fizycznym Atari.
Bez testu na fizycznym sprzęcie.

[ODCZYT] `make check`: 122 testy w 90,000 s, 119 zaliczonych,
3 pominięte z powodu braku archiwalnego v126. Kontrola mapy potwierdza
wyzerowanie 16 slotów masek i wolnego obszaru banku 2.

Wydanie: `build/visual-prototype-v163.xex` i odpowiadający JSON;
oba są identyczne z przetestowanymi plikami roboczymi dev.
SHA-256 XEX: `a670abbb762a11e11d8747c7bb42e86031a35d38389c090e3790cd5833b14db0`.
