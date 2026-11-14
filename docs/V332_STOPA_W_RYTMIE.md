# V332 — ruch stopy w finale

Leżący chłopak porusza czubkiem stopy co beat, w takcie zegara playera.
Kołysanie przesuwa mały pikselowy wycinek o jeden wiersz obrazu w górę i
z powrotem. Działa bez kopiowania pełnej klatki, dodatkowych banków i zmian
timeline’u. Kontroler finału ma 698 B; rutyna stopy zajmuje 117 B w wolnej
szczelinie banku 49 przed tablicami orbity.

Build stereo: `build/visual-prototype-v332.xex` oraz JSON obok. Ma 298
współdzielonych wierszy i 2560 B kodu. SHA-256: `be6837b553940ddb1d4a0826961c679f892ed4c12c2d15c1945d3d5b56f2a053`.
Paczka: `build/visual-prototype-v332-stereo.zip`.
Nie uruchamiano testów ani emulatora;
v332 nie był sprawdzony na fizycznym Atari. Ostatnim potwierdzonym
sprzętowo pozostaje v330.
