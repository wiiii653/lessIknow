# V282 — paleta scen, hali i ekranu ładowania

Pierwsza sekwencja szkolna używa w całym ujęciu tej samej palety co
zatwierdzony kadr: czerń, przygaszony róż, stalowy błękit i brzoskwinia.
Próbki RGB po podglądzie odpowiadają dokładnie kolorom z referencji:
`#000000`, `#9D5058`, `#426FA7`, `#DE988A`. Paleta Atari `$38/$88/$2C`
obejmuje także początkowe ujęcie, panoramę oraz reakcje chłopca.

Hala ma oddzielną paletę GTIA `$38/$68/$2A` — cieplejszą i ciemniejszą.
Zachowuje pierwotny podział kolorów źródłowej grafiki, więc stroje, parkiet,
ściany i piłka pozostają czytelne. Ustawienie obejmuje grupowe ujęcia taneczne,
trening i koszykówkę.

Ekran ładowania podaje tytuł, Atari XE stereo, produkcję Ognjena i Silly
Venture 2026. Pozostaje informacja o ładowaniu banków. Tło jest ciemnogranatowe,
a tekst brzoskwiniowy; cienie OS i rejestry GTIA mają te same wartości.

Stereo XEX dla AVG: `releases/less-i-know-demo-release-019-stereo.xex`
(935 281 B, SHA-256 `10f0c7cc2ed7b67b22e01cbb658195381b35b772f75708775f3c2715953a1752`).
Metadane: `releases/less-i-know-demo-release-019-stereo.json`.
Kompaktowy late-start staging obejmuje teraz także `$07E5–$07E8`, zgodnie
z bieżącym segmentem niskiej pamięci.

[ODCZYT] Kompilacja: 298 wspólnych wierszy, kod główny 2560 B. Renderowane
podglądy scen szkolnej i hali zostały sprawdzone; pierwszy zawiera dokładnie
cztery wskazane kolory, a hala trzy rozróżnialne ciepłe barwy oraz czerń.
Finalny XEX ma 0,892 MiB.

[OGRANICZENIE] Nie uruchamiano testów automatycznych ani pełnego porównania
muzyki. Ten build nie był sprawdzony na fizycznym Atari.
