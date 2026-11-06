# V057 — taniec cheerleaderek

[ODCZYT] Nowa sala i cztery pozy cheerleaderki używają czterokolorowej
konwersji do ANTIC E. Źródła: `assets/art/source/act1_gym_dance_v056.png`
i `assets/art/source/act1_cheer_dance_v056.png`. Kompozytor dodaje czarny
obrys i cienie, a dla trzech postaci wybiera fazy póz `0, 1, 3`. Każda poza
trwa 32 ticki muzyki. Granice wejścia solo, duo, trio i kalejdoskopu pozostają
takie jak w v055. Dwanaście gotowych klatek nadal zajmuje sześć banków.

[ODCZYT] Cztery playery i cztery missiles tworzą przesuwające się akcenty na
uderzeniach. Każdy player ma oddzielny kolor; pocisk używa jego koloru.
Pomocnik PMG zajmuje 228 bajtów w `$AF00–$AFE3`, nie narusza obszaru kopii
klatek i odtwarza swoją zawartość po innych scenach.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 60 testów OK,
w tym testy czterech faz trio, kolorów i ruchu PMG, kopii nieaktywnego bufora,
muzycznych NMI i powrotów do innych scen. Pełne porównanie stereo POKEY z
oryginalnym v035 w Atari800 dało 7 890 552 identyczne bajty po jednokrotnym
wyrównaniu początku. Pomiar nie zastępuje odsłuchu.

[ODCZYT] Porównanie v055 i v057 w instrumentowanym Atari800 7.2.1, PAL,
1088XE, Altirra OS i stereo: 14 958 klatek do ticku 59832; licznik muzyki i
cztery próbkowane rejestry POKEY są zgodne w każdej parze. Poza odcinkiem
tańca i bezpośrednim przejściem do mozaiki skróty klatek są zgodne. Podgląd
GIF jest renderem procedury 6502, z przybliżoną paletą, a nie nagraniem
ekranu emulatora ani fizycznego Atari.

Wydanie: `releases/visual-prototype-v057.xex`; SHA-256
`aa87e68ffb919c69491fbcd55bc338f6f91344aef95659ae4a7f7152a3379645`.

## Grafiki źródłowe

Obie grafiki wygenerowano wbudowanym narzędziem imagegen, używając istniejącej
planszy treningu jako wzorca stylu; plansza tańca była dodatkowym wzorcem póz.
Prompty:

- „Use case: illustration-story. Asset for an Atari 8-bit demo animation sprite sheet. Image 1 is the existing four-pose sheet (composition reference); image 2 is the gym scene (art direction reference). Produce a clean 2 by 2 grid of four consecutive full-body poses of ONE SAME young adult blonde/dark blonde school cheerleader, dancing with two large pom-poms. European comic illustration, credible anatomy, bold confident ink, mature appealing face, no manga, matching the gym scene's 1980s European graphic novel style. Four clearly different readable action poses with arms and legs moving in a coherent dance sequence; head, body proportions, costume and placement consistent for frame-by-frame animation. Each panel isolated on pure solid black, no borders or text, exact 2x2 equal grid, each full body centered with generous black margins and all pom-poms within its own cell. Use only solid black, bright magenta, cyan, and warm peach flat color fills; no other colors or gradients, bold large shapes designed for severe reduction to 48 by 144 pixels. Pink and cyan uniform, blonde hair suggested by warm peach because of the four-color constraint; crisp uncluttered silhouette.” Wynik jest w pipeline skalowany do 48×128, aby animowane fragmenty mieściły się w obszarze częściowej kopii.
- „Use case: illustration-story. Asset: empty school gym background for an Atari 8-bit animated scene, referenced image is the style and location. A symmetrical wide shot of the SAME school gym from the reference, seen straight on with clear basketball hoop, high wide windows, beams, polished wooden basketball court with restrained perspective. Reserve the middle foreground for three dancers to be composited later, no people, no silhouettes. European comic book artwork with strong clean black inking, restrained flat geometric shapes, bright cyan windows, magenta wall accents and warm peach floor, black shadows. Exactly four flat colors: black, cyan, vivid pink, warm peach. No gradients, text, logos, or tiny textures. Bold graphic architecture, readable when reduced to 160 by 192 Atari pixels. Entire image is one uninterrupted scene, no panels.”
