# V100 — krój napisów inspirowany oryginałem

Napisy plazmy korzystają z ręcznie ułożonych, grubszych liter szeryfowych na
siatce GTIA 11. Kolorowe lica i przesunięte krawędzie nawiązują do barwnych,
przestrzennych liter z przekazanego obrazu. Są interpretacją w ograniczonej
rozdzielczości Atari, nie dokładną kopią kroju. Litery pozostają częścią
plazmy: nie dodano czarnego panelu, a maska zmienia tylko odcień piksela.

TAME i IMPALA wyłaniają się kolejno, ale tworzą jeden wiersz. Dodatkowa
rastrowa faza pozwala kolejnym słowom i wierszom wyjść z plazmy stopniowo;
przejście wykonawcy w tytuł oraz stała animacja plazmy są zachowane. Nowe
maski mieszczą się w istniejących bankach; liczba banków się nie zmienia.
Granice plansz i muzyczne ticki pozostają takie same.

[ODCZYT] 70 testów py65 zakończyło się poprawnie, w tym porównanie maski
kolorowych liter, częściowego wyłaniania i ciągłości plazmy pomiędzy planszami.
[ODCZYT] Atari800 PAL, 1088XE, Altirra OS, stereo: po jednokrotnym wyrównaniu
początku zapis rejestrów POKEY był identyczny z v035 dla 6 085 728 bajtów;
porównanie obejmuje cały utwór. [WNIOSEK] Podgląd i test POKEY nie zastępują
oceny czytelności, płynności i odsłuchu na prawdziwym Atari.

`build/visual-prototype-v100-tytul.gif` jest programowym podglądem o
przybliżonych kolorach i tempie. XEX: `build/visual-prototype-v100.xex`;
SHA-256 `d1aef662841f3dce0c66b07422214d44c4a273988a1084194679632da7a0551b`.
