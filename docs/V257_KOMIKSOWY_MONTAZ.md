# V257 — fabularne przebitki w istniejącym montażu

[ODCZYT] W odpowiedzi na prośbę o domknięcie historii do istniejącego
montażu dodano cztery kompozycje z istniejących źródeł postaci:

- 37884–39378: mozaika twarzy Trevora;
- 40875–42370: trzy panele — Trevor, dziewczyna i chłopiec;
- 42371–43866: konfrontacja Trevora i koszykarza;
- 46858–49849: zbliżenie Trevora przed ujęciem pokonanego chłopca.

W każdym z tych okien statyczny kadr komiksowy jest przeplatany co 256
ticków z dotychczasowym ruchomym rotatorem/tunelem. To komiksowe przebitki,
a nie nowa animacja walki. Pozostają zatwierdzone 13 ciosów z piłkami,
oczy dziewczyny 39379–40126 oraz chłopiec i terminal od 49850. Żaden z
istniejących ticków cięć ani zegar muzyki nie został przesunięty.

[ODCZYT] Grafiki zajmują sloty 56–59 organicznego tunelu w loader banku 17;
poza scenami sloty 56–63 przekierowano na 52–55. Zastępuje to cztery
kolejne fazy tunelu, oprócz czterech wykorzystanych wcześniej na oczy.
Bank 2: selektor scen `$7600–$7647`, publikacja i bramka PMG `$7700–$772D`;
rozszerzony selektor oczu `$7500–$7550`. W nowych panelach piłka PMG jest
wyłączana podczas blankingu, aby nie zasłaniała twarzy; po powrocie do
efektu wraca dotychczasowy renderer piłki. Kod główny bez wzrostu,
jedna zmiana adresu JSR; 64 banki. Podgląd callbacków CPU z przybliżoną
paletą: `build/v257-story-preview.png` — nie jest nagraniem emulatora.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 16 377 408
bajtów identycznych z v035 przez cały utwór. Bez oceny A/V na sprzęcie;
testy py65 nie modelują ANTIC DMA ani FPS.

[ODCZYT] `make check PYTHON=/tmp/tliktb-fix-venv/bin/python`: 203/203
przypadków, bez pominięć; 152,000 s.
