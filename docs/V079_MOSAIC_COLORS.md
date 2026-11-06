# v079 — kolory rotatora i tunelu

Palety są rozjaśnione względem v076 i przyciemnione względem v077. Gdy para odcieni traci kontrast w ciemniejszej fazie, jasność drugiego koloru jest podnoszona o cztery poziomy. W obu częściach sekwencji zachowano 161 różnych par. Nie zmieniono granic scen ani ruchu piłki.

[ODCZYT] `make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 63 testy OK; sprawdzono obie fazy jasności. Porównanie pełnego utworu `tools/check_playback.py --demo build/visual-prototype-v079.xex --seconds 12`: 8 719 056 zgodnych bajtów stereo POKEY. Nie wykonano odsłuchu na fizycznym Atari.
