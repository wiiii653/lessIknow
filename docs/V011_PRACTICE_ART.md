# Trzy ujęcia treningu — v011

[ODCZYT] Nowa grafika w stylu `act1_school_court_boy.png`: zbliżenie
koszykarza (5984–6980), rzut (6981–7977), dziewczyny przy drabinkach
(7978–8975). Taniec nadal zaczyna się na 8976. Każde ujęcie jest statyczną
ilustracją 160×64 wyświetlaną w 192 liniach. Wyłączono dawną piłkę PMG.
Pozostałe sceny zachowano po przeglądzie; główna niespójność dotyczyła
prostych geometrycznych postaci treningu.

## V2/V3

[ODCZYT] Wszystkie trzy ujęcia mieszczą się razem w dotychczasowym
8 KiB obszarze na końcu banku 8. Bufory i zasady ochrony PORTB jak w v010.

## V6

[ODCZYT] 21 testów przeszło. Atari800 PAL/1088XE, stereo POKEY:
6 776 136 identycznych bajtów rejestrów względem v035 (~1887,5 s emulacji),
cały utwór objęty porównaniem. Brak testu na fizycznym Atari i odsłuchu.

## Grafika i sposób przygotowania

Wbudowany image_gen; referencja stylu: `assets/art/source/act1_school_court_boy.png`.
Zapisany oryginał: `assets/art/source/act1_practice_storyboard_v011.png`.
Konwersja: ImageMagick, point sampling 160×192, najbliższy kolor z palety Atari.

Prompt:
Use attached image solely as exact visual style reference. Create a SINGLE storyboard contact sheet with three equal horizontal landscape panels stacked vertically, no gutters or text. Each panel aspect ratio 5:3. Retro Atari pixel illustration same sophisticated comic face design as reference, natural teenage athletic proportions NOT chibi, NOT stick figures, bold black silhouettes, only black, bright cyan, hot magenta and peach palette. Flat clean pixel shapes no gradients, compose to survive 160x64 logical pixel reduction. Panel top: cinematic waist-up close-up of handsome dark-haired school basketball player holding basketball at chest, focused expression, cyan jersey, gym windows behind. Middle: dynamic medium shot of basketball player releasing jump shot toward visible hoop at upper right, another player at left, natural anatomy, detailed gym architecture, strong readable silhouettes. Bottom: medium shot of two teenage girls in modest sportswear stretching beside wooden gym wall bars, one overhead side stretch and other leg stretch, natural faces like reference, floor and window depth. Same coherent gym, graphic polish and palette in all panels, no text or panel labels. Output the full contact sheet as one image.
