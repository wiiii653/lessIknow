# v343 — animowane kropki loadera

Przywrócenie tekstu loadera v330 w v342 zgubiło animację postępu. v343
aktualizuje trzy kropki po inicjalizacji każdego z 50 banków. Napis
`LOADING BANKS` pozostaje nieruchomy, a kropki zajmują stałe pozycje; nie
wyświetlają się bloki ani adresy.

Zachowany tekst:

- `THE LESS I KNOW THE BETTER`
- `LOADING BANKS` z animowanymi kropkami po prawej
- `A\SLOP BY OGNJEN / SILLY VENTURE 2026 WE`

Build stereo: `build/visual-prototype-v343.xex` (1 115 801 B), SHA-256
`495cf1a60c4048df81de69f187df3d70177c80ce0bf5248ba38226cbe9e92ef4`.
Generator zgłosił 298 współdzielonych wierszy i 2560 B kodu głównego;
`git diff --check` przechodzi. Testów, emulatora ani sprzętu nie uruchamiano.
