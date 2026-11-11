# Repository Guidelines

## Project Structure & Module Organization

This project is an Atari XE 1 MB audiovisual demo for “The Less I Know The Better.” The checkout contains planning documents, a source pipeline, tests and a prebuilt player:

- `TLIKTB_Atari_Timeline_v2.md`: act boundaries, musical events, and player tick synchronization.
- `TLIKTB_Technical_Constraints.md`: hardware limits, memory layout, proposed asset formats, and verification tasks V1–V7.
- `less-i-know-release-v035.xex`: the supplied executable.

`tools/` generates NMOS 6502 code and assets; `tests/` executes callbacks with py65; `assets/` contains source artwork. `build/visual-prototype-dev.xex` and its JSON are working artifacts. Preserve numbered releases; use a new output name for each release.

## Current Project Progress — v244

The user targets Silly Venture. The latest visual release is
`build/visual-prototype-v244.xex`; use its matching JSON. The replaceable
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
stars and fades to permanent black. In v240, the same fixed lower image
and terminal begin at tick 51850; text ends at 59085, and the final fade
and black ending retain their original timing.
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
- Act 5 keeps the banana rotator at tick 32909, with continuous 32-frame
  full turns through tick 35900 (bar 96); the spiral tunnel then runs until the organic
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
  Hero helper is 2892 B, ending at exclusive `$4B4C`; 52 B remain before `$4B80`.
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

V244 main code occupies $1400–$1DFC (2557 B), with only THREE bytes before
the row pool at $1E00. Any further unbanked growth requires refactoring;
never overlap the row pool. Earlier headroom figures are historical.

V244 adds lifetime ownership: title banks 40–48 are only title assets until
tick 2992. Starting at tick 3072, retired banks 40–47 become 32 raw peeled
banana frames; compressed banana banks 3–10 become 32 raw bunch frames.
Bank 48 is staging space ($4000–$4EFF) and raw-helper templates
($6000–$67FF). No 65th bank and no other scene's gaps are consumed.
Do not add post-title assets to banks 40–48. The retired intro draw region
is also reused: worker $E580–$E956, scratch $EA00–$EAFF, private state
$EB00–$EB1F; FLAG=$0DDF. Typewriter at $EB44 stays untouched. Intro restart
or seeking back into the title after preparation requires reloading the XEX;
this is a forward-playback lifetime overlay. Fresh late seeks use the
existing compressed renderer; they do not represent warmed playback costs.
Normal playback finishes preparation well before the first rotator.


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
  overlap. The current Trevor helper is 2500 B, leaving 60 B before `$6A00`.
  `docs/V120_PRZEGLAD_PAMIECI.md` describes historical free space,
  some of which v142 recovered. Use this current map for availability.
- Index 49 also holds the final-boy controller at `$5CD0–$5FFF` (816 B),
  with only 10 B between controllers and 4 B before Trevor code at `$6000`.
  Preserve both code ranges; the installer rejects overlap.
- Index 1 (hero): code is 2892 B at `$4000–$4B4B`, bitmap/ball data
  `$4B80–$7E3B`. Three 48×24 board patches occupy `$7ADC–$7E3B`;
  85 B code gap remains. Dunk orbit tables occupy `$7E40–$7F3F` (256 B),
  with 192 B bank tail and 4 B between patches and orbit tables.
  Do not add full hero frames without a new budget.
- Main code occupies `$1400–$1DFC` (2557 B), with 3 B left before the
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

V198 changes only the orbiting glyph palette: 19 vivid GTIA colours cycle every
256 ticks, with a four-colour phase offset between planes. Orbit, timing, masks,
fade and memory use are unchanged. See docs/V198_TECZOWE_KOLORY_FINALE.md.

V216 adds credits/greetz in existing windows (53850–56842–59085). See
`docs/V216_CREDITS_GREETZ.md`. No expansion-bank gaps are consumed. Loader
`$3E58–$3FC3` (364 B) and 1738 B of compressed resources occupy explicit
unbanked player gaps; resource tail starts at `$3FC4`. Scratch `$0DD0–$0DD7`
must stay outside shared row storage. Finale controller now fills exactly
`$5CD0–$5FFF` (816 B): do not grow it. On finale entry, the held bitmap owns
`$9000`; the retired second bitmap buffer holds compressed staging at
`$B000`, saved normal DLIST at `$B800–$BAFF`, private caption DLIST at
`$BC00–$BE53`, and unpacked text/font/code at
`$C000–$CEFF`. These addresses must never receive static assets at load time.
The 5-row ANTIC-2 band keeps the complete bitmap; caption DLI positions are
1/79/157/235 lines, preserving four 78-line music intervals. Restore only the
inactive DLIST and publish inside VCOUNT 124–127. Do not read write-only
ANTIC registers to infer the active DLIST or PMG bank; use engine state.

Caption DLIST must stay within one 1 KiB ANTIC DL page. The normal lists end
at `$8249`/`$8649`; bytes after these are static artwork, not DLIST padding.
When restoring, copy exactly 586 B per normal list, never 768 B. Invalidate
bitmap and DL cache keys after restoring the reusable framebuffer.

V218 keeps the lower 235-line outro layout and PMG +32-line shift through
the final fade; after tick 59085 replace text pointers with blank records,
never restore the higher framing. Normal-DLIST reset at `$C340` is for seeks
out of the outro only. Top bitmap rules at source rows 5/9 are removed.
ANTIC-2 terminal palette uses hue `$C0`, foreground luminance `$0E` and `>`
prompts; bitmap palette is restored at its raster boundary. See
`docs/V218_STALY_KADR_TERMINAL.md`.

V222 adds true typewriter output, cursor and Enter/scroll. See
`docs/V222_TERMINAL_PISANIE.md`. Reserved intro-helper size is now 1824 B:
its original code ends at `$EB43`, terminal code fills `$EB44–$EBDF`, and
shared scanline storage begins at `$EBE0`. Do not grow either helper without
checking all owners. Dead original UI `$23CE–$2450` holds line timing/lengths;
`$23CD` is RTS. Disabled font initializer `$2D00–$2D26` now stores packed
data: its `$218F` call must stay disabled. Terminal screen is `$BF00–$BFC7`
and scratch extends through `$0DD8`. The cursor uses ANTIC inverse-space,
not the finale PMG. Restore old UI/font code before ever re-enabling it.

V225 replaces foreground terminal palette polling with a display-list split.
ANTIC 4 draws green COLPF0 letters on true COLBK black; do not write COLPF2
from terminal foreground code. Extra DLI after line 41 is palette-only:
`outro_palette` router `$2451–$248F` skips music and restores the NMI stack,
while the original 1/79/157/235 music ticks remain. Normal music entry calls
the router in place of its old WSYNC (same 3 B). Code occupies retired UI
and old font-copy space; never re-enable these routines without relocating
it. Cursor is glyph `$5F`, font 3×7. Trevor entrance uses `$48/$68/$2A`, same
base as the punches; helper size/labels preserved. See
`docs/V225_PALETY_TERMINAL_I_TREVOR.md`.

V227 final-boy controller is 814 B (`$5CD0–$5FFD`). PMG back-buffer choice
uses RAM shadow `$83E8`, never a read from write-only PMBASE `$D407`. Final
Y tables include +16 PMG bytes (+32 raster lines) directly. Do not reapply
the shift in outro_text: PMG RAM must not be written after publication.
First entry disables PMG while preparing inherited buffers; warm updates
write only the inactive buffer. See `docs/V227_CZYSTE_PMG_NAD_GLOWA.md`.

V230: fixed-column six-row terminal (one status plus five typed history rows),
no horizontal wobble. First eight BLACK bitmap scanlines are replaced by the
extra text row, leaving all character pixels at the same physical position.
Caption DLI now occur at 1/49/79/157/235; only 49 is palette-only (VCOUNT 28).
Ink $CE, rare foreground-only white/noise pulse. Router ends $249A; player
variables $249C–$24A4 must NEVER hold code/data. Intro reservation 1888 B,
typer $EB44–$EC05, static row pool starts $EC20. PMG grip data has a fixed
centre stem in every phase; base pose-3 and quarter-sheet palm annotations
are corrected and snapped to the individual actor's skin. Side anchors stay
unchanged. Ribbon PMBASE also uses RAM shadow $83E8. See
`docs/V230_TERMINAL_I_CHWYTY_SZARF.md`.

V231 directs only the existing post-Trevor tunnel windows, ticks 41984–53849.
72 half-bar/phrase-fill cues select existing spiral/organic frames, forward
or reverse playback and normal/double speed. Original banana windows and
all earlier effects remain unchanged; lying-boy entry stays at 53850.
Director is 337 B at $EC20–$ED70, reservation 384 B; intro reservation is
now 2272 B and shared static rows start at $EDA0. Scratch $0DDA belongs
to the director; do not reuse it during the callback. Main code is 2524 B.
No new expansion banks or effect bitmaps. Ball/satellites retain the
existing masks and cover the tunnel hole at every tested cue boundary.
See `docs/V231_DYNAMICZNY_TUNEL_PO_TREVORZE.md`.

V233 adds a single wink (overhead frame 14) then puckered kiss (frame 15),
with an eight-phase shaded heart leaving the lips at tick 20662. The launch
still ends at 20942. Facial artwork changes stay inside the existing head;
framing, flight and dancer keyframes are retained. During the final kiss,
four PMG players draw the growing/yawing heart; all four missile air trails
remain. Earlier launch stages retain their player wind and side bursts.
Heart uses 992 B at $7C00–$7FDF in original player-table bank index 10
(ribbon tail index 2); the other ribbon tails remain untouched. Total tail
space left is 5152 B. The unbanked trampoline is 31 B at $0F00–$0F1E;
RUNTIME_END is now $0F40, protecting it from static-row allocation.
Private foreground scratch $0DDB/$0DDC must not be used by NMI code.
Ribbon controller is 2252 B, ending $5CCB; final-boy code still starts
$5CD0. Main is 2551 B, leaving 9 B before $1E00. Heart colours are restored
by the existing reentrant rainbow helper after music DLI; do not add a
music tick or banked palette lookup. See `docs/V233_OCZKO_BUZIAK_SERCE.md`.

V234 uses seven terminal rows: status plus six typed history rows. Extra
text replaces eight more BLACK bitmap lines (16 skipped in total); the
boy, PMG orbit and every remaining bitmap pixel keep their physical Y.
Private DLIST bitmap starts $BC16, has 176 rows, footer $BE26 and 554 B
total. DLI positions 1/57/79/157/235; only 57 is palette-only, VCOUNT 32.
Screen rows occupy $BF00–$BFEF. Timing has 48 entries (96 B) at
$23CE–$242D; lengths moved to 47 unused control-glyph bytes $C828–$C856,
loaded with the font. Do not install these statically over the second
framebuffer. Typer is 195 B, $EB44–$EC06. Compressed outro is 1743 B;
loader is 373 B at $3E58–$3FCC, only one byte before the $3FCE resource
gap. Do not grow it without auditing both owners. Main remains 2551 B;
no expansion-bank gaps were consumed. See
`docs/V234_SIODMY_WIERSZ_TERMINALA.md`.

V235 adds `HUMAN VISION / LLM CODE` to credits page 1's sixth row and
`AI TOOLS / ATARI SOUL` to the SV page. Existing text schedules, greetz,
framing and act boundaries remain. Raw text has 38 lines, 47 display slots;
timing stays 48 entries. Compressed outro is 1795 B. Resource staging now
also owns retired UI $242E–$2450 (12 B used, 35 B reserved); timing must
end by $242E, palette router still starts $2451. Adjacent $2C81–$2D00 and
$2D00–$2E00 gaps are merged for chunk copying, so the bootstrap remains
373 B despite the added staging region. Total staging capacity 1818 B;
main remains 2551 B, no expansion-bank gaps consumed. See
`docs/V235_LLM_AI_W_CREDITS.md`.

V236 fixes banana rotation at both sources: mosaic pixels now use phase
directly for the angle (360 degrees/32 frames), rather than phase/4 (90
degrees with a discontinuous wrap). Act 5 masks the clock with 31 and
no longer loops its 16-frame halves separately or forces bit 4 at bar 92.
All scene ticks and post-Trevor tunnel cuts remain unchanged. Banana tile,
palette, zoom, PMG masks and the eight tunnel banks are preserved; only
the banana-oriented bitmap data and Act-5 frame selection change. Same
32 stored banana frames, same bank allocation; main shrinks to 2521 B
(39 B before $1E00). See `docs/V236_PELNY_OBROT_BANANOW.md`.

V239 alternates the bunch and a half-peeled single banana by visible
banana-window appearance: 12288 bunch, 14336 peeled, the whole Act-5
32909–35900 bunch, then alternating post-Trevor windows from 43008 peeled.
Both motifs keep 32 full-turn frames and the same tick/16 clock. The
peeled cycle starts at the opposite zoom/angle phase to balance bank
payload sizes; it never loses a frame or switches motif mid-appearance.
The existing eight banana banks (loader 3–10) now store both motifs in
byte-RLE, not raw 4-frame payloads. Runtime entry stays $7C00; banana-only
helper $7840–$7BFE, entry $7C00–$7C6B, copy $7C80–$7C9B, decoder
$7D00–$7D90, eight pointer pairs $7F80–$7F8F. Data occupies $4000 up
to $7840; bank 0 fills that region exactly. Total compressed graphics
111114 B, code/tables 1256 B per bank; 9910 B remains across these eight
banks. No other bank gaps or additional banks are used. Main remains
2521 B. Scratch $0DDD owns the variant key and $0DDE the private cache;
$0DC0/$0DC1 is the existing foreground source pointer. Never borrow these
in NMI. Banana entry invalidates the shared $83FA key on return, and
checks layout/ownership before reusing its private cache, preventing
collisions with school and compressed-ribbon renderers. Tunnel banks
remain byte-identical to v236. v237/v238 were discarded slow LZ
prototypes; use v239. See `docs/V239_KISC_I_OBRANY_BANAN.md`.

V240 implements the user's explicit 10-second-earlier terminal request:
outro_text.START/final_boy.START are 51850 (formerly 53850). Text END is
still 59085, demo END/fade still 59833/59705. Eight page starts are
51850/52850/53850/54850/55697/56544/57391/58238: three credits pages and
five complete greetz paragraphs. Each page types in 55–180 ticks then
holds for 667–900 ticks; no history scroll. Prefix is `>`, cursor glyph
$5F is a baseline underscore and always follows tick bit 6, including
during typing and read holds. Typer 172 B at $EB44–$EBEF. Timing now
loads WITH the font into unused control glyphs: 55 entries / 110 B at
$C828–$C895; 54 lengths $C8A8–$C8DD. Never install these statically over
the reusable second bitmap. Retired UI $23CE–$2450 now belongs entirely
to compressed staging (49 B used, 131 B capacity); $23CD remains RTS,
router starts $2451, live player vars $249C remain protected. Total
staging capacity 1914 B, payload 1832 B, bootstrap still 373 B. Post-Trevor
director stops at 51850, 60 cues / 301 B at $EC20–$ED4C; reservation
unchanged. Main still 2521 B, all 64 bank payloads identical to v239.
Seven-row layout, boy/orbit position and four music updates are unchanged.
See `docs/V240_WCZESNIEJSZY_TERMINAL_I_PLANSZE.md`.

V241 removes runtime RLE from both banana motifs. Their 128×128 source
patterns contain opposite, point-symmetric pairs of unchanged fruit shapes;
zoom repeats per half-turn. Sixteen unique raw images per motif therefore
represent all 32 angular samples exactly, with continuous 15→16 and 31→0
steps. This changes the background arrangement/density; it does not claim
32 unique bitmap payloads. Eight banks hold four 3840-byte frames each;
bunch banks 0–3, peeled banks 4–7 within the banana bank group. Each has
a 981-byte helper at $7C00–$7FD4, leaving 43 B (344 B total, superseding
v239's 9910 B free-space report). No runtime decoder or RLE streams remain.
The selector maps the logical phase/motif to the raw bank without changing
the PMG clock. New unbanked routines occupy existing helper reservations:
$EBF0–$EC11 (34 B) and $ED4D–$ED8F (67 B). Typewriter must end by $EBF0;
post-Trevor director must end by $ED4D. Asserts and allocation validation
protect both. Main is 2518 B. Private $0DDD/$0DDE cache ownership remains;
no zero-page scratch is borrowed. Both variants cost ~47k CPU cycles warm,
matching tunnels; the regression cap is now 62k including cold setup.
Eight tunnel banks remain byte-identical to v240. Terminal and all scene
ticks remain v240. See `docs/V241_SZYBKIE_BANANY_BEZ_RLE.md`.

V242 fixes repeated normal-DLIST restoration during ticks 51850–53849.
The intro invalidate/seek guard still compared against the old hardcoded
53850 after v240 moved the outro to 51850. Every warm callback therefore
published the old higher normal list, then rebuilt/published $BC00 again.
Use outro_text.START in BOTH bytes of that guard, never a copied literal.
New regression traces repeated callbacks across the complete early window:
$D403 must not be rewritten after the first publication, normal DLISTs
must not be restored, and the lower bitmap mapping stays fixed. This test
fails v241 immediately at tick 51854 and passes v242. No graphics, timing,
memory layout, PMG or music changes. See `docs/V242_STALY_KADR_BEZ_RESETOW.md`.


V243 restores all 64 dense banana bitmaps byte for byte from v240. The user
rejected v241's sparse point-symmetric layout; do not restore it to save CPU.
Both motifs retain 32 independent phases, original zoom/orientation and the
same timeline clock. Banana banks 3–10 use page-bounded RLE: input Y and
output X advance independently; literals copy two bytes and fills eight per
loop. Packet boundaries cannot cross either source or destination pages;
token zero advances the input page, and exactly 15 output pages end decoding.
The helper remains at $7840, entry $7C00, selector $7C80, decoder $7D00,
fill loop $7E00, dispatch $7F00 and frame pointers $7F80. Scratch is
$0DC0–$0DC1 and $0DC4–$0DC6; no zero-page or music scratch is borrowed.
Private cache $0DDE and key $0DDD still isolate bananas from other renderers.
Only eight banana banks and 13 bytes of the unbanked selector differ from
v242; all other banks (including tunnels, PMG and the fixed outro) match.
Packed graphics 113981 B, code/tables 1667 B per bank, free 3755 B in these
same eight banks. See `docs/V243_GESTE_BANANY_SZYBSZY_DEKODER.md`.


V244 eliminates runtime decompression during normal banana playback. The
background worker prepares one 256-byte page per callback during ticks
3072–11775, then both motifs use the same raw COPY_PAGES path as tunnels.
Bootstrap is only armed while tick high byte is $0C; a fresh development
seek to a later scene does not destroy live title code. Original eight
archive banks are expanded in reverse frame order; frames overlapping
compressed input use bank 48 as temporary raw storage. Peeled frames and
helper templates are copied before any corresponding archive is overwritten.
Every job preserves PORTB and avoids framebuffer/PMG/display registers.
Atari800 PAL/1088XE reaches READY at tick 8609. Act 2B's scene threshold is
tick 11968 (bar 32); the first measured mosaic selection callback is tick
11976 and sees READY=2. Native phase trace shows all 32 phases, 63 consecutive
bunch transitions and 38 peeled transitions without skips. Max warm CPU:
bunch 47323, peeled 47402, tunnel 47245 cycles. Graphical assets/timeline
remain v243. `docs/V244_SUROWE_BANANY_I_BANKI_PO_TYTULE.md` describes the
lifetime map, tests and the distinction between startup and runtime budgets.

V244 validation: make check 189/189, 151.2 s; full-track stereo POKEY
10589472 bytes identical to v035. No physical Atari run has been made.
