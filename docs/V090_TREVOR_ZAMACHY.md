# V090 — zamach przed każdym ciosem

Trevor podnosi tę rękę, którą za chwilę uderzy: do istniejącej pozy zamachu
dodano jej lustrzaną klatkę, dopasowaną do lustrzanej klatki ciosu. W
pierwszych fazach ciosu sylwetka wykonuje także niewielki ruch w kierunku
pięści, co wzmacnia wrażenie pchnięcia. Czasy uderzeń, BANG i początek
rozprysku pozostają takie jak w v089.

W 16 bankach faz tunelu miejsce kopii pierwszej planszy wstępu zajmuje teraz
nowa klatka zamachu; oba obrazy spokojnego wstępu oraz kod odtwarzający
umieszczono w ostatnim wolnym banku rozszerzenia. Demo wykorzystuje wszystkie
64 banki 16 KiB konfiguracji 1 MB. Kod sterujący przywraca PORTB po każdej
scenie i po przerwaniu muzycznym.

[ODCZYT] 68 testów py65 zakończyło się poprawnie, w tym sprawdzenie właściwego
zamachu bezpośrednio przed czterema kolejnymi ciosami, póz uderzenia,
rozprysku, przełączenia banków i powrotu do pozostałych scen.
[ODCZYT] Atari800 PAL, 1088XE, Altirra OS, stereo: po jednokrotnym wyrównaniu
początku zapis rejestrów POKEY był identyczny z v035 dla 6 193 728 bajtów;
porównanie obejmuje cały utwór. [WNIOSEK] Nie zastępuje to osobnego odsłuchu
ani oceny płynności na prawdziwym Atari.

`build/visual-prototype-v090-trevor.gif` to programowy podgląd display listy
i PMG o przybliżonych kolorach i tempie. XEX: `build/visual-prototype-v090.xex`;
SHA-256 `350e90212aca6a970dbd41676c993c0b0e809e68ec6c4d6b752a61dd289eabc3`.
