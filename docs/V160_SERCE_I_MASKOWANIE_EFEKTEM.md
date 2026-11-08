# V160 — bijące serce i maskowanie otworu aktywnym efektem

Na życzenie użytkownika usunięto osobną piłkę, która w v158 stale osłaniała
środek niezależnie od pokazywanego efektu. Teraz **sam aktualny obiekt PMG**
ma pełną sylwetkę nad otworem. Nie ma dodatkowej piłki ani wspólnej maski
pod obiektami. Wszystkie cztery players należą do bieżącego efektu.

Z cyklu po Trevora usunięto fajerwerki. Kolejność:

1. Duża obracająca piłka, ponownie cztery płaszczyzny kolorów.
2. Kompaktowa kolorowa piłka.
3. Bijące czerwono-różowe serce z cieniowaniem i jasnym refleksem.
4. BANG/BAM na pełnej komiksowej chmurce.
5. Pełna chmurka z rozchodzącymi się fragmentami.
6. Duża gwiazda i krążące mniejsze gwiazdki.
7. Zwarty podmuch powietrza z wąskimi smugami, bez fajerwerków.
8. Pełny odłamek szkła z barwnymi płaszczyznami i lecącymi fragmentami.

Serce ma osiem faz z dwoma pulsami wielkości oraz zmianą jasności.
Jego kontur, górne wcięcie i refleks są rysowane bezpośrednio do masek
16×32. Minimalna sylwetka nadal przykrywa cały otwór.

W piłkach otwór zasłania piłka, w BANG/BAM sama chmurka, w gwiazdkach
centralna gwiazda itd. Mniejsze cząstki mogą odlatywać, ale główny obiekt
nie odsłania otworu. Fajerwerki wcześniejszego intro i wyrzutu nie są
częścią tej zmiany. Szarfy nadal są wykluczone z cyklu.

Zakres 32909–59085, zmiana trybu co 512 ticków i pętla 4096 ticków bez zmian.
Dithering v159, wcześniejsze sceny, końcowy chłopiec i muzyka pozostają.

## Renderer, priorytet i pamięć

Player 0 nie ma już stałej maski, pozycji lub rozmiaru. Każda z 64 klatek
ma własny 32-bajtowy strumień i metadane. Rodzaj obiektu decyduje, która
płaszczyzna przykrywa środek. W komiksowym wybuchu i szkle pełne tło
obiektu jest na P3, pod napisami/rozjaśnieniami P1/P2. Zachowano rzeczywistą
kolejność priorytetu GTIA. Poprawiono też kolejność składania warstw
w podglądzie programowym, aby P0 był nad P1 itd.

Bank loadera 2:

- `$4000–$41F0`: helper, 497 B, +28 B.
- `$4400–$63FF`: strumienie P1/P2/P3 i missiles, 8192 B.
- `$6400–$693F`: dotychczasowe metadane, 1344 B.
- `$6A00–$6AFF`: dotychczasowe wskaźniki, 256 B.
- `$6B00–$72FF`: dynamiczne maski P0, 2048 B zamiast wspólnego rdzenia 16 B.
- `$7300–$73BF`: pozycje i rozmiary P0, 192 B.
- `$7400–$747F`: wskaźniki P0, 128 B.
- `$7800–$7FFF`: renderer wcześniejszych scen, 2048 B.

[ODCZYT] Zajętość banku 14 705 B, +2380 B względem v159; pozostaje
1679 B luk. Nadal 64 banki i 2546 B głównego kodu z 14 B zapasu.
Odzysk netto względem v141: 13 081 B (12,77 KiB).

Całe PMG przygotowuje się w nieaktywnym buforze, potem zatwierdza
w ograniczonym oknie początku wygaszania. Nie ma chwili z pustą osłoną
podczas przejścia między trybami.

## Walidacja

Test wykonuje wszystkie 64 klatki i sprawdza:

- zgodność każdej z czterech masek i jej pozycji z aktywnym efektem;
- zasłonięcie każdego piksela otworu sumą rzeczywistych masek efektu;
- brak fajerwerków oraz obecność serca i obu jego pulsów;
- priorytet napisów nad chmurką w sprzęcie i podglądzie;
- brak zapisu do aktywnego bufora, powroty do wcześniejszych scen i finału;
- przerwania NMI dekodera i zachowanie PORTB oraz późny VCOUNT.

[ODCZYT] `make check`: 124 testy, 121 zaliczonych, 3 pominięte
(brak archiwalnego v126), 90,686 s.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY:
15 806 592 identyczne bajty względem v035 przez cały utwór.

py65 nie modeluje DMA ANTIC i nie ustala rzeczywistego FPS ani stabilności
rastra na fizycznym Atari. Nie wykonano odsłuchu i testu na sprzęcie.

## Wydanie i podglądy

`build/visual-prototype-v160.xex` i odpowiadający JSON.
`build/v160-beating-heart.gif` — serce; `build/v160-pmg-cycle.gif` — pełny
cykl. `build/v160-active-objects.png` zestawia piłkę, serce, napis i szkło.
Podglądy powstają po callbacku 6502; paleta i tempo są przybliżone,
nie są nagraniem emulatora.

SHA-256 XEX: `1f74fc2fb6533b216d2a18924ee83394fcff62b3009d2f3c2c6e4b043fbab3f5`.
Numerowane XEX/JSON są identyczne z plikami roboczymi dev.
