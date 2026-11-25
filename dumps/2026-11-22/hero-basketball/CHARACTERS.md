> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../../../docs/README.md) for active instructions.

# Klatki postaci — 2026-11-22

Źródło: `build/visual-prototype-dev.xex` (SHA-256 `a16369204db01d42aa2d2789f5ebdfec472bb5a5670c79e30beec6cacd6fc731`).
Wydanie referencyjne: `releases/less-i-know-demo-release-133-stereo.xex`.

Klatek wejściowych: 11; unikalnych: 11; usunięto dokładnych duplikatów: 0.

| postać | klatek | unikalnych | rozmiary | źródło |
| --- | ---: | ---: | --- | --- |
| hero-basketball | 11 | 11 | 160×56 | `basketball_hero.frames()/shattered_frame()` |

## Uwagi

- Trevor/tunel: 64 klatki różnią się tłem tunelu; postać ma 4 etapy.
- Taniec: klatki 16-31 to samo tło sali bez tancerki, więc pominięte.
- Chłopiec szkolny i trening mają tło wpieczone w klatkę.
- Dziewczyna szkolna jest zapisana jako sprite z alfą (źródło builda).
- school-girl/walk-0..3 to arkusz girl-walk-cycle-v177; bieżący montaż go nie używa.
- Nieużywane arkusze (girl_back_art, walk_head_art, boy-whistle, hero-v177) pominięto.

Klatki 1:1 są indeksowane; sprite’y dziewczyny i boku tancerki
mają kanał alfa oraz osobną maskę `*-mask.png`.

