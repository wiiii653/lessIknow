# V196 — kontakt dłoni i rytm kozłowania

Środek piłki przesunięto z X=97 do X=84, pod środek dłoni z oryginalnych
klatek. Tor biegnie pionowo między kontaktem przy dłoni a podłogą, po łuku
sinusoidalnym. Oryginalne grafiki postaci i maski piłki są zachowane.

Sekwencja kozłów trwa 374 ticki: szybki 94, szybki 94, wolny 186. Odpowiada
to około 0,47 + 0,47 + 0,93 s. Ten sam zegar wybiera fazę piłki i ramię,
więc przyspieszenie obejmuje obie animacje. Granice sceny i wsadu bez zmian.

Build: `build/visual-prototype-v196.xex`; 298 wierszy, 2560 B kodu głównego.
21 testów koszykówki i finału zaliczonych, w tym niezmienione klatki wsadu
i tablicy porównane z v175. Podgląd programowy (bez emulacji DMA ANTIC):
`build/v196-dribble.gif` i `build/v196-dribble-contact.png`.

V195 z ditheringiem piłki zostało wycofane na polecenie użytkownika.
