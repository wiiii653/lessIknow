# V360 — twarz tancerki i wyprostowana postawa

Punkty odniesienia to tancerki ze wstążkami i dziewczyny przy drabinkach.
Zbliżenie korzysta z twarzy i loków z `act2_ribbon_dancer_v136.png`,
przeniesionych na cztery kolory areny. Jasny brzeg uśmiechu odtworzono
na siatce docelowej. Szyja jest jasna i osadzona nad barkami, a wokół
twarzy pozostała cienka linia konturu. W dalszych kadrach, kiedy dziewczyna
idzie do drzwi, widać głównie włosy od tyłu.

W bocznym spacerze głowę przesunięto nad barki i zmniejszono wysunięcie
twarzy. Krok nadal ma 18 klatek i ten sam rytm. Zachowano codzienny strój:
koszulkę bez rękawów, dżinsowe szorty i sportowe buty. Porównanie rzeczywistych
kadrów Atari800 jest w `build/v360-opening-review.png`, a ruch w
`build/v360-walk-comparison.gif`.

Pula zawiera 301 współdzielonych wierszy i 11 605 B, kod główny 2542 B.
Generator w razie braku miejsca przestawia całe łańcuchy wierszy w obrębie
istniejących zakresów. Piksele, nieprzekraczalne granice stron ANTIC i zakresy
niskiej RAM odtwarzane przez loader pozostają chronione. Zmienione obrazy
banków mają indeksy 33–37 (od zera). Pakowanie zachowuje kontrakt 058.

- Stereo `releases/less-i-know-demo-release-076-stereo.xex`, 945 368 B,
  SHA-256 `43d71c3b078816ef048b1f51ccc0b9847b5efcfd45eb33f412679e9c281eb203`.
- Mono `releases/less-i-know-demo-release-077-mono.xex`, 945 368 B,
  SHA-256 `686ed212ba5cbe781b76233391ac880bbac814707c838d0d3f5cad0cb9e614c6`.

Przeszło 21 testów ukierunkowanych. Atari800 PAL, 1088 XE, Altirra OS:
59 833 aktualizacje POKEY w 076 zgodne z 074, a w 077 zgodne z 075.
Utwór trwa 5:00. Obejrzano wskazane kadry. Bez pełnego `make check`
i bez próby nowych plików na fizycznym Atari.
