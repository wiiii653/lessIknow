# V174 — czytelny szyld ATARI ARENA

Pierwsze ujęcie chłopca przed areną miało czarne plamy i przezroczyste
fragmenty na napisie. Źródłem błędu była szeroka maska portretu: traktowała
czarne tło źródłowego obrazka jako część chłopca i nadpisywała nim szyld.

Maska wybiera teraz kolorowe składowe postaci oraz ich czarny kontur, zamiast
wypełniać cały wielokąt tła. Klucze wiolinowe i nuty przesunięto nad napis,
aby nie zaciemniały liter ATARI ARENA.

- Podgląd złożonego kadru: `build/v174-arena-sign-preview.png`.
- XEX: `build/visual-prototype-v174.xex`.
- 307 współdzielonych wierszy (limit 309), 2552 B kodu.
- SHA-256: `f9576e668282b94ec598de5c04f55a0e50e578014c07fb09af471bb282979b12`.
- Ticki, granice scen i przydział pamięci bankowej bez zmian.
- Zbudowano; nie uruchamiano testów ani odtwarzania emulatorowego.
