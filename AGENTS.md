# Repository Guidelines

## Project Structure & Module Organization

This project is an Atari XE 1 MB audiovisual demo for “The Less I Know The Better.” The checkout contains planning documents, a source pipeline, tests and a prebuilt player:

- `TLIKTB_Atari_Timeline_v2.md`: act boundaries, musical events, and player tick synchronization.
- `TLIKTB_Technical_Constraints.md`: hardware limits, memory layout, proposed asset formats, and verification tasks V1–V7.
- `less-i-know-release-v035.xex`: the supplied executable.

`tools/` generates NMOS 6502 code and assets; `tests/` executes callbacks with py65; `assets/` contains source artwork. `build/visual-prototype-dev.xex` and its JSON are working artifacts. Preserve numbered releases; use a new output name for each release.

## Current Project Progress — v197

The user targets Silly Venture. The latest visual release is
`build/visual-prototype-v197.xex`; use its matching JSON. The replaceable
`visual-prototype-dev` pair is the development target. These are full demo
builds using the original v035 music, not replacements for the supplied player.
Use `docs/PLAN_STATUS.md` for remaining production work and V1–V7 status.
The plan audit `docs/AUDYT_BRAKOW_V144.md` verifies gaps against the actual
v144 callback: last ~90 seconds are placeholders; Act 1 still lacks Trevor
in the school background, and bar 92 changes phases rather than source/mirror.

V145 implements the user-approved story changes (2026-11-07): the third
ribbon shot is overhead and the thrown girl approaches the lens while the
court/bases recede; the boy shatters the backboard during the dunk; the last
outro shot at ticks 59085–59833 shows him on the floor with four orbiting
stars and fades to permanent black. In v193, this same image begins at tick
53850 as the planned credits/greetz background; the text overlays remain
unimplemented. The full final-shot timing remains unchanged.
See `docs/V145_WYRZUT_TABLICA_FINAL.md` for assets, memory and validation.
V146 removes the grid/court markings and all ribbon masks from the overhead
shot. Its preparation has quiet black ground; from tick 20662 the launch
uses compact player fireworks in side columns and missile sparks. Earlier
side/group/solo shots retain their ribbons. See `docs/V146_WYRZUT_FAJERWERKI.md`.
V148 supersedes v147's slow preparation: ticks 17950–20475 are animated group
dance, then one quick crouch, a front-view takeoff and an overhead approach.
The close-up arrives in under a second. Only the throw runs once; dance may
cycle. Both flight angles have white/cyan player wind streaks, moving narrow
missile trails and two side fireworks. See `docs/V148_DYNAMICZNY_WYRZUT.md`.

- Acts 1–3 have their core renderers (Act 1's planned background Trevor is
  still missing); act 2 now opens with the approved side-profile
  ribbon backstep in ticks 8975–11966. In v143 the girl moves across the frame
  from x=40 to x=128 together with all ribbon/spark HPOS registers, while
  the gym scrolls left in two depth layers. The former pompom dance is preserved as the
  independent `projects/pompom-dance` project, including its original artwork,
  twelve exact reference frames, player, build, tests and numbered v001 XEX.
  Act 2 also includes the approved three-shot ribbon
  dance in ticks 14959–20942: group, solo, group lift and launch. It replaces
  the old four pompom portraits. Do not restore the old portrait renderer.
- V142 stores 36 compact ribbon compositions (16 side, 20 later compositions)
  in the six original player banks 9–14. The previous dance used 96 KiB and
  later ribbon bitmaps another 40 KiB. Net recovery including extra controller,
  anchors and main code is 46,633 B (45.54 KiB), without reducing bank count.
  See `docs/V142_SZARFY_Z_BOKU_I_ARCHIWUM_POMPONOW.md`.
- V143 separates the side dancer from the background using eight masked
  2048-byte actors. Current net recovery relative to v141 is 29,901 B
  (29.20 KiB), after the movement data/code. See `docs/V143_PRZEJSCIE_Z_SZARFA.md`.
- V145 adds 864 B of backboard patches, 428 B of hero code, 812 B of final
  controller and 2560 B of final bitmap; removing dead pompom dispatch saves
  66 B of main code. Current net recovery vs v141: 25,303 B (24.71 KiB).
- V146's fireworks add 349 B of controller/shape data. Current net recovery
  vs v141: 24,954 B (24.37 KiB); still 64 banks and 36 ribbon compositions.
- V148 adds 128 B of wind data, 34 B of banked code and 21 B of unbanked
  palette code. Current recovery vs v141: 24,771 B (24.19 KiB), still 64 banks.
- Act 4 has the common-gym Trevor entrance, timed wind-ups/punch combinations,
  alternating BANG/BAM, coloured player cloud fragments and missile debris.
  Hit timestamps and hand sequence remain in `tools/trevor_polished.py`.
- Act 5 keeps the banana rotator at tick 32909 and shows both animation halves
  through tick 35900 (bar 96); the spiral tunnel then runs until the organic
  texture change at 40388. The organic tunnel holds through tick 41983 so the
  global cycle starts on a complete tunnel phase at 41984. Trevor mosaic at 41884 and
  eyes at 43379 remain unfinished. Acts 6–7 and credits/greetz overlays remain
  placeholders; the lying-boy backdrop now starts at 53850, and the full final
  shot and black ending retain their original 59085–59833 timing.
- V135 fixes the tunnel ball's PMG enable race. V136 introduces double-buffered
  ribbon PMG, V137 rainbow raster colours/sparks, V138 double-buffered impacts.
  Do not remove those protections when adding more effects.
- V140 adds double-buffered GTIA 11 fireworks and a skyline to both opening
  cards. The title appears I KNOW, THE BETTER, THE LESS, while its final
  top/middle/bottom layout stays THE LESS / I KNOW / THE BETTER. PMG masks
  protect both title layouts, including shadows and their dissolve.
- V141 raises both opening cards above the skyline and adds a pixel Żuraw
  landmark. Title rows start at visible raster lines 0/48/96, leaving the
  skyline below source row 49 clear of lettering and its extrusion.
- V144 supersedes that small skyline landmark with a 40×32 source-pixel
  Żuraw, half the active image's width and height, at (20,32) on the 80×64
  GTIA grid. Historic twin towers/timber hoods, cyan brickwork, warm roofs,
  black keylines. Artist rows now 0/48, title top/middle/bottom 0/33/66;
  title glyphs use one source row per glyph row. Words and shadows stay
  in source rows 0–31. Reveal order/times stay unchanged. Firework masks
  protect the whole crane silhouette as well as text, including dark parts.
  No extra Atari memory or code. See `docs/V144_DUZY_ZURAW.md`.
- V149 connects the left crane tower to the gatehouse and scales the whole
  silhouette to 36×29 source pixels at (22,35). Opening fireworks have rising
  rockets, radial bursts and falling fragments. They deliberately cross IN
  FRONT of both letters and crane, superseding the v140/v144 clipping masks.
  Reveal order, title layout and all scene ticks remain unchanged.
  New data/code consumes 1088 B across banks 40/41; net recovery vs v141 is
  23,683 B (23.13 KiB), still 64 banks. See `docs/V149_ZURAW_I_PIERWSZY_PLAN.md`.
- V150 replaces the pulsing tunnel/rotator ball with 16 distinct sphere
  rotations, curved seams, four neon panel inks, a rim and a reflected glint.
  The silhouette is fixed and opaque, including the tunnel's central hole.
  Colour phase advances every 16 player ticks. Satellite paths are unchanged.
  Two complementary masks reconstruct the four player planes; shared satellite
  tables and a 640-byte clear keep it in loader bank 2, `$7800–$7FFF` (2048 B).
  No new bank or main code; net recovery vs v141 is now 23,646 B (23.09 KiB).
  See `docs/V150_PSYCHODELICZNA_PILKA.md` for validation and previews.
- V151 implements user-authorized internal Act 3 retiming: preserve the
  ribbon/throw length through tick 20942, then tunnel/ball 20942–21690,
  dribble 21690–23186, fast dunk 23186–23934. Trevor still enters at 23934.
  The dunk's phase advances every 8 ticks instead of 16; keep all shatter stages.
  Do not restore the former 20942 dribble / 22438 dunk thresholds.
  ATARI ARENA replaces the school exterior in 2992–5984 and the hero's gym
  backdrop. The existing actors/paths remain; a large Fuji replaces NORTH
  on the girl's back, with a small Fuji in the side-profile shot.
  New sources/prompts are `act1_atari_arena_exterior_v151.*` and
  `act3_atari_arena_interior_v151.*`; `tools/arena_art.py` prepares native art.
  Still 64 banks. Main code +31 B, hero helper +15 B, packed rows -71 B;
  net recovery vs v141 is now 23,671 B (23.12 KiB). See
  `docs/V151_ATARI_ARENA_I_PRZEBITKA.md` for tests, memory and previews.
- V153 replaces the practice-shot, dribble and dunk ball with a compact
  opaque neon sphere: eight panel rotations, curved bright seams, glint and
  a darker rim. All three use the same 512-byte masks from `rainbow_ball`.
  Four player luminances are 6/10/12/14; paths and hand anchors are unchanged.
  No data/code growth, no extra bank. See `docs/V153_PILKA_RZUT_KOZIO_WSAD.md`.
- V155 fixes transparent exterior-boy hair/jacket from v151's component
  selection. Portrait alpha now comes from a complete silhouette, including
  black hair, connected magenta jacket and the clipped right edge. Do not use
  colour connectivity or black-as-transparency for these portraits.
  Regression checks both poses against original hair/jacket pixels.
  Main/hero code and all timing remain unchanged; packed rows now 10,764 B
  (163 B less than v153), net recovery vs v141 23,834 B (23.28 KiB).
  See `docs/V155_PELNA_MASKA_CHLOPCA.md`.
- V156 adds a tunnel-ball release after the lettering on every third Trevor
  hit (indices 2,5,8,...). BANG/BAM timing/alternation and all hit ticks remain.
  Ages 80–135 replace the player puffs with four large tunnel-ball rotations;
  missiles retain impact debris. The ball moves up/right from the splash.
  Action banks 24–39 store 512 B each at `$5E00–$5FFF`. Never install this
  payload in quiet bank 49: that area belongs to the final-boy controller.
  The shared Trevor helper is now 2556 B (`$6000–$69FB`), only 4 B free.
  Existing offscreen PMG preparation and early-blank publication are retained.
  Cost vs v155: 8192 B masks + 2737 B repeated helper growth = 10,929 B;
  net recovery vs v141 is now 12,905 B (12.60 KiB), still 64 banks.
  See `docs/V156_TREVOR_WYBIJA_PILKE.md`.
- V157 fixes gaps across all ribbon shots. Curve samples must be connected
  with rasterized segments: sampling alone skipped rows 26/38 in phase 0.
  All 64 player masks now have a full vertical span and one connected path.
  Missile sparks, launch fireworks and wind streams retain their sparse shapes.
  Stream size remains 5120 B; no RAM/code/bank/timing growth.
  See `docs/V157_CIAGLE_SZARFY.md`.
- V158 cycles eight PMG families after Trevor, ticks 32909–59084, with no
  ribbons: large ball, shot ball, city fireworks, BANG/BAM, cloud fragments,
  orbiting stars, launch wind/fireworks and glass shards. Each mode lasts
  512 player ticks (~2.57 s), full loop 4096 ticks (~20.54 s).
  V160 supersedes the original permanent ball guard and fireworks: every
  current effect now covers the hole itself. Earlier mosaic scenes keep v150 PMG.
  Loader bank 2's unused legacy Trevor artwork/code is replaced by the
  showcase; its historical generator is retained as `legacy_bank()`.
  Main code/ticks/bank count stay unchanged. See `docs/V158_CYKL_PMG.md`.
- V159 adds sparse ordered 4×4 dithering to banana shade transitions and
  a narrow coloured edge band of the tunnel fan. The fruit raster is fixed
  in texture coordinates, tunnel raster in screen coordinates. Black outlines,
  tunnel white crests/central hole and all PMG remain unchanged. Roughly 2%
  of pixels change, with no RAM/code/bank/timing growth.
  See `docs/V159_DELIKATNY_DITHERING.md`.
- V160 removes the separate central guard ball and all fireworks from the
  post-Trevor cycle. Eight modes remain, now with a red/pink beating heart
  instead of city fireworks and a solid wind rush instead of launch fireworks.
  All four players belong to the ACTIVE object; its own silhouette covers the
  tunnel aperture in every phase. Never restore a permanent ball behind modes.
  Compact ball, bubble, cloud, star, air rush and glass are centred/adapted
  so that their own opaque middle covers the hole. Earlier scenes are unchanged.
  See `docs/V160_SERCE_I_MASKOWANIE_EFEKTEM.md`.
- V161 removes v159 dithering from banana/tunnel artwork at the user's
  request. All 64 mosaic frames match v158 byte for byte. Other banks and
  unbanked RAM match v160; its heart, active-effect coverage and cycle remain.
  Do not restore dithering without a new user request. No memory/timing change.
  See `docs/V161_BEZ_DITHERINGU.md`.
- V162 withdraws the new post-Trevor PMG showcase, heart and its data.
  Rotator/tunnel use the SAME original `tunnel_ball` renderer as their earlier
  shots, including full hole-covering ball and missile satellites. No new cycle.
  Bank 2 `$4000–$77FF` is zero/free (14 KiB); only `$7800–$7FFF` remains.
  Retired source/tests live in `docs/archive/*pmg_showcase_v160.py`, outside
  the production builder and test discovery. Do not re-enable them.
  Every third Trevor hit now alternates TWO existing balls: large tunnel ball
  flies left, compact shot ball flies right. BANG/BAM and missile debris remain.
  The same 512 B per action bank holds two phases of each ball; no new masks.
  Trevor helper is 2557 B, ending `$69FC`, leaving 3 B to `$6A00`.
  Net recovery vs v161: 12,640 B; total vs v141 25,721 B (25.12 KiB).
  See `docs/V162_STARE_EFEKTY_I_DWIE_PILKI.md`.
- V163 supersedes v162's two copied impact masks. Every third hit now
  borrows the actual original rotator/tunnel renderer: all 16 ball rotations,
  original colours and BOTH paired missile satellites. The whole effect flies
  towards the nearest edge, according to the striking hand (4 left, 2 right).
  BANG/BAM, hit ticks and ages 80–135 remain. Other hits keep their clouds.
  Never read HPOS back: GTIA reads return collision latches. The original
  renderer accepts pose 96 and the signed horizontal offset in `$83EA`;
  positions are translated before its normal blanking-window publication.
  Nested unbanked trampoline calls restore bank selection and call operands.
  Removed all 16 duplicate 512 B ball tables. Trevor helper is 2466 B,
  ending `$69A1`, leaving 94 B before `$6A00`. Bank 2 adds only a 44 B
  entry adapter at `$4000–$402B`; its existing 2048 B helper stays at `$7800`.
  Further net recovery vs v162: 9695 B; total vs v141: 35,416 B (34.59 KiB).
  See `docs/V163_PILKA_Z_SATELITAMI.md`.
- V164 replaces the opening fireworks' short local rise with a full launch
  from visible y=190 to four upper-sky apexes y=36/44/56/72. Four staggered
  rockets rise for 64 player ticks, flash, expand into radial bursts, then
  drop fragments. Vertical anchors advance every four ticks; shape phases
  every 16; rainbow colours every eight, also during the explosion. Detached
  missiles spread sideways. Both title cards keep foreground PMG, fades,
  double buffers, bounded blanking publication and their original text/order.
  Each plasma-bank controller is now 1428 B, anchors 257 B, shapes still
  3072 B. Cost across both banks: 648 B; net recovery vs v141: 34,768 B
  (33.95 KiB). See `docs/V164_TECZOWE_RAKIETY.md`.
- V165 replaces pre-impact dunk droplets with four satellites centred on
  the moving ball: wide ellipse, tall reverse ellipse, twice-speed flattened
  ellipse and tilted reverse ellipse. Their 32-step phase uses player tick
  >> 3; missiles are double width and inherit the ball's four cycling inks.
  Only dunk phases 0–74 use orbits. First crack (phase 75) immediately restores
  the original glass-fragment trajectories and missile sizes; dribble unchanged.
  Live PMG rewrite now requires bounded VCOUNT 124–127, skipping late blanking.
  Hero helper is 2859 B, ending `$4B2A`; 85 B remain before `$4B80`.
  New orbit tables are 256 B at `$7E40–$7F3F`, after the board patches;
  192 B remain at the bank tail. Cost +463 B in loader bank 1 only; net
  recovery vs v141 is 34,305 B (33.50 KiB). No scene/tick/music changes.
  See `docs/V165_ORBITY_PRZY_WSADZIE.md`.
- V166 adds 14 real inbetween compositions to the three later ribbon-dance
  shots, using nine new anatomically drawn poses from the v166 3×3 source
  sheet. Insertions fall halfway between the original 46/47-tick intervals;
  original accents, camera cuts, throw and side shot remain unchanged.
  Original frame IDs 0–35 and final ID 36 stay fixed. Python preview IDs
  37–50 denote inbetweens; runtime keeps the original `$83ED` and uses
  `$83E5=$80` as the midpoint/cache flag. The selector restores original hand
  metadata on EVERY call or writes the new pose's matching hand anchors.
  New bitmap data is fast LZ: 16,886 B for 35,840 B raw. It prefers matches
  of 8+ bytes to reduce CPU setup. A 140 B decoder runs in bank 2 and 32–38;
  NMI preserves each active bank. Controller grows 9 B to 2246 B, ending
  `$5CC5` (10 B before the final controller). Main remains 2546 B in v166.
  See `docs/V166_PLYNNIEJSZY_TANIEC.md` and `build/v166-allocations.json`.
  At V166 the confirmed free bank regions totaled 31,623 B, not the historical
  net-recovery figures in earlier release notes. Do not treat the old
  bank 2 region or whole Trevor slots as free after this release.
- V167 cycles the Act 5 tunnel's bright highlight hue while retaining the
  banana palette. V168 morphs Trevor's tunnel frame between rectangle and
  oval in the existing background phases. V169 changes the Act 5 tunnel
  texture at tick 40388 from spiral bands to a radial star lattice, reusing
  frame slots 32–63. No bank allocation changes; main code is 2552 B, leaving
  8 B before `$1E00`. See the V167–V169 notes in `docs/`.
- V170 replaces the Act 1 boy-front art with a wink/whistle portrait and
  screen-resolution treble-clef/note overlays behind the walking girl. No
  bank allocation changes or tick changes. Shared scanline storage is now
  11,913 B across 309 rows; main code remains 2552 B. See
  `docs/V170_GWIZDAJACY_ZIOMEK.md`.
- V171 attempted four quarter-phase bitmap poses in the solo ribbon-dance
  shot, but placed their streams in player banks without a decoder. Playback
  through those frames could execute graphics bytes as code; that XEX is
  superseded. V172 keeps the same poses/ticks and moves their 3805 B streams
  to free tails in decoder-equipped loader indices 32–35. Selector remains
  1370 B at `$4040–$4599`, with six bytes before `$4600`. Group shots, side
  shot, accents and throw timing remain fixed. Confirmed free bank gaps:
  27,463 B. See `docs/V171_DODATKOWE_KLATKI_SOLOWKI.md` and
  `docs/V172_POPRAWKA_DEKODERA_TANCA.md`.
- V173 redraws those four solo follow-through poses to match their actual
  preceding midpoint and endpoint: arm descent, torso turn, rise from squat,
  and uncrossing into a wide stance. Same four ticks, selector, decoder routing
  and bank slots; art grows by 140 B. Confirmed free bank gaps: 27,323 B.
  See `docs/V173_DOPRACOWANIE_SOLOWKI.md`.
- Passing CPU tests and stereo POKEY comparison do not establish compo readiness,
  real FPS, physical-Atari playback or live raster stability. Preserve these
  distinctions in progress reports. Three v126 comparison tests are skipped
  when that archived XEX is absent; report the skips explicitly.

## Current Memory Ownership

V188 main code fills $1400–$1DFF (2560 B), with ZERO bytes before the row
pool at $1E00. Any further unbanked growth requires refactoring/relocation;
never overlap the row pool. Earlier 8-byte-headroom notes are historical.

All 64 expansion banks of the tested 1 MB configuration are allocated. Loader
indices below mean the `school_portrait_bank.bank_value()` indices, not PORTB
values or the original player's bank numbers. Never assume there is a free bank.

- Loader index 2: original rebound `$4000–$402B`; midpoint/quarter selector
  `$4040–$4599` (1370 B); compressed frames `$4600–$5AA6` and
  `$6000–$6E0E` (8886 B); decoder `$5E00–$5E8B` (140 B);
  original tunnel-ball helper/data `$7800–$7FFF` (2048 B).
  Free gaps total 3896 B after v178; largest is `$6E0F–$77FF` (2545 B).
- Loader indices 24–31: side actor pixels/masks `$4A00–$51FF` unchanged;
  `$5200–$53FF` remains free (4096 B total across eight banks).
- Loader indices 32–38: compressed midpoint frames start at `$4A00`,
  using 944/940/994/1303/1303/1265/1251 B respectively. V173 places four
  refined solo-quarter streams after those in indices 32–35: 983/1006/986/970 B.
  Tails to `$53FF` total 5975 B free. Each also owns decoder `$5E00–$5E8B`; only
  `$5E8C–$5FFF` (372 B per bank) remains free in that old ball slot.
- Loader indices 24–31 and 39: `$5E00–$5FFF` stays free (9 × 512 B).
  Combined with the seven 372 B tails this is 7212 B in former ball slots.
- Index 39: final-boy bitmap owns `$4A00–$53FF` (2560 B). Never clear it.
  All these known bank gaps plus six original player-bank tails total 27,323 B
  after v178. Original player-bank indices 8–13 each retain six compact
  ribbon frames at `$4000–$7BFF` and a free 1 KiB tail at `$7C00–$7FFF`.
- Index 49: quiet Trevor art `$4000–$53FF`, ribbon controller at `$5400`,
  Trevor engine `$6000–$69FF`, ribbon streams `$6A00–$7DFF`, anchor metadata
  `$7E00–$7F1F` (288 B), wind shapes `$7F20–$7F9F` (128 B).
  Ribbon/fireworks/wind controller is 2246 B, ending `$5CC5`.
  Engine growth must fit below `$6A00`; installers reject
  overlap. The v163 Trevor helper is 2466 B, leaving 94 B in its slot.
  `docs/V120_PRZEGLAD_PAMIECI.md` describes historical free space,
  some of which v142 recovered. Use this current map for availability.
- Index 49 also holds the final-boy controller at `$5CD0–$5FFB` (812 B),
  with only 10 B between controllers and 4 B before Trevor code at `$6000`.
  Preserve both code ranges; the installer rejects overlap.
- Index 1 (hero): code is 2859 B at `$4000–$4B2A`, bitmap/ball data
  `$4B80–$7E3B`. Three 48×24 board patches occupy `$7ADC–$7E3B`;
  85 B code gap remains. Dunk orbit tables occupy `$7E40–$7F3F` (256 B),
  with 192 B bank tail and 4 B between patches and orbit tables.
  Do not add full hero frames without a new budget.
- Main code occupies `$1400–$1DF1` (2546 B), with 14 B left before the
  scanline pool at `$1E00`. The old full-height pompom dispatch is removed;
  its independently archived project is unaffected. V151's unbanked
  `hero_cutaway` trampoline reuses the normal tunnel renderer. Its nested
  returns restore the hero bank, then the caller's bank. Preserve this order.
- Runtime reservation stays `$0C00–$0EFF`; the bank-safe masked compositor
  starts at `$0E00`, now routing midpoint frames before its original copy.
  Midpoint selector wrapper `$0D60–$0DAF`, copy entry `$0DB0–$0DB9`,
  private source/bank/step/anchor workspace `$0DC0–$0DCF`; DL keys remain
  `$0DFE–$0DFF`. Do not place assets in these formerly empty runtime gaps.
  Shared-row pool still begins at `$0F00`. Side-dancer cache keys include
  translation as well as pose/layout; midpoint keys add `$83E5` to the tag.
- Plasma indices 40–41 now also contain fireworks in their formerly empty
  tails: 1428-byte controller at `$6C00–$7193`, commit entry `$7000`,
  shapes `$7400–$7FFF` (3072 B), vertical anchors `$7280–$7380` (257 B). Do not allocate those tails as free memory.
  Firework preparation runs before plasma composition; publication only swaps
  the complete PMG and registers. Keep `PRIOR=$C1` and fifth-player mode off
  for normal PMG colours over GTIA 11. Do not cut fireworks against letters
  or the crane: the user explicitly requested complete foreground bursts.
  Four players use 16 × 32 rows each and 64 moving vertical anchors; missiles
  use 16 × 64 upper-sky rows with a fixed zero anchor and their own source
  pointer table. Installers check code/anchor/shape overlap.
- PMG uses two 640-byte spans: `$0980–$0BFF` and `$8980–$8BFF`. The prefixes
  of their 1 KiB PMBASE regions may hold other data; clear only PMG spans.
  The second span is excluded from the static scanline pool.
- ANTIC bitmap buffers are unbanked `$9000` / `$B000`; display lists are
  `$8000` / `$8400`. Prepare inactive bitmap/PMG buffers, then commit during
  an early bounded blanking window. Merely testing `VCOUNT >= 124` permits
  late entry and is insufficient to protect a lengthy live PMG rewrite.
- The ribbon rainbow helper is unbanked and reentrant. It runs after existing
  music ticks, only in scene 14. Keep NMI scratch private to the stack and
  preserve foreground PORTB/registers. In flight frames 12–15 it keeps players
  0/3 white/cyan for wind. Do not add music updates to palette DLIs.

## Build, Test, and Development Commands

Install `requirements-dev.txt` into a virtual environment. Run `make all PYTHON=/path/to/venv/bin/python` for the replaceable working build and `make check PYTHON=/path/to/venv/bin/python` for required tests. Run `tools/check_playback.py` to compare full-track stereo POKEY in Atari800. `ATARI_TEST_XEX` selects another XEX (with matching JSON) for tests and the CPU profiler.

The current local test interpreter is `/tmp/opencode/tliktb-venv/bin/python`
when present. Full music comparison currently uses
`tools/check_playback.py --seconds 20` with Atari800 PAL/1088XE and Altirra OS.
For sprites, check active-buffer ownership and moving-VCOUNT regressions in
addition to final raster pixels. Relevant tests include `test_ribbon_buffers`,
`test_tunnel_raster`, `test_trevor_bang` and music-NMI injection tests.

- `ls -lh *.xex`: inspect available executables and sizes.
- `sha256sum less-i-know-release-v035.xex`: record the binary checksum before comparisons.

To run locally, load the XEX in Altirra configured for 65XE, PAL, 1 MB expanded RAM, and stereo POKEY. Record the memory expansion configuration used.

## Coding Style & Naming Conventions

Preserve the existing Markdown structure and Polish terminology when updating the specifications. Use `$` hexadecimal notation for Atari addresses, such as `$D301`.

No formatter, linter, or source indentation standard is configured. Establish consistent formatting when adding code. The proposed asset convention uses `snake_case` with act prefixes, for example `act2_hearts_tile.bin`; formats include `.bin`, `.pal`, `.pmg`, `.fnt`, and compressed `.zx0` files.

## Testing Guidelines

Run automated tests and emulator playback comparisons for engine changes. py65 does not model ANTIC DMA or real raster deadlines; distinguish CPU costs from observed FPS. Keep V1–V7 status in `docs/PLAN_STATUS.md` accurate. Verify v035 addresses instead of reusing v024 addresses without checking.

Test each build in the target configuration and listen for missed music ticks throughout playback. Record results under the relevant V-number, distinguishing direct observations (`[ODCZYT]`), inferences (`[WNIOSEK]`), and assumptions (`[ZAŁOŻENIE]`).

## Commit & Pull Request Guidelines

Git history is unavailable in this checkout, so existing commit conventions cannot be established. Use concise, imperative subjects describing one change.

Pull requests should explain the change, affected acts or memory regions, and validation results. Include screenshots for visual changes and playback observations for timing changes.

## Timing & Memory Constraints

Use the player tick counter for scene synchronization. Preserve four evenly spaced music updates per PAL frame. Verify PORTB restoration and bank ownership before changing memory use. Obtain human confirmation before changing act boundaries, tick positions, or production priorities.


V174 corrects the first arena shot's portrait mask: it must not turn the
source-image black backdrop into opaque pixels over the ATARI ARENA sign.
Whistle glyphs sit above the lettering. No timing or bank ownership changes.
The build uses 292 shared rows (of 309) and 2552 code bytes. See
`docs/V174_CZYTELNY_SZYLD_ARENY.md`.


V175 changes the alternating Trevor bubble words to BNG! and BAM. Keep the
impact glyphs four planes wide, with the exclamation mark inside the existing
bubble; scene timing and bank ownership do not change.


V176 replaces the arena-walk cutout with the left-facing Atari-jacket sprite
and reverses the actor and background pan (right to left). Keep scene ticks and
boundaries unchanged. Preview and build stats are in `docs/V176_SPACER_WZDLUZ_ARENY.md`.


V177 installs production RGBA character layers for the opening boy/girl and
all basketball poses. Masks are thresholded source alpha, with no guide
polygons; basketball backboard and net are redrawn on the clean arena plate.
The build uses 292 of 309 shared rows (10,919 B) and 2,552 code bytes. These
17 remaining shared rows are the hard limit; any new full-screen source art
must stay banked or reduce existing row use. Timing and bank ownership remain
unchanged. See `docs/V177_GRAFIKA_PRODUKCYJNA_POSTACI.md`.

V178 restores the original opening shot sizes and placements from v176 while
keeping its corrected sign mask. The V177 basketball alpha sprites remain in
use. The separate arena pan still moves right to left. V178 uses 307 of 309
shared rows (12,084 B), 2,552 code bytes; timing and bank allocation do not
change. See `docs/V178_KADRY_OTWARCIA.md`.

V179 preserves black hair and jacket pixels inside the boy's silhouette mask.
His neutral look remains before the girl passes; the wink, puckered lips and
music notes follow her pass. Existing framing, ticks and bank allocation stay
unchanged. Repeated rows reduce use to 286 shared rows (11,034 B), with 2,552
code bytes. The source composition preview is `build/v179-opening-frames.png`;
it is not emulator capture. Tests and emulator playback were not run. See
`docs/V179_MASKA_I_REAKCJA_CHLOPCA.md`.

V180 extends the Act 5 tunnel shot by moving its start from bar 104 (tick
38892) to bar 92 (tick 34404). The banana rotozoomer now ends at bar 92; the
existing bar 108 texture change and bar 112 transition remain unchanged. No
act boundary, later scene tick, code size or bank allocation changes. See
`docs/V180_DLUZSZY_TUNEL.md`. Its timing was superseded by v193: rotator now
runs through bar 96 before the tunnel.

V181 restores the exact v175 side-walk frames from archived XEX bank data
(`assets/art/reference/v175/arena-pan.bin`) and the v175 encounter shot order.
Keep these camera scales and framing. Only the receding girl positions change:
her final feet align with the left entrance at logical (82,52), rather than
the adjacent pillar. Boy torso guide pixels are opaque as well as black hair.
The six focused CPU/render tests pass; emulator audio check was blocked by
the installed Atari800 AppImage requiring FUSE. Uses 275 shared rows (10,630 B)
and 2552 code bytes; bank allocation unchanged. See
`docs/V181_WEJSCIE_DZIEWCZYNY_V175.md`.

V182 stages the boy reaction explicitly: original forward-facing portrait at
ticks 2992 and 4114, turned gaze during the foreground pass (4488) and the
receding shots (4862,5236), whistle/wink/notes only at doorway tick 5610.
Use `school_story.boy_poses()` for the three distinct poses. Walk, doorway
trajectory, framing and all ticks remain as v181. Seven focused CPU/render
tests pass. Build uses 316 unique rows, 12,153 B row storage, 2552 B code.
Historical row-count ceilings in earlier notes are not allocator limits:
actual byte packing and checked region bounds determine capacity. Bank
allocation unchanged. See `docs/V182_REAKCJA_CHLOPCA.md`.

V183 removes ALL bitmap melody overlays from the opening boy shot. Notes,
paired notes and a treble clef now fly out of his mouth and rise on four
players; missiles form short detached sparkle tails. Only scene 12 (tick
5610 until practice at 5984) enables the melody. Use whistle_pmg.py, not
bitmap glyphs. Loader index 0 now owns its 835 B helper at $6A00–$6D42,
inside the gap after the old pom helper ending $69AB and before cleanup
$6F00. The banked rainbow_ball entry has a 10 B scene-12 dispatch addition.
Both PMG buffers ($0980–$0BFF / $8980–$8BFF) alternate; completed planes
are published in bottom blanking. No act ticks or further bank contents
change; all other 63 banks are byte-identical with v182. Main code 2552 B,
316 shared rows / 12,158 B. Thirteen focused CPU/render tests pass; no new
emulator playback (known FUSE obstacle). See docs/V183_NUTY_PMG.md.

V184 advances the doorway/whistle shot and PMG emission by one beat: tick
5516 instead of 5610 (94 ticks, about 0.47 s). Use the shared
`school_story.WHISTLE_START` constant for both scene 12 and whistle_pmg.START.
The final shot lasts until the unchanged practice start at 5984. Earlier
poses, girl trajectory and all later cuts stay unchanged. See
`docs/V184_WCZESNIEJSZY_GWIZD.md`.

V185 starts the whistle and PMG melody at tick 4862 (bar 13), immediately
after the foreground pass; the turned neutral pose still appears at 4488.
Scenes 10–12 keep the whistle until practice at 5984 (about 5.6 s).
WHISTLE_START now controls the melody start; the final doorway placement
is restored to its original tick 5610 independently. PMG advances every
eight ticks, giving each note about 2.56 s of upward flight and keeping
the complete interval below the 8-bit phase wrap. The helper now occupies
839 B at $6A00–$6D46 in loader index 0; the entry dispatch covers scenes
10–12 (14 B). Main 2552 B; 316 rows / 12,174 B. Fourteen focused tests pass.
CPU animation: build/v185-whistle.gif. No new emulator playback. See
docs/V185_DLUZSZA_MELODIA.md.

V186 synchronises puckered lips and first PMG note at WHISTLE_START=4862;
WHISTLE_END=5610 is the doorway arrival. Only scenes 10–11 whistle; scene 12
returns to the turned neutral face and disables PMG. Two finite staggered
waves fan into separate curved trajectories, fade and end before arrival;
there is no endless respawn. Puckered mouth is explicitly drawn at logical
(119,33), and old source-image rays outside the face are cleaned. Preserve
v175 framing, girl scales, entrance target and pan. Bank 0 owns the 1119 B
helper $6A00–$6E5E (161 B remain before $6F00 cleanup). All other 63 banks
are identical with v185. Main 2552 B, 298 shared rows / 11,480 B.
Fifteen focused CPU/render tests pass. Full-track stereo POKEY comparison
passes (6,220,440 identical bytes). Atari800 works with environment
APPIMAGE_EXTRACT_AND_RUN=1; this resolves the earlier FUSE obstacle.
Full-suite status and pre-existing failures are recorded in
`docs/V186_DOMKNIETA_SCENA_SPOTKANIA.md`.

V187 makes melody symbols twice as wide and tall: SIZEP=1 (16 logical pixels),
24 double-line PMG rows (up to 48 scanlines). Hold luminance 14 through phase
32; fade only phases 33–35. Rainbow hues alternate with white flashes.
Missiles use SIZEM=$55 for wider sparkle tails. Curves clear the face faster
and spread over the sky; the emission anchor compensates for the large
glyph size. Start/end remain 4862/5610, character frames unchanged.
Whistle helper now 1167 B at $6A00–$6E8E; 113 B before $6F00 cleanup.
Main 2552 B, 298 rows / 11,480 B. Sixteen focused tests pass. See
`docs/V187_DUZE_NUTY_PMG.md` and `build/v187-whistle.gif`.

V187 stereo POKEY playback comparison passed for the entire track:
16,221,456 identical bytes with v035, Atari800 PAL/1088XE / Altirra OS.
Only loader bank 0 changed; the other 63 banks match v186 exactly.

V188 fixes actual PMG blanking: generic colors previously wrote GRACTL=0
and DMACTL=$22 on every callback before the whistle helper prepared its
back buffer and waited for the next blanking. A moving-beam trace showed
267–313 missing scanlines per update. Scenes 10–11 now bypass those resets,
keeping front DMA enabled until the new buffer is published. Exits still
reset normally. Eight bytes added to main (2560 B, exact budget); whistle
art/helper bank 0 byte-identical with v187. Bank-call targets relocate with
the main labels. tests/test_whistle_raster.py traces full callback lifetimes
at eight PAL raster offsets, three ticks and two stall cases (48 cases);
old v187 fails the new regression, v188 passes. Nineteen focused tests and
full-track stereo POKEY comparison pass (16,336,440 identical bytes).
See docs/V188_CIAGLE_PMG_BEZ_STROBO.md for full-suite status and limits.

V189 restores exact basketball art/keyframes and ALL three board-fracture
patches from v175. `assets/art/reference/v175/basketball.bin` holds 12,988 B
from loader index 1 at $4B80–$7E3B. basketball_hero.frames() reconstructs
eight original poses, including the four distinct dribble-arm phases;
shattered_frame() applies the archived fracture patches. Do not replace the
board with independently placed procedural geometry: character, ball, board
and break patches must retain v175 coordinates. The v177 RGBA basketball
sheet is preserved as source but is no longer a build input. Hero code,
ball paths, satellites, scene ticks and v188 PMG fix stay unchanged. Only
bank 1 differs from v188; the other 63 banks are byte-identical. Bank 1
still has 85 B before DATA, 4 B between art and orbits, and 192 B after
orbits; a full extra frame costs 2240 B, so no new full keyframe is added.
23 focused tests pass, including archived runtime-frame and PMG equality
with v175. Full-track POKEY comparison passes (14,992,848 identical bytes).
See docs/V189_KOSZYKOWKA_I_TABLICA_V175.md for full-suite status.

V190 replaces BNG! with BUM, alternating with BAM. Tunnel frames 48–63
now use continuous warped liquid folds instead of radial/ring checkerboard.
No bank allocation or timing change. Main remains 2560 B. See docs/V190_BUM_I_ORGANICZNY_TUNEL.md.

V191 centres BOTH three-letter words in the 32-clock bubble (+4-clock
lettering offset). impact_anchor(index) precomputes deterministic xorshift
scatter for all 40 hits: ±6 logical X pixels and ±3 double-line PMG rows
(±6 scanlines), independently around the correct hand anchor. The offset
is held for the entire hit; bubble, word and cloud share the same origin.
No per-frame random jitter or arbitrary screen positions. Trevor helper
shrinks to 2500 B, leaving 60 B below $6A00. Main 2560 B, banks unchanged.
24 targeted tests and full-track stereo POKEY comparison pass. See
`docs/V191_DYMKI_PRZY_PIESCI.md`.

V192 derives U in BUM directly from the vertically inverted A in BAM,
replacing the crossbar with the side-stem row. Same glyph cell and size;
centering, bounded hit anchors, code sizes and timing unchanged.
See docs/V192_U_Z_ODWROCONEGO_A.md.

V193 changes timeline boundaries only: the banana rotator runs from bar 88 to
96 (32909–35900), showing both existing animation halves. The spiral tunnel
starts at bar 96; the organic texture change stays at bar 108 and Act 5 cuts
remain at bars 112/116. The lying-boy scene starts at bar 144 (53850) beneath
the reserved credits/greetz windows; the 8C full-shot/fade still starts at
bar 158 (59085). No artwork, effect renderer, or effect data changed.

V194 aligns the post-Act-5 motif cycle to tick 41984 rather than beginning at
bar 112 / tick 41884. The latter falls 100 ticks before the global tunnel
phase and exposed bananas for about half a second. The organic tunnel now
holds through tick 41983, then the unchanged cycle resumes on spiral tunnel.
No artwork or effect generator changed. `docs/V194_CIAGLY_CYKL_ROTATORA.md`.

V195 ball dithering was reverted at the user request; keep v194 ball masks
and colours. V196 aligns the dribble ball centre at X=84 (previously 97),
with two 94-tick fast bounces and one 186-tick slow bounce per 374-tick cycle.
The same remapped phase drives the arm and ball. Dunk and glass remain v175;
scene boundaries unchanged. 21 focused tests pass. See
`docs/V196_KOZLY_DWA_SZYBKIE_JEDEN_WOLNY.md`.

V197 alternates the finale orbit between stars and the opening whistle's notes/treble
clef every 256 player ticks (1.28 s). Four glyphs share the existing head orbit,
rainbow colours, inactive PMG buffers and final fade. Glyphs retain the original
8-bit silhouettes with single PMG rows for the smaller finale framing. Final
controller: 809 B at $5CD0, 48 B at $69C4 and 95 B at $7FA0 in bank 49;
net +140 B versus v196, no new banks. See docs/V197_NUTKI_W_FINALE.md.
