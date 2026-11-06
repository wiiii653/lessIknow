# V058 — rotator, tunel i ruch piłki

Rotator używa okresowych, czterokrotnie symetrycznych rozet; tunel używa
zakrzywionych pasm i spiralnych fal. Wzory zamykają się w pętli klatek.

Piłka na playerach wykonuje w rotatorze pełny poziomy tor nieskończoności:
pozycje X i Y są wyliczane niezależnie, bez rysowania śladu. Jej obracające
się maski zmieniają powierzchnię z 156 do 352 pikseli PMG, sugerując
oddalanie i przybliżanie. Pociski nadal orbitują wokół piłki. W tunelu
zachowano osobny mały ruch obu osi; test sprawdza zakrycie jego środka.

Granice scen i odtwarzacz pozostają jak w v057. `make check` przeszło 60
testów, w tym tor obu osi, powrót do środka i zakrycie dziury tunelu; po
dodaniu kontroli skali maski uruchomiono także ten test osobno. Pełne
porównanie stereo POKEY z oryginałem dało 8 152 272 identyczne bajty po
jednorazowym wyrównaniu początku. Podglądy są renderem procedur 6502 z
przybliżoną paletą, nie nagraniem z fizycznego Atari.

Wydanie: `releases/visual-prototype-v058.xex`, SHA-256
`549e4b2bc6c42c9331f4685709836fa31a8a98e84f991ef3e0b7a8dcbf276c24`.
