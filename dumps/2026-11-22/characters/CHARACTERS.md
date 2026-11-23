# Klatki postaci — 2026-11-22

Źródło: `build/visual-prototype-dev.xex` (SHA-256 `62eb87c5f957c22c67430fd19a9aaed226afb64b91358a698aa437ab2e16bd43`).
Wydanie referencyjne: `releases/less-i-know-demo-release-133-stereo.xex`.

Klatek wejściowych: 188; unikalnych: 188; usunięto dokładnych duplikatów: 0.

| postać | klatek | unikalnych | rozmiary | źródło |
| --- | ---: | ---: | --- | --- |
| school-boy | 3 | 3 | 160×192 | `school_story.boy_poses()` |
| school-story | 6 | 6 | 160×192 | `school_story.story_frames()` |
| school-girl | 8 | 8 | 48×64, 96×128, 160×64 | `build/*.rgba + school_story` |
| arena-walk-girl | 18 | 18 | 160×64 | `school_parallax.frames()` |
| school-practice | 3 | 3 | 160×64 | `gym_practice.practice_pixels()` |
| cheer-dance | 20 | 20 | 160×64 | `ribbon_dance.artwork()` |
| ribbon-side | 8 | 8 | 68×56 | `ribbon_dance.side_actor_data()` |
| ribbon-inbetweens | 18 | 18 | 160×64 | `ribbon_inbetweens.payloads()` |
| trevor-panels | 4 | 4 | 160×64 | `trevor_polished.frames()` |
| trevor-tunnel | 64 | 64 | 160×64 | `trevor_polished.tunnel_frames()` |
| hero-basketball | 11 | 11 | 160×56 | `basketball_hero.frames()/shattered_frame()` |
| final-boy | 1 | 1 | 160×64 | `final_boy.artwork()` |
| crush-portraits | 4 | 4 | 80×52 | `crush_portraits.portraits()` |
| crush-pompoms | 16 | 16 | 80×52 | `pompom_effects.variants()` |
| girl-eyes | 4 | 4 | 160×96 | `girl_eyes.pixels()` |

## Uwagi

- Trevor/tunel: 64 klatki różnią się tłem tunelu; postać ma 4 etapy.
- Taniec: klatki 16-31 to samo tło sali bez tancerki, więc pominięte.
- Chłopiec szkolny i trening mają tło wpieczone w klatkę.
- Dziewczyna szkolna jest zapisana jako sprite z alfą (źródło builda).
- school-girl/walk-0..3 to arkusz girl-walk-cycle-v177; bieżący montaż go nie używa.
- Nieużywane arkusze (girl_back_art, walk_head_art, boy-whistle, hero-v177) pominięto.

Klatki 1:1 są indeksowane; sprite’y dziewczyny i boku tancerki
mają kanał alfa oraz osobną maskę `*-mask.png`.

