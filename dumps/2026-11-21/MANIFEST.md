> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../../docs/README.md) for active instructions.

# Zrzut bitmap — 2026-11-21

Źródło: `build/visual-prototype-dev.xex` (SHA-256 `4aecdc0876a85e1d48109ce989cebc8bb6bdb3b5e6e3b9884875a6450716229e`).
Kandydat: v386 / stereo 124. Wydanie: `releases/less-i-know-demo-release-124-stereo.xex` (SHA-256 `838391be995454515856c8c44377dd039a95b1d01496c1e15da4efc117821448`).
Kopia builda: `build/visual-prototype-v386.xex` (SHA-256 `4aecdc0876a85e1d48109ce989cebc8bb6bdb3b5e6e3b9884875a6450716229e`).

Pliki 1:1 są indeksowane: wartość piksela to surowy indeks Atari.
Katalog `4x/` zawiera powiększenia nearest-neighbour, a w każdym
folderze leży `_contact-2x.png` do szybkiego przeglądu.

## Grupy

- **01-intro** — Intro: plazma GTIA 11 i karty tytułu: 40 plików
  - użycie: sceny 0-2, ticki 0-2992; banki 40-48
- **02-school** — Szkoła: pan, historia, portret i trening: 26 plików
  - użycie: sceny 3-6 i 13; banki 0, 7, 19-23 i wspólna pula wierszy
- **03-dance** — Taniec: przód, bok i klatki pośrednie: 62 plików
  - użycie: sceny 4-5 i montaż; banki 8-14 oraz 24-39
- **04-kaleidoscope** — Mozaika, tunel i oczy: 32 plików
  - użycie: scena 6 i montaż; banki 11-18, klatki 32-63
- **05-bananas** — Banany: atlasy obrotów: 320 plików
  - użycie: montaż po Trevrze; banki 3-10, 32 pozycje zapisane na wariant
- **06-trevor** — Trevor: panele, tunel i stare tło: 70 plików
  - użycie: sceny 7-10 i montaż; bank 1-2 oraz 24-39
- **07-hero** — Koszykówka i arena: 13 plików
  - użycie: sceny 11-12 i montaż; bank 1 oraz plansze areny
- **08-final** — Finał: chłopiec na tle gwiazd: 1 plików
  - użycie: scena 15; bank 39

## Weryfikacja

Sprawdzono 230 fragmentów banków; 230 zgodnych.

Dodatkowo 205 plików porównano z wydaniem 124; niezgodnych: 0.

Pliki z `verified_against_xex: true` porównano bajt w bajt z bankiem
zbudowanego XEX po spakowaniu 2bpp/4bpp. Pozostałe pochodzą z tych
samych funkcji builda, ale są komponowane w locie (np. panele Trevora
są wejściem do banków tunelu, a storyboardy trafiają do wspólnej puli
wierszy), więc nie mają własnego, ciągłego bloku w banku.

## Poza zakresem

- sprite'y PMG (players/missiles) i ich maski
- fonty: terminal, credits/outro, final mark, duże napisy
- ekrany tekstowe ANTIC 2 (loading screen, terminal)
- tablice palet i kod 6502 w bankach

## Pliki

### 01-intro

| plik | wymiary | bank | offset | źródło |
| --- | --- | --- | --- | --- |
| `01-intro/plasma/plasma-00.png` | 80×64 | 40 | $0000 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-01.png` | 80×64 | 40 | $0A00 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-02.png` | 80×64 | 40 | $1400 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-03.png` | 80×64 | 40 | $1E00 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-04.png` | 80×64 | 41 | $0000 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-05.png` | 80×64 | 41 | $0A00 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-06.png` | 80×64 | 41 | $1400 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-07.png` | 80×64 | 41 | $1E00 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-08.png` | 80×64 | 42 | $0000 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-09.png` | 80×64 | 42 | $0A00 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-10.png` | 80×64 | 42 | $1400 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-11.png` | 80×64 | 42 | $1E00 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-12.png` | 80×64 | 43 | $0000 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-13.png` | 80×64 | 43 | $0A00 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-14.png` | 80×64 | 43 | $1400 | `tools/title_plasma.py:artwork()` |
| `01-intro/plasma/plasma-15.png` | 80×64 | 43 | $1E00 | `tools/title_plasma.py:artwork()` |
| `01-intro/title-masks/title-mask-0.png` | 80×64 | 44 | $0000 | `tools/title_plasma.py:artwork() masks` |
| `01-intro/title-masks/title-mask-1.png` | 80×64 | 44 | $0A00 | `tools/title_plasma.py:artwork() masks` |
| `01-intro/title-masks/title-mask-2.png` | 80×64 | 44 | $1400 | `tools/title_plasma.py:artwork() masks` |
| `01-intro/title-masks/title-mask-3.png` | 80×64 | 44 | $1E00 | `tools/title_plasma.py:artwork() masks` |
| `01-intro/title-masks/title-mask-4.png` | 80×64 | 44 | $2800 | `tools/title_plasma.py:artwork() masks` |
| `01-intro/title-masks/title-mask-5.png` | 80×64 | 44 | $3200 | `tools/title_plasma.py:artwork() masks` |
| `01-intro/fades/title-fade-0.png` | 80×64 | 45 | $0000 | `tools/title_plasma.py:artwork() fade frames` |
| `01-intro/fades/title-fade-1.png` | 80×64 | 45 | $0A00 | `tools/title_plasma.py:artwork() fade frames` |
| `01-intro/fades/title-fade-2.png` | 80×64 | 45 | $1400 | `tools/title_plasma.py:artwork() fade frames` |
| `01-intro/fades/title-fade-3.png` | 80×64 | 45 | $1E00 | `tools/title_plasma.py:artwork() fade frames` |
| `01-intro/fades/title-fade-4.png` | 80×64 | 46 | $0000 | `tools/title_plasma.py:artwork() fade frames` |
| `01-intro/fades/title-fade-5.png` | 80×64 | 46 | $0A00 | `tools/title_plasma.py:artwork() fade frames` |
| `01-intro/transitions/title-transition-0.png` | 80×64 | 47 | $0000 | `tools/title_plasma.py:artwork() transitions` |
| `01-intro/transitions/title-transition-1.png` | 80×64 | 47 | $0A00 | `tools/title_plasma.py:artwork() transitions` |
| `01-intro/transitions/title-transition-2.png` | 80×64 | 47 | $1400 | `tools/title_plasma.py:artwork() transitions` |
| `01-intro/transitions/title-transition-3.png` | 80×64 | 47 | $1E00 | `tools/title_plasma.py:artwork() transitions` |
| `01-intro/transitions/title-transition-4.png` | 80×64 | 48 | $0000 | `tools/title_plasma.py:artwork() transitions` |
| `01-intro/transitions/title-transition-5.png` | 80×64 | 48 | $0A00 | `tools/title_plasma.py:artwork() transitions` |
| `01-intro/transitions/title-transition-6.png` | 80×64 | 48 | $1400 | `tools/title_plasma.py:artwork() transitions` |
| `01-intro/transitions/title-transition-7.png` | 80×64 | 48 | $1E00 | `tools/title_plasma.py:artwork() transitions` |
| `01-intro/transitions/title-reveal-0.png` | 80×64 | 47 | $2800 | `tools/title_plasma.py:artwork() reveal frames` |
| `01-intro/transitions/title-reveal-1.png` | 80×64 | 47 | $3200 | `tools/title_plasma.py:artwork() reveal frames` |
| `01-intro/transitions/title-reveal-2.png` | 80×64 | 48 | $2800 | `tools/title_plasma.py:artwork() reveal frames` |
| `01-intro/transitions/title-reveal-3.png` | 80×64 | 48 | $3200 | `tools/title_plasma.py:artwork() reveal frames` |

### 02-school

| plik | wymiary | bank | offset | źródło |
| --- | --- | --- | --- | --- |
| `02-school/pan/pan-00.png` | 160×64 | 19 | $0000 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-01.png` | 160×64 | 19 | $0A00 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-02.png` | 160×64 | 19 | $1400 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-03.png` | 160×64 | 19 | $1E00 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-04.png` | 160×64 | 20 | $0000 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-05.png` | 160×64 | 20 | $0A00 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-06.png` | 160×64 | 20 | $1400 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-07.png` | 160×64 | 20 | $1E00 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-08.png` | 160×64 | 21 | $0000 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-09.png` | 160×64 | 21 | $0A00 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-10.png` | 160×64 | 21 | $1400 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-11.png` | 160×64 | 21 | $1E00 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-12.png` | 160×64 | 22 | $0000 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-13.png` | 160×64 | 22 | $0A00 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-14.png` | 160×64 | 22 | $1400 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-15.png` | 160×64 | 22 | $1E00 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-16.png` | 160×64 | 23 | $0000 | `tools/school_parallax.py:frames()` |
| `02-school/pan/pan-17.png` | 160×64 | 23 | $0A00 | `tools/school_parallax.py:frames()` |
| `02-school/story/story-00.png` | 160×192 | — | — | `tools/school_story.py:story_frames()` |
| `02-school/story/story-01.png` | 160×192 | — | — | `tools/school_story.py:story_frames()` |
| `02-school/story/story-02.png` | 160×192 | — | — | `tools/school_story.py:story_frames()` |
| `02-school/story/story-03.png` | 160×192 | — | — | `tools/school_story.py:story_frames()` |
| `02-school/story/story-04.png` | 160×192 | — | — | `tools/school_story.py:story_frames()` |
| `02-school/story/story-05.png` | 160×192 | — | — | `tools/school_story.py:story_frames()` |
| `02-school/portrait/girl-portrait.png` | 160×64 | 0 | $0000 | `tools/school_story.py:girl_front_pixels()[::3]` |
| `02-school/practice/practice-storyboard.png` | 160×192 | — | $2000 | `tools/gym_practice.py:practice_pixels()` |

### 03-dance

| plik | wymiary | bank | offset | źródło |
| --- | --- | --- | --- | --- |
| `03-dance/front/front-00.png` | 160×64 | — | $0000 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-01.png` | 160×64 | — | $0A00 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-02.png` | 160×64 | — | $1400 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-03.png` | 160×64 | — | $1E00 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-04.png` | 160×64 | — | $2800 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-05.png` | 160×64 | — | $3200 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-06.png` | 160×64 | — | $0000 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-07.png` | 160×64 | — | $0A00 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-08.png` | 160×64 | — | $1400 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-09.png` | 160×64 | — | $1E00 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-10.png` | 160×64 | — | $2800 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-11.png` | 160×64 | — | $3200 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-12.png` | 160×64 | — | $0000 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-13.png` | 160×64 | — | $0A00 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-14.png` | 160×64 | — | $1400 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-15.png` | 160×64 | — | $1E00 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-16.png` | 160×64 | — | $2800 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-17.png` | 160×64 | — | $3200 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-18.png` | 160×64 | — | $0000 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-19.png` | 160×64 | — | $0A00 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-20.png` | 160×64 | — | $1400 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-21.png` | 160×64 | — | $1E00 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-22.png` | 160×64 | — | $2800 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-23.png` | 160×64 | — | $3200 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-24.png` | 160×64 | — | $0000 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-25.png` | 160×64 | — | $0A00 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-26.png` | 160×64 | — | $1400 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-27.png` | 160×64 | — | $1E00 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-28.png` | 160×64 | — | $2800 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-29.png` | 160×64 | — | $3200 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-30.png` | 160×64 | — | $0000 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-31.png` | 160×64 | — | $0A00 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-32.png` | 160×64 | — | $1400 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-33.png` | 160×64 | — | $1E00 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-34.png` | 160×64 | — | $2800 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/front/front-35.png` | 160×64 | — | $3200 | `tools/ribbon_dance.py:packed_frame()` |
| `03-dance/side/side-00.png` | 68×56 | 24 | $0A00 | `tools/ribbon_dance.py:side_actor_data()` |
| `03-dance/side/side-01.png` | 68×56 | 25 | $0A00 | `tools/ribbon_dance.py:side_actor_data()` |
| `03-dance/side/side-02.png` | 68×56 | 26 | $0A00 | `tools/ribbon_dance.py:side_actor_data()` |
| `03-dance/side/side-03.png` | 68×56 | 27 | $0A00 | `tools/ribbon_dance.py:side_actor_data()` |
| `03-dance/side/side-04.png` | 68×56 | 28 | $0A00 | `tools/ribbon_dance.py:side_actor_data()` |
| `03-dance/side/side-05.png` | 68×56 | 29 | $0A00 | `tools/ribbon_dance.py:side_actor_data()` |
| `03-dance/side/side-06.png` | 68×56 | 30 | $0A00 | `tools/ribbon_dance.py:side_actor_data()` |
| `03-dance/side/side-07.png` | 68×56 | 31 | $0A00 | `tools/ribbon_dance.py:side_actor_data()` |
| `03-dance/inbetweens/inbetween-00.png` | 160×64 | 2 | $0600 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-01.png` | 160×64 | 2 | $0B60 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-02.png` | 160×64 | 2 | $1070 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-03.png` | 160×64 | 2 | $1559 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-04.png` | 160×64 | 2 | $2000 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-05.png` | 160×64 | 2 | $2537 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-06.png` | 160×64 | 2 | $2A51 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-07.png` | 160×64 | 32 | $0A00 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-08.png` | 160×64 | 33 | $0A00 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-09.png` | 160×64 | 34 | $0A00 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-10.png` | 160×64 | 35 | $0A00 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-11.png` | 160×64 | 36 | $0A00 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-12.png` | 160×64 | 37 | $0A00 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-13.png` | 160×64 | 38 | $0A00 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-14.png` | 160×64 | 32 | $0DB0 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-15.png` | 160×64 | 33 | $0DAC | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-16.png` | 160×64 | 34 | $0DE2 | `tools/ribbon_inbetweens.py:packed()/compress()` |
| `03-dance/inbetweens/inbetween-17.png` | 160×64 | 35 | $0F17 | `tools/ribbon_inbetweens.py:packed()/compress()` |

### 04-kaleidoscope

| plik | wymiary | bank | offset | źródło |
| --- | --- | --- | --- | --- |
| `04-kaleidoscope/frames/kaleido-00.png` | 160×96 | 11 | $0000 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-01.png` | 160×96 | 11 | $0F00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-02.png` | 160×96 | 11 | $1E00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-03.png` | 160×96 | 11 | $2D00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-04.png` | 160×96 | 12 | $0000 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-05.png` | 160×96 | 12 | $0F00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-06.png` | 160×96 | 12 | $1E00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-07.png` | 160×96 | 12 | $2D00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-08.png` | 160×96 | 13 | $0000 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-09.png` | 160×96 | 13 | $0F00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-10.png` | 160×96 | 13 | $1E00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-11.png` | 160×96 | 13 | $2D00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-12.png` | 160×96 | 14 | $0000 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-13.png` | 160×96 | 14 | $0F00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-14.png` | 160×96 | 14 | $1E00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-15.png` | 160×96 | 14 | $2D00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-16.png` | 160×96 | 15 | $0000 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-17.png` | 160×96 | 15 | $0F00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-18.png` | 160×96 | 15 | $1E00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-19.png` | 160×96 | 15 | $2D00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-20.png` | 160×96 | 16 | $0000 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-21.png` | 160×96 | 16 | $0F00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-22.png` | 160×96 | 16 | $1E00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-23.png` | 160×96 | 16 | $2D00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-24.png` | 160×96 | 17 | $0000 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-25.png` | 160×96 | 17 | $0F00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-26.png` | 160×96 | 17 | $1E00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-27.png` | 160×96 | 17 | $2D00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-28.png` | 160×96 | 18 | $0000 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-29.png` | 160×96 | 18 | $0F00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-30.png` | 160×96 | 18 | $1E00 | `tools/mosaic.py:pixels()` |
| `04-kaleidoscope/frames/kaleido-31.png` | 160×96 | 18 | $2D00 | `tools/mosaic.py:pixels()` |

### 05-bananas

| plik | wymiary | bank | offset | źródło |
| --- | --- | --- | --- | --- |
| `05-bananas/v0-w20/pose-00.png` | 20×12 | 3 | $1BC3 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-01.png` | 20×12 | 3 | $1BF9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-02.png` | 20×12 | 3 | $1C2F | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-03.png` | 20×12 | 3 | $1C65 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-04.png` | 20×12 | 3 | $1C9B | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-05.png` | 20×12 | 3 | $1CD1 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-06.png` | 20×12 | 3 | $1D07 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-07.png` | 20×12 | 3 | $1D3D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-08.png` | 20×12 | 3 | $1D73 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-09.png` | 20×12 | 3 | $1DA9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-10.png` | 20×12 | 3 | $1DDF | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-11.png` | 20×12 | 3 | $1E15 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-12.png` | 20×12 | 3 | $1E4B | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-13.png` | 20×12 | 3 | $1E81 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-14.png` | 20×12 | 3 | $1EB7 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-15.png` | 20×12 | 3 | $1EED | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-16.png` | 20×12 | 3 | $1F23 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-17.png` | 20×12 | 3 | $1F59 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-18.png` | 20×12 | 3 | $1F8F | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-19.png` | 20×12 | 3 | $1FC5 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-20.png` | 20×12 | 3 | $1FFB | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-21.png` | 20×12 | 3 | $2031 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-22.png` | 20×12 | 3 | $2067 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-23.png` | 20×12 | 3 | $209D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-24.png` | 20×12 | 3 | $20D3 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-25.png` | 20×12 | 3 | $2109 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-26.png` | 20×12 | 3 | $213F | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-27.png` | 20×12 | 3 | $2175 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-28.png` | 20×12 | 3 | $21AB | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-29.png` | 20×12 | 3 | $21E1 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-30.png` | 20×12 | 3 | $2217 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w20/pose-31.png` | 20×12 | 3 | $224D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-00.png` | 24×14 | 3 | $22C9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-01.png` | 24×14 | 3 | $2315 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-02.png` | 24×14 | 3 | $2361 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-03.png` | 24×14 | 3 | $23AD | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-04.png` | 24×14 | 3 | $23F9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-05.png` | 24×14 | 3 | $2445 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-06.png` | 24×14 | 3 | $2492 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-07.png` | 24×14 | 3 | $24DF | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-08.png` | 24×14 | 3 | $252C | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-09.png` | 24×14 | 3 | $2579 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-10.png` | 24×14 | 3 | $25C6 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-11.png` | 24×14 | 3 | $2613 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-12.png` | 24×14 | 3 | $2660 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-13.png` | 24×14 | 3 | $26AD | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-14.png` | 24×14 | 3 | $26F9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-15.png` | 24×14 | 3 | $2745 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-16.png` | 24×14 | 3 | $2791 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-17.png` | 24×14 | 3 | $27DE | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-18.png` | 24×14 | 3 | $282A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-19.png` | 24×14 | 3 | $2876 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-20.png` | 24×14 | 3 | $28C3 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-21.png` | 24×14 | 3 | $2910 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-22.png` | 24×14 | 3 | $295D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-23.png` | 24×14 | 3 | $29A9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-24.png` | 24×14 | 3 | $29F5 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-25.png` | 24×14 | 3 | $2A41 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-26.png` | 24×14 | 3 | $2A8E | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-27.png` | 24×14 | 3 | $2ADB | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-28.png` | 24×14 | 3 | $2B28 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-29.png` | 24×14 | 3 | $2B74 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-30.png` | 24×14 | 3 | $2BC0 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w24/pose-31.png` | 24×14 | 3 | $2C0C | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-00.png` | 28×16 | 4 | $1A01 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-01.png` | 28×16 | 4 | $1A68 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-02.png` | 28×16 | 4 | $1ACF | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-03.png` | 28×16 | 4 | $1B36 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-04.png` | 28×16 | 4 | $1B9C | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-05.png` | 28×16 | 4 | $1C03 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-06.png` | 28×16 | 4 | $1C6A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-07.png` | 28×16 | 4 | $1CD1 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-08.png` | 28×16 | 4 | $1D38 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-09.png` | 28×16 | 4 | $1D9F | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-10.png` | 28×16 | 4 | $1E06 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-11.png` | 28×16 | 4 | $1E6D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-12.png` | 28×16 | 4 | $1ED4 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-13.png` | 28×16 | 4 | $1F3B | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-14.png` | 28×16 | 4 | $1FA2 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-15.png` | 28×16 | 4 | $2009 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-16.png` | 28×16 | 4 | $2070 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-17.png` | 28×16 | 4 | $20D7 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-18.png` | 28×16 | 4 | $213E | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-19.png` | 28×16 | 4 | $21A5 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-20.png` | 28×16 | 4 | $220C | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-21.png` | 28×16 | 4 | $2273 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-22.png` | 28×16 | 4 | $22DA | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-23.png` | 28×16 | 4 | $2341 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-24.png` | 28×16 | 4 | $23A8 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-25.png` | 28×16 | 4 | $240F | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-26.png` | 28×16 | 4 | $2476 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-27.png` | 28×16 | 4 | $24DD | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-28.png` | 28×16 | 4 | $2544 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-29.png` | 28×16 | 4 | $25AB | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-30.png` | 28×16 | 4 | $2612 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w28/pose-31.png` | 28×16 | 4 | $2679 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-00.png` | 32×19 | 5 | $1D17 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-01.png` | 32×19 | 5 | $1DA4 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-02.png` | 32×19 | 5 | $1E31 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-03.png` | 32×19 | 5 | $1EBE | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-04.png` | 32×19 | 5 | $1F4B | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-05.png` | 32×19 | 5 | $1FD7 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-06.png` | 32×19 | 5 | $205D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-07.png` | 32×19 | 5 | $20EA | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-08.png` | 32×19 | 5 | $2177 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-09.png` | 32×19 | 5 | $2205 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-10.png` | 32×19 | 5 | $2293 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-11.png` | 32×19 | 5 | $2321 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-12.png` | 32×19 | 5 | $23AE | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-13.png` | 32×19 | 5 | $243B | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-14.png` | 32×19 | 5 | $24C8 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-15.png` | 32×19 | 5 | $2555 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-16.png` | 32×19 | 5 | $25E2 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-17.png` | 32×19 | 5 | $2670 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-18.png` | 32×19 | 5 | $26FD | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-19.png` | 32×19 | 5 | $278A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-20.png` | 32×19 | 5 | $2817 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-21.png` | 32×19 | 5 | $28A5 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-22.png` | 32×19 | 5 | $2933 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-23.png` | 32×19 | 5 | $29C0 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-24.png` | 32×19 | 5 | $2A4D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-25.png` | 32×19 | 5 | $2ADA | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-26.png` | 32×19 | 5 | $2B68 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-27.png` | 32×19 | 5 | $2BF6 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-28.png` | 32×19 | 5 | $2C84 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-29.png` | 32×19 | 5 | $2D11 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-30.png` | 32×19 | 5 | $2D9E | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w32/pose-31.png` | 32×19 | 5 | $2E2B | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-00.png` | 36×21 | 6 | $1DC9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-01.png` | 36×21 | 6 | $1E79 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-02.png` | 36×21 | 6 | $1F2A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-03.png` | 36×21 | 6 | $1FDA | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-04.png` | 36×21 | 6 | $208A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-05.png` | 36×21 | 6 | $2133 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-06.png` | 36×21 | 6 | $21DC | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-07.png` | 36×21 | 6 | $2285 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-08.png` | 36×21 | 6 | $2336 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-09.png` | 36×21 | 6 | $23E7 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-10.png` | 36×21 | 6 | $2498 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-11.png` | 36×21 | 6 | $2549 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-12.png` | 36×21 | 6 | $25FA | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-13.png` | 36×21 | 6 | $26AB | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-14.png` | 36×21 | 6 | $275C | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-15.png` | 36×21 | 6 | $280D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-16.png` | 36×21 | 6 | $28BE | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-17.png` | 36×21 | 6 | $296E | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-18.png` | 36×21 | 6 | $2A1F | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-19.png` | 36×21 | 6 | $2AD0 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-20.png` | 36×21 | 6 | $2B81 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-21.png` | 36×21 | 6 | $2C31 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-22.png` | 36×21 | 6 | $2CE2 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-23.png` | 36×21 | 6 | $2D93 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-24.png` | 36×21 | 6 | $2E44 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-25.png` | 36×21 | 6 | $2EF5 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-26.png` | 36×21 | 6 | $2FA5 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-27.png` | 36×21 | 6 | $3056 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-28.png` | 36×21 | 6 | $3107 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-29.png` | 36×21 | 6 | $31B8 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-30.png` | 36×21 | 6 | $3269 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v0-w36/pose-31.png` | 36×21 | 6 | $331A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-00.png` | 20×12 | 7 | $1BC3 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-01.png` | 20×12 | 7 | $1BFE | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-02.png` | 20×12 | 7 | $1C38 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-03.png` | 20×12 | 7 | $1C72 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-04.png` | 20×12 | 7 | $1CAC | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-05.png` | 20×12 | 7 | $1CE6 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-06.png` | 20×12 | 7 | $1D21 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-07.png` | 20×12 | 7 | $1D5C | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-08.png` | 20×12 | 7 | $1D97 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-09.png` | 20×12 | 7 | $1DD2 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-10.png` | 20×12 | 7 | $1E0C | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-11.png` | 20×12 | 7 | $1E46 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-12.png` | 20×12 | 7 | $1E80 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-13.png` | 20×12 | 7 | $1EBA | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-14.png` | 20×12 | 7 | $1EF4 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-15.png` | 20×12 | 7 | $1F2D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-16.png` | 20×12 | 7 | $1F66 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-17.png` | 20×12 | 7 | $1F9A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-18.png` | 20×12 | 7 | $1FCE | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-19.png` | 20×12 | 7 | $2002 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-20.png` | 20×12 | 7 | $2035 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-21.png` | 20×12 | 7 | $2065 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-22.png` | 20×12 | 7 | $2095 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-23.png` | 20×12 | 7 | $20C7 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-24.png` | 20×12 | 7 | $20F9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-25.png` | 20×12 | 7 | $212B | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-26.png` | 20×12 | 7 | $2161 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-27.png` | 20×12 | 7 | $2197 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-28.png` | 20×12 | 7 | $21CE | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-29.png` | 20×12 | 7 | $2205 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-30.png` | 20×12 | 7 | $223B | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w20/pose-31.png` | 20×12 | 7 | $2276 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-00.png` | 24×14 | 7 | $22F2 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-01.png` | 24×14 | 7 | $2344 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-02.png` | 24×14 | 7 | $2396 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-03.png` | 24×14 | 7 | $23E8 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-04.png` | 24×14 | 7 | $2439 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-05.png` | 24×14 | 7 | $248A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-06.png` | 24×14 | 7 | $24DD | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-07.png` | 24×14 | 7 | $2530 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-08.png` | 24×14 | 7 | $2583 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-09.png` | 24×14 | 7 | $25D6 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-10.png` | 24×14 | 7 | $2628 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-11.png` | 24×14 | 7 | $267A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-12.png` | 24×14 | 7 | $26CC | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-13.png` | 24×14 | 7 | $271D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-14.png` | 24×14 | 7 | $276E | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-15.png` | 24×14 | 7 | $27BF | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-16.png` | 24×14 | 7 | $2810 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-17.png` | 24×14 | 7 | $2860 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-18.png` | 24×14 | 7 | $28AA | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-19.png` | 24×14 | 7 | $28F4 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-20.png` | 24×14 | 7 | $293A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-21.png` | 24×14 | 7 | $2980 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-22.png` | 24×14 | 7 | $29C6 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-23.png` | 24×14 | 7 | $2A0C | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-24.png` | 24×14 | 7 | $2A53 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-25.png` | 24×14 | 7 | $2A9A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-26.png` | 24×14 | 7 | $2AE2 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-27.png` | 24×14 | 7 | $2B2F | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-28.png` | 24×14 | 7 | $2B7C | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-29.png` | 24×14 | 7 | $2BC9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-30.png` | 24×14 | 7 | $2C16 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w24/pose-31.png` | 24×14 | 7 | $2C68 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-00.png` | 28×16 | 8 | $1A01 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-01.png` | 28×16 | 8 | $1A6F | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-02.png` | 28×16 | 8 | $1ADC | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-03.png` | 28×16 | 8 | $1B49 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-04.png` | 28×16 | 8 | $1BB6 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-05.png` | 28×16 | 8 | $1C22 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-06.png` | 28×16 | 8 | $1C8E | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-07.png` | 28×16 | 8 | $1CFC | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-08.png` | 28×16 | 8 | $1D6A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-09.png` | 28×16 | 8 | $1DD8 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-10.png` | 28×16 | 8 | $1E46 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-11.png` | 28×16 | 8 | $1EB3 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-12.png` | 28×16 | 8 | $1F20 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-13.png` | 28×16 | 8 | $1F8D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-14.png` | 28×16 | 8 | $1FF9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-15.png` | 28×16 | 8 | $2065 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-16.png` | 28×16 | 8 | $20D1 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-17.png` | 28×16 | 8 | $2136 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-18.png` | 28×16 | 8 | $219A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-19.png` | 28×16 | 8 | $21FE | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-20.png` | 28×16 | 8 | $225B | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-21.png` | 28×16 | 8 | $22B7 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-22.png` | 28×16 | 8 | $230F | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-23.png` | 28×16 | 8 | $236A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-24.png` | 28×16 | 8 | $23C4 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-25.png` | 28×16 | 8 | $2425 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-26.png` | 28×16 | 8 | $2486 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-27.png` | 28×16 | 8 | $24ED | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-28.png` | 28×16 | 8 | $2554 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-29.png` | 28×16 | 8 | $25BC | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-30.png` | 28×16 | 8 | $2624 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w28/pose-31.png` | 28×16 | 8 | $2692 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-00.png` | 32×19 | 9 | $1D17 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-01.png` | 32×19 | 9 | $1DAC | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-02.png` | 32×19 | 9 | $1E41 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-03.png` | 32×19 | 9 | $1ED6 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-04.png` | 32×19 | 9 | $1F6A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-05.png` | 32×19 | 9 | $1FFE | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-06.png` | 32×19 | 9 | $2091 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-07.png` | 32×19 | 9 | $2127 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-08.png` | 32×19 | 9 | $21BD | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-09.png` | 32×19 | 9 | $2253 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-10.png` | 32×19 | 9 | $22E9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-11.png` | 32×19 | 9 | $237E | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-12.png` | 32×19 | 9 | $2413 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-13.png` | 32×19 | 9 | $24A7 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-14.png` | 32×19 | 9 | $253B | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-15.png` | 32×19 | 9 | $25CF | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-16.png` | 32×19 | 9 | $2662 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-17.png` | 32×19 | 9 | $26ED | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-18.png` | 32×19 | 9 | $2778 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-19.png` | 32×19 | 9 | $27FA | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-20.png` | 32×19 | 9 | $287C | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-21.png` | 32×19 | 9 | $28F9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-22.png` | 32×19 | 9 | $2976 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-23.png` | 32×19 | 9 | $29F3 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-24.png` | 32×19 | 9 | $2A72 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-25.png` | 32×19 | 9 | $2AF1 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-26.png` | 32×19 | 9 | $2B78 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-27.png` | 32×19 | 9 | $2BFF | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-28.png` | 32×19 | 9 | $2C8D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-29.png` | 32×19 | 9 | $2D1B | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-30.png` | 32×19 | 9 | $2DAA | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w32/pose-31.png` | 32×19 | 9 | $2E38 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-00.png` | 36×21 | 10 | $1DC9 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-01.png` | 36×21 | 10 | $1E83 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-02.png` | 36×21 | 10 | $1F3D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-03.png` | 36×21 | 10 | $1FF6 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-04.png` | 36×21 | 10 | $20AF | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-05.png` | 36×21 | 10 | $2167 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-06.png` | 36×21 | 10 | $221F | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-07.png` | 36×21 | 10 | $22DA | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-08.png` | 36×21 | 10 | $2395 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-09.png` | 36×21 | 10 | $2450 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-10.png` | 36×21 | 10 | $250A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-11.png` | 36×21 | 10 | $25C4 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-12.png` | 36×21 | 10 | $267D | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-13.png` | 36×21 | 10 | $2736 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-14.png` | 36×21 | 10 | $27EE | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-15.png` | 36×21 | 10 | $28A6 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-16.png` | 36×21 | 10 | $295E | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-17.png` | 36×21 | 10 | $2A0C | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-18.png` | 36×21 | 10 | $2ABA | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-19.png` | 36×21 | 10 | $2B5E | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-20.png` | 36×21 | 10 | $2C02 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-21.png` | 36×21 | 10 | $2CA0 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-22.png` | 36×21 | 10 | $2D3E | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-23.png` | 36×21 | 10 | $2DD6 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-24.png` | 36×21 | 10 | $2E77 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-25.png` | 36×21 | 10 | $2F18 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-26.png` | 36×21 | 10 | $2FC1 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-27.png` | 36×21 | 10 | $306A | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-28.png` | 36×21 | 10 | $3114 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-29.png` | 36×21 | 10 | $31C5 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-30.png` | 36×21 | 10 | $3278 | `tools/banana_sprites.py:stamp()` |
| `05-bananas/v1-w36/pose-31.png` | 36×21 | 10 | $332A | `tools/banana_sprites.py:stamp()` |

### 06-trevor

| plik | wymiary | bank | offset | źródło |
| --- | --- | --- | --- | --- |
| `06-trevor/panels/panel-0.png` | 160×64 | — | — | `tools/trevor_polished.py:frames()` |
| `06-trevor/panels/panel-1.png` | 160×64 | — | — | `tools/trevor_polished.py:frames()` |
| `06-trevor/panels/panel-2.png` | 160×64 | — | — | `tools/trevor_polished.py:frames()` |
| `06-trevor/panels/panel-3.png` | 160×64 | — | — | `tools/trevor_polished.py:frames()` |
| `06-trevor/tunnel/phase-00-stage-0.png` | 160×64 | 24 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-00-stage-1.png` | 160×64 | 24 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-00-stage-2.png` | 160×64 | 24 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-00-stage-3.png` | 160×64 | 24 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-01-stage-0.png` | 160×64 | 25 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-01-stage-1.png` | 160×64 | 25 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-01-stage-2.png` | 160×64 | 25 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-01-stage-3.png` | 160×64 | 25 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-02-stage-0.png` | 160×64 | 26 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-02-stage-1.png` | 160×64 | 26 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-02-stage-2.png` | 160×64 | 26 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-02-stage-3.png` | 160×64 | 26 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-03-stage-0.png` | 160×64 | 27 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-03-stage-1.png` | 160×64 | 27 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-03-stage-2.png` | 160×64 | 27 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-03-stage-3.png` | 160×64 | 27 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-04-stage-0.png` | 160×64 | 28 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-04-stage-1.png` | 160×64 | 28 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-04-stage-2.png` | 160×64 | 28 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-04-stage-3.png` | 160×64 | 28 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-05-stage-0.png` | 160×64 | 29 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-05-stage-1.png` | 160×64 | 29 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-05-stage-2.png` | 160×64 | 29 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-05-stage-3.png` | 160×64 | 29 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-06-stage-0.png` | 160×64 | 30 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-06-stage-1.png` | 160×64 | 30 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-06-stage-2.png` | 160×64 | 30 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-06-stage-3.png` | 160×64 | 30 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-07-stage-0.png` | 160×64 | 31 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-07-stage-1.png` | 160×64 | 31 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-07-stage-2.png` | 160×64 | 31 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-07-stage-3.png` | 160×64 | 31 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-08-stage-0.png` | 160×64 | 32 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-08-stage-1.png` | 160×64 | 32 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-08-stage-2.png` | 160×64 | 32 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-08-stage-3.png` | 160×64 | 32 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-09-stage-0.png` | 160×64 | 33 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-09-stage-1.png` | 160×64 | 33 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-09-stage-2.png` | 160×64 | 33 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-09-stage-3.png` | 160×64 | 33 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-10-stage-0.png` | 160×64 | 34 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-10-stage-1.png` | 160×64 | 34 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-10-stage-2.png` | 160×64 | 34 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-10-stage-3.png` | 160×64 | 34 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-11-stage-0.png` | 160×64 | 35 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-11-stage-1.png` | 160×64 | 35 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-11-stage-2.png` | 160×64 | 35 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-11-stage-3.png` | 160×64 | 35 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-12-stage-0.png` | 160×64 | 36 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-12-stage-1.png` | 160×64 | 36 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-12-stage-2.png` | 160×64 | 36 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-12-stage-3.png` | 160×64 | 36 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-13-stage-0.png` | 160×64 | 37 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-13-stage-1.png` | 160×64 | 37 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-13-stage-2.png` | 160×64 | 37 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-13-stage-3.png` | 160×64 | 37 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-14-stage-0.png` | 160×64 | 38 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-14-stage-1.png` | 160×64 | 38 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-14-stage-2.png` | 160×64 | 38 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-14-stage-3.png` | 160×64 | 38 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-15-stage-0.png` | 160×64 | 39 | $1400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-15-stage-1.png` | 160×64 | 39 | $2A00 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-15-stage-2.png` | 160×64 | 39 | $3400 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/tunnel/phase-15-stage-3.png` | 160×64 | 39 | $0000 | `tools/trevor_polished.py:tunnel_frames()` |
| `06-trevor/legacy/legacy-0.png` | 160×64 | — | — | `tools/trevor_awakens.py:backgrounds()` |
| `06-trevor/legacy/legacy-1.png` | 160×64 | — | — | `tools/trevor_awakens.py:backgrounds()` |

### 07-hero

| plik | wymiary | bank | offset | źródło |
| --- | --- | --- | --- | --- |
| `07-hero/poses/pose-0.png` | 160×56 | 1 | $0B80 | `tools/basketball_hero.py:frames()` |
| `07-hero/poses/pose-1.png` | 160×56 | 1 | — | `tools/basketball_hero.py:frames()` |
| `07-hero/poses/pose-2.png` | 160×56 | 1 | $1440 | `tools/basketball_hero.py:frames()` |
| `07-hero/poses/pose-3.png` | 160×56 | 1 | $1D00 | `tools/basketball_hero.py:frames()` |
| `07-hero/poses/pose-4.png` | 160×56 | 1 | $25C0 | `tools/basketball_hero.py:frames()` |
| `07-hero/poses/pose-5.png` | 160×56 | 1 | $2E80 | `tools/basketball_hero.py:frames()` |
| `07-hero/poses/pose-6.png` | 160×56 | 1 | — | `tools/basketball_hero.py:frames()` |
| `07-hero/poses/pose-7.png` | 160×56 | 1 | — | `tools/basketball_hero.py:frames()` |
| `07-hero/shatter/shatter-1.png` | 160×56 | 1 | $3ADC | `tools/basketball_hero.py:shattered_frame()` |
| `07-hero/shatter/shatter-2.png` | 160×56 | 1 | $3BFC | `tools/basketball_hero.py:shattered_frame()` |
| `07-hero/shatter/shatter-3.png` | 160×56 | 1 | $3D1C | `tools/basketball_hero.py:shattered_frame()` |
| `07-hero/arena/arena-exterior.png` | 200×64 | — | — | `tools/arena_art.py:background()` |
| `07-hero/arena/arena-interior.png` | 160×56 | — | — | `tools/arena_art.py:background()` |

### 08-final

| plik | wymiary | bank | offset | źródło |
| --- | --- | --- | --- | --- |
| `08-final/scene/final-boy.png` | 160×64 | 39 | $0A00 | `tools/final_boy.py:artwork()` |

