# V187 — duże, wyraźne nuty PMG

Poprzednie znaki zajmowały tylko 8 logicznych pikseli szerokości, a ich
jasność malała przez znaczną część lotu. Na kolorowej arenie były zbyt małe
i za mało czytelne.

V187 podwaja oba wymiary: players mają 16 logicznych pikseli szerokości,
a glify są rysowane w 24 podwójnych wierszach PMG, do 48 linii ekranu.
To czterokrotnie większa powierzchnia znaku. Jasność 14 utrzymuje się przez
33 z 36 faz lotu; dopiero ostatnie trzy fazy wygaszają znak. Barwy tęczy
przeplatają białe błyski. SIZEM=$55 poszerza oderwane ślady pocisków.

Większe nuty szybciej oddalają się od twarzy, a cztery łuki szerzej
rozchodzą się po niebie. Początek toru skorygowano tak, aby powiększony
znak wychodził sprzed ust, zamiast zasłaniać twarz. Dziubek i pierwsza nuta
nadal startują w 4862, a całość kończy się przy dojściu dziewczyny do drzwi
w 5610. Kadry, postacie, skale i tor dziewczyny pozostają z v186.

## Wynik i sprawdzenie

- `build/visual-prototype-v187.xex` i JSON; dev identyczny.
- SHA-256: `1491ff54537d31dfdd8b6999269cd850d3c0321f393827ac8de2a30d7b221a27`.
- Helper PMG 1167 B w $6A00–$6E8E banku loadera 0; do cleanup $6F00
  pozostaje 113 B. Bez nowego banku; main 2552 B, 298 wierszy / 11 480 B.
- 16 testów CPU/grafiki zaliczonych. Nowa regresja kontroluje sprzętowe
  podwojenie szerokości, faktyczną liczbę zapalonych wierszy, jasność 14
  i poszerzone missiles; pozostałe sprawdzają synchronizację, tory,
  wygaszanie przy drzwiach, bufory, maski i niezmieniony spacer v175.
- Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 16 221 456 identycznych
  bajtów względem v035; cały utwór. Tryb AppImage
  `APPIMAGE_EXTRACT_AND_RUN=1`, po 20 s czasu hosta na nagranie.
- Zmienił się tylko bank loadera 0; pozostałe 63 banki są identyczne
  bajt w bajt z v186.
- `build/v187-whistle.gif` i `build/v187-whistle-preview.png`: podglądy
  po wykonaniu callbacków 6502, z PMG, bez modelowania DMA ANTIC.
- Pełnego zestawu nie powtarzano po tej zmianie rozmiaru i kolorów.
  Ostatni wynik (v186) oraz 10 wcześniejszych niezaliczonych testów są
  opisane w `V186_DOMKNIETA_SCENA_SPOTKANIA.md`.
