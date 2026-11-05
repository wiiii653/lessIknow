# V053 — kompletna korekta zegara muzycznego

V053 zachowuje mapowanie taktów wprowadzone w v052 i koryguje ostatni próg
ujęcia Trevora: zmianę pozy w cichym fragmencie aktu 4. Próg wypada teraz na
granicy taktu 68 (`tick_at_bar(68) = 25429`), zamiast na `start + 4 × 374`.

Wspólna funkcja `tools/music_timing.py` ustawia wszystkie granice muzyczne od
początku utworu według `ceil(n × 373,95555)`. Obejmuje granice aktów, przebitki
cheerleaderek, trening i koszykówkę, wejście i uderzenie Trevora, oraz beat
accenty. Mozaika rytmuje palety w odstępach 186/187 ticków z właściwą fazą PAL.

| Granica | Tick |
| ---: | ---: |
| Takt 24 — taniec | 8975 |
| Takt 32 — kalejdoskop | 11967 |
| Takt 40 — portrety | 14959 |
| Takt 56 — koszykówka | 20942 |
| Takt 64 — wejście Trevora | 23934 |
| Takt 68 — zmiana pozy Trevora | 25429 |
| Takt 72 — uderzenie | 26925 |
| Takt 88 — koniec sceny Trevora | 32909 |
| Takt 160 — koniec utworu | 59833 |

`make all` zbudowało `build/visual-prototype-v053.xex`. Kopia wydania
`releases/visual-prototype-v053.xex` ma tę samą sumę SHA-256:

`65d4f50caa0b5006be459a7a8db3118720ae665b64936ab04c70563cee19ce2d`

Testów automatycznych i pełnego odsłuchu na emulatorze w tej zmianie nie
wykonywano.
