# V064 — BANG Trevora

Usunięto wykrzyknik z glifu G. Dymek rozpoczyna się od mniejszego rozbłysku,
rozrasta się, a następnie znika; w ostatniej fazie cztery osobne missiles
rozchodzą się na boki jako kolorowe gwiazdki. Podobnie jak satelity piłki,
każdy pocisk dostaje osobną pozycję i kształt w pamięci PMG. Odległość
gwiazdek od pięści rośnie podczas fazy rozrzutu.

Kolejne uderzenia wybierają jeden z czterech niewielkich offsetów X/Y. Ten sam
offset jest stosowany do napisu, dymka i późniejszych gwiazdek, dzięki czemu
części efektu pozostają razem. Napis jest pełnej wielkości podczas widocznej
fazy; skaluje się sam rozbłysk.

`make check PYTHON=/tmp/tliktb-girl-venv/bin/python`: 62 testy OK, w tym
kontrola napisu, różnych miejsc, rozchodzenia gwiazdek i powrotu do sceny
tańca. Pełne porównanie stereo POKEY v064 z oryginalnym v035 w Atari800:
8 244 648 identycznych bajtów po jednokrotnym wyrównaniu początku. Nie
zastępuje to odsłuchu. Podgląd GIF pochodzi z renderera 6502; czas jego
klatek jest przybliżony i nie stanowi nagrania z fizycznego Atari.

Wydanie: `releases/visual-prototype-v064.xex`, SHA-256
`6e24e90a0cb8cede78d7b2fcdfcaa14db9335f6e9f43cfe1ccce101b4a603e15`.
