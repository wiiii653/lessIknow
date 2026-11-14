# V335 — nieruchoma stopa w finale

Wycofano animację stopy i dodatkowy helper w luce banku 49. Ostatnia scena
wraca do statycznej grafiki chłopaka z v330. Poprawka serca i panoramy z
v333–v334 pozostaje.

Build stereo: `build/visual-prototype-v335.xex`; SHA-256:
`7145dd1ec6b1bccc7c5121392bb11b0da9ea676877c89432b6fde44030873f5d`.
Build zachowuje 298 współdzielonych wierszy i 2560 B kodu. Nie uruchamiano
testów, emulatora ani Atari; ostatnim potwierdzonym sprzętowo pozostaje v330.

Ruch stopy nie zużywał wolnego banku: jego 117 B leżało w luce już
przydzielonego banku. Nie powinien też wpływać na loader, bo helper jest
wywoływany dopiero w finale. Produkcyjny `loading_screen.py` pokazuje stały
napis `LOADING BANKS`; animowane kropki są w osobnym narzędziu diagnostycznym
`build_init_trace_high.py`.
