> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# Graphics layers report — v246

**Date:** 2026-11-11  
**Scope:** layer and background export for `build/visual-prototype-v246.xex`; no
changes to source code, generators or XEX files. Only the report and the
resulting PNGs were added; no tests were run.

## 1. Export result

The layers are in `build/v246-scene-layers/`:

- 159 PNG files in the `characters/`, `backgrounds/` and
  `composite-only/` directories;
- `INDEX.md` contains the list, sources and limitations of each kind of asset;
- `build/v246-scene-layers.zip` contains the whole set.

The export is anchored to XEX v246 with SHA-256
`449defc2cfd2d3cdd0af3d4c34acc5171168f9718592deb544c5ed4e26ab0fba`.

## 2. What "a separate plane" means in this set

The files have three different kinds of separation. They must not be treated as
equivalent:

1. **Transparent character (`RGBA`)** — the alpha comes from the production
   source or from the mask used by the current generator. It can be placed on
   another background.
2. **Delta layer (`aligned delta`)** — stores only the pixels that differ from
   a specific background plate. It is exact when composited with that plate,
   but it is not a universal character silhouette.
3. **Flattened composite** — the character and the background are already one
   source image. The file is kept as a reference; we do not pretend it has a
   real alpha channel.

Disabling PMG in the previous export removed the hardware players and missiles
from the previews. It did not separate characters drawn directly in the bitmap.

## 3. Content by scene

| Scene | Characters / planes | Separation status |
|---|---|---|
| Intro | 16 plasma phases, the city and the Crane; six title masks | Background and text masks separate; the background atlas uses a fixed GTIA 6 brightness, so it does not reproduce DLI brightness changes. |
| Act 1 — façade | Boy, girl, ATARI ARENA plate | Plate from the generator; girl in RGBA; three frames of the boy as deltas to the plate. The clean source sprite of the whistling boy is separate. |
| Act 1 — training | Storyboard of three training shots | The input storyboard is flattened. v246 has no separate masks for the characters and the gym, so the shots are in `composite-only/`. |
| Act 2 — ribbons | Group, side and top poses plus V166/V171/V173 intermediate frames | Separate transparent pose sheets; the gym background and the scrolling gym background are separate. |
| Act 3 — basketball | Eight runtime frames V175 and the hall plate | The runtime layer contains every pixel that differs between the frame and the plate — character, ball and backboard elements. It is not a clean cutout of the basketball player alone. The V177 sheet is clean RGBA but **is not** the graphic used by v246 (V189 restored the V175 frames). |
| Act 4 — Trevor | Entrance, four fight poses, separate PMG reveal | The character and the tunnel phases are separated. The PMG reveal is an additional separate layer. |
| Act 5 / after Trevor | Bananas, spiral and organic tunnel, director's windows | Representative v246 bitmap screens without PMG; in these shots the bitmap itself is the background/effect. |
| Finale | Lying boy and floor grid | The boy's silhouette has a runtime mask; the grid is a separate plate. |

The full list of files and their paths is in
`build/v246-scene-layers/INDEX.md`.

## 4. Limitations and risk of confusion

- **Boy from Act 1:** the neutral, inverted and whistling school bitmap
  is composed from the plate. The `*-aligned-delta.png` export reproduces the
  delta for that particular façade; it must not be used as an isolated
  silhouette on any background. The clean whistling-boy sprite has a separate
  `source` name.
- **Training:** separating the people from the storyboard would require new
  masks or manual tracing. No such approximations were added in this report.
- **Basketball:** the source V177 sheet looks like the basketball player alone,
  but v246 renders the recovered V175 frames together with the ball/backboard.
  The V177 sheet must not be described as a faithful runtime cutout.
- **Bitmap and PMG layers:** the ball, fireworks and fragments may belong to
  separate PMGs, while the basketball player or Trevor are bitmap. Disabling PMG
  removes the first group, not the second.

## 5. Contract for further expansion

When adding or fixing scenes, the following source layout is recommended:

```text
scene-layers/<scene-id>/
  background.png
  characters/<character-id>/<pose-id>.png
  overlays/<effect-id>/<phase>.png
  manifest.json
```

The manifest should describe at least: `scene`, `character/effect`, source
version, size, anchor and screen scale, masking method, base background
identifier, and the status `runtime-exact`, `source-only`, `aligned-delta` or
`composite-only`.

Quality rules:

1. Provide a new character with a real alpha channel and a separate background
   plate; do not use black as transparency for hair, outlines and jackets.
2. Always pair a delta layer with the hash/ID of the background against which it
   was computed.
3. Check every `background + characters + overlays` set by recompositing it and
   comparing with the corresponding v246 PNG. Mark deviations; do not hide them
   under the name "cutout".
4. For flattened sources (currently the training storyboard), first obtain the
   original layers from the author or approve manual masks. Do not change the
   build-time compositor code without separate approval.
5. Keep PMG as its own hardware layer; exports without PMG are references to the
   bitmap, not a complete reproduction of all effects.

## 6. Next work without code changes

1. Review `INDEX.md` and indicate whether manual masks are needed for the
   training storyboard.
2. Decide whether the basketball player should stay consistent with runtime
   V175 or return to the source RGBA V177; this is an artistic and memory
   decision, not just a file export.
3. On further scene changes, save new plates and masks in separate sources, and
   then refresh the layer export from the new XEX number.
