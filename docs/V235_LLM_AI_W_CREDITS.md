# V235 — LLM i AI w credits

Na prośbę autora dodano dwie krótkie linie o sposobie tworzenia dema:

```text
HUMAN VISION / LLM CODE
AI TOOLS / ATARI SOUL
```

Pierwsza jest szóstym wpisem planszy autora, po `MADE WITH OPENAI CODEX`.
Zaczyna się w 54408 i używa nowego wiersza terminala. Druga jest czwartym
wpisem planszy Silly Venture, od 56162. Obie mają dotychczasową animację
pisania i kursor. Ticki wcześniejszych wpisów, początek greetz w 56842,
koniec tekstu w 59085 oraz cała grafika pozostają zachowane.

## Pamięć

38 surowych rekordów tekstowych mieści się w dotychczasowych dwóch
obszarach po 44 B na rekord; drugi kończy się pod $CEEC. Liczba logicznych
slotów (47), wpisów czasu (48) i szerokość/wysokość terminala nie rosną.

Po kompresji zasoby mają 1795 B, o 52 B więcej niż v234. Dodano audytowane
35 B wyłączonego UI $242E–$2450; użyto 12 B. Obszar znajduje się dokładnie
za 96-bajtową tabelą czasu i przed routerem palety $2451. Assert chroni
granicę czasu $242E. Łączna pojemność stagingu wynosi teraz 1818 B.

Scalono dwa już używane, sąsiadujące zakresy $2C81–$2D00 i $2D00–$2E00
w jeden region kopiowania. Oszczędzona instrukcja pętli chunku pozwala
zachować loader 373 B w $3E58–$3FCC; nie wchodzi on na ogon zasobów $3FCE.
Główny kod nadal 2551 B, brak zajmowania luk banków rozszerzenia.

## Weryfikacja

Test terminala sprawdza obie pełne linie w działającym 6502. Test stagingu
sprawdza brak nakładania zasobów na tabelę czasu i router palety.
Podgląd CPU/ANTIC/PMG: `build/ai-credits-v235.png`.

[ODCZYT] Pełna regresja: **174/174 testy**, bez pominięć, 118,6 s.
Atari800 PAL/1088XE, stereo POKEY: **10 847 448 identycznych bajtów**
względem v035, cały utwór. Bez próby na fizycznym Atari.
Numerowane XEX i build roboczy są identyczne; SHA-256:
`53ba615148430ee79a68639cec5ca2e1554e4bf342e1694c6915729b14fa46ee`.
