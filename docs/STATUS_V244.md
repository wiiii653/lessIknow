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
3. **Niezakomitowane dokumenty sesyjne** (untracked):
   `docs/TIMELINE_MAP.md`, `docs/BANK_MEMORY_FREE_V244.md`,
   `docs/STATUS_V244.md` (ten raport) — do zacommitowania.

## Pamięć

- 64 banki rozszerzenia wszystkie zaalokowane. Wolne w obrazie
  załadowania: ~118 900 B, ale po tytule (tick 3072+) banki 40–47 są
  nadpisywane surowymi klatkami bananów obranych, bank 48 pełni rolę
  stagingu, a 3–10 przechodzi na surowe — **realnie dostępne
  ok. 63 300 B ≈ 61,9 KiB** (raport: `docs/BANK_MEMORY_FREE_V244.md`).
- Kod główny: `$1400–$1DFC` (2557 B), wolne **3 B przed pulą wierszy**
  `$1E00` — każdy dalszy element unbanked wymaga refactoru.
- Szczelina: wg notatek przed `$4B80` w banku 1 (hero) ma być wolny
  przeskok; pomiar z XEX-a v244 pokazuje tam treść. Przy planowaniu
  nowych danych w banku 1 tę mapę trzeba najpierw odświeżyć (baza:
  `docs/BANK_MEMORY_FREE_V244.md`).
- Rezerwowane po tytule (nie zajmować): banki 40–48, `$4A00–$53FF`
  banku 39, `$7800–$7FFF` banku 2, strefy fireworks 40/41.

## Plan przed SV

1. Zacommitować dokumenty sesyjne; odnotować v244 w AGENTS.md.
2. Podjąć decyzję 5C/5D (zrobić albo formalnie odpuścić).
3. Uruchomić demo na fizycznym 1088XE w konfiguracji SV (PAL, 1 MB,
   stereo POKEY) i odsłuchać cały przebieg.
4. (Opcja) Pomiar realnych FPS na sprzęcie — dotąd mierzalne tylko
   cykle CPU na py65.

## Pliki pomocnicze z kontroli dnia

- `docs/TIMELINE_MAP.md` — mapa ujęć w m:ss + rotatory A–D.
- `docs/BANK_MEMORY_FREE_V244.md` — raport wolnego per bank.
- `docs/GREETZ_I_CREDITS.md` — treść creditów (zacommitowana).
