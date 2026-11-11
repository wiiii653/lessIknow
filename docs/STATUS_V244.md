# STATUS projektu — stan na v244 (10.11.2026)

Demo: „The Less I Know The Better" na Silly Venture. Ostatni commit
`e6cd188 Add v244 demo build` (9.11.2026). Pełny zestaw testów zielony:
189/189; porównanie dźwięku stereo POKEY z oryginałem zgodne co do bajta
(10 589 472 B). Testu na fizycznym Atari jeszcze nie wykonano.

## Gotowe etapy

| Część | Stan |
|---|---|
| Intro (plazma, Żuraw, fajerwerki) | zrobione (V140–V149) |
| Akt 1 (spotkanie, gwizd z nutami PMG) | zrobione (V176–V188) |
| Akt 2 (taniec szarfą, solówka, rzut z sercem) | zrobione (V142–V173, V233) |
| Akt 3 (koszykówka, wsad, rozbicie tablicy) | zrobione (V156–V196) |
| Akt 4 (Trevor, dymki BUM/BAM) | zrobione (V168, V190–V192) |
| Akt 5 (banany kiść/obrany, tunel z piłką) | zrobione (V236/V239/V243/V244) |
| Po Trevorze (dyrektor tuneli/bananów) | zrobione (V231/V240) |
| Outro (terminal z credits/greetz, finał, fade) | zrobione (V216–V242) |

## Otwarte punkty przed SV

1. **Sceny 5C „Trevor Mosaic" i 5D „Eyes"** — zaplanowane, nigdy nie
   zaimplementowane. Odcinek ok. 3:30 pokazuje ciągły tunel organiczny.
   Decyzja: robić przed SV czy zostawić tunel jako zastępczy (obecnie
   wygląda spójnie dzięki V194/V231).
2. **Test na fizycznym Atari 1088XE** — dotąd tylko py65 (bez modelu
   DMA ANTIC) i Atari800 (porównanie audio z v035 i próby rastrowe).
   Trzeba potwierdzić FPS i stabilność rastrową na sprzęcie przed SV.

## Pamięć

- 64 banki rozszerzenia wszystkie zaalokowane. Wolne zakresy w obrazie
  startowym: **119 226 B ≈ 116,4 KiB**; po odjęciu całych banków 40–48
  (overlay tytułu/stagingu) i 3–10 (surowe banany) konserwatywna pula poza
  tymi overlayami wynosi **61 497 B ≈ 60,1 KiB**. To rozproszone luki,
  nie jeden ciągły obszar; szczegóły i ograniczenia:
  `docs/BANK_MEMORY_FREE_V244.md`.
- Kod główny: `$1400–$1DFC` (2557 B), wolne **3 B przed pulą wierszy**
  `$1E00` — każdy dalszy element unbanked wymaga refactoru.
- Szczelina: wg notatek przed `$4B80` w banku 1 (hero) ma być wolny
  przeskok; pomiar z XEX-a v244 pokazuje tam treść. Przy planowaniu
  nowych danych w banku 1 tę mapę trzeba najpierw odświeżyć (baza:
  `docs/BANK_MEMORY_FREE_V244.md`).
- Rezerwowane po tytule (nie zajmować): banki 40–48, `$4A00–$53FF`
  banku 39, `$7800–$7FFF` banku 2, strefy fireworks 40/41.

## Plan przed SV

1. Podjąć decyzję 5C/5D (zrobić albo formalnie odpuścić).
2. Uruchomić demo na fizycznym 1088XE w konfiguracji SV (PAL, 1 MB,
   stereo POKEY) i odsłuchać cały przebieg.
3. (Opcja) Pomiar realnych FPS na sprzęcie — dotąd mierzalne tylko
   cykle CPU na py65.

## Pliki pomocnicze z kontroli dnia

- `docs/TIMELINE_MAP.md` — mapa ujęć w m:ss + rotatory A–D.
- `docs/BANK_MEMORY_FREE_V244.md` — raport wolnego per bank.
- `docs/GREETZ_I_CREDITS.md` — treść creditów (zacommitowana).
