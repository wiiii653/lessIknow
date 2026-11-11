# V253 — napis podczas wczytywania

[ODCZYT] Po pierwszej inicjalizacji oryginalnego playera, przed jego
pierwszym bankiem muzycznym, XEX tworzy ekran tekstowy ANTIC 2:

```
NOW LOADING ATARI XE DEMO
SILLY VENTURE 2026 WE
OGNJEN 2026
```

Dane ekranu `$0600–$0677`, display list `$0700–$070A`, inicjalizacja
`$0780–$07BC`; obszary są tymczasowe i później nadpisuje loader OS RAM.
Rejestry i ich cienie OS ustawiane są przed kopiowaniem banków. W playerze
v035 instrukcję wyłączającą DMA przy KAŻDYM kolejnym kopiowaniu oryginalnego
banku zastąpiono trzema NOP, dzięki czemu napis pozostaje widoczny także
podczas kolejnych INIT. Pierwszy INIT nadal wyłącza DMA przed konfiguracją
nowego ekranu. Nie zmienia to danych muzyki ani granic scen.

[ODCZYT] Test ładowania sprawdza kolejność segmentów i INIT, tekst, rejestry,
cienie oraz zmienioną instrukcję. Nie wykonano wizualnej obserwacji ekranu
w emulatorze ani próby na fizycznym Atari; test CPU nie modeluje ANTIC DMA.

[ODCZYT] Atari800 PAL/1088XE, Altirra OS, stereo POKEY: 16 080 048
bajtów identycznych z v035; porównanie obejmuje cały utwór. Emulator
uruchomiono z rozpakowanego AppImage, bez FUSE.

[ODCZYT] `make check PYTHON=/tmp/tliktb-fix-venv/bin/python`: 196/196
przypadków zaliczonych, bez pominięć; 148,545 s.
