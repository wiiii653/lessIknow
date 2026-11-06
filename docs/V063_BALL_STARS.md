# V063 — czterokolorowa piłka i gwiazdki

Cztery playery piłki otrzymują cztery różne, nasycone barwy o jasności
`$0A` lub `$0C`, zamiast dwóch jaśniejszych pól. Sąsiednie playery mają
zbliżone barwy, aby sprzętowy podział w środku był mniej wyraźny niż
zakrzywiony szew. Nie usuwa to całkowicie granicy pomiędzy playerami.

Cztery missiles połączono w dwie symetryczne gwiazdki, po dwa pociski na
każdą. Jedna porusza się po elipsie o promieniach 25×14, druga 40×23 jednostek
PMG; ich fazy są przesunięte. Gwiazdki pozostają jasne i zmieniają kolor.
Piłka zachowuje tor ósemki i zmianę skali z v058 oraz zakrywa środek tunelu.

`make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 61 testów OK, w tym
porównanie obu orbit, kształtu pocisków, czterech barw, ósemki i zakrycia
środka tunelu. Pełne porównanie stereo POKEY z oryginalnym v035 w Atari800
dało 8 819 280 identycznych bajtów po jednokrotnym wyrównaniu początku.
Podgląd jest renderem 6502 z przybliżoną paletą, a nie nagraniem z Atari.

Wydanie: `releases/visual-prototype-v063.xex`; SHA-256
`ab1aac7b311c00050a710a34400bf55a1cee421d4e2d77ca5d9477e86df2cc60`.
