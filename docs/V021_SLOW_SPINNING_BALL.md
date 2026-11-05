# v021 — jeden powolny lot i obrót piłki

[ODCZYT] Ujęcie nadal trwa od ticka 6981 do 7978. Lot wykorzystuje
cały 16-bitowy czas od początku ujęcia: faza = (tick − 6981) >> 3,
0–124. Piłka leci raz, od dłoni do obręczy, przez około pięć sekund.
Nie ma powtarzania, opadania ani kolejnego odbicia w tym ujęciu.

[ODCZYT] Rozmiar wzrósł z 8×16 do 16×32 pikseli logicznych:
playery mają podwójną szerokość, maska ma 16 podwójnych linii.
Osiem klatek zmienia położenie zakrzywionego szwu, równikowego szwu
oraz kolorowych paneli. Obraca się geometria maski, obok niezależnej
zmiany czterech kolorów GTIA. Pociski nadal rysują kolorowe krople.

## V1 / V6 — sprawdzenie

[ODCZYT] 34 testy OK: ruch przez całe ujęcie, brak restartu po 256,
512 i 768 tickach, nowy rozmiar i osiem różnych masek obrotu.
Sprawdzono również zachowanie tła i odtworzenie PMG sceny tańca.
W Atari800 PAL `-1088xe` zweryfikowano dziewięć faz od początku do
ostatniego ticka ujęcia, następne ujęcie oraz powrót do tańca.
Fazy na zrzutach zgadzają się z pełnym czasem od początku rzutu.

[ODCZYT] Pełne porównanie stereo POKEY z oryginałem:
8 980 704 identyczne bajty, około 2501,6 s emulacji.

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v021.xex --seconds 12
```

[ZAŁOŻENIE] Pozostaje kontrola na fizycznym Atari. GIF przybliża kolory PAL
oraz proporcje pikseli: `build/v021-slow-spinning-ball.gif`.
Wcześniejsze XEX-y zachowano.
