# The Less I Know The Better — Atari XE demo

## Build and run

Run `make` with Python 3 and ImageMagick installed to produce
`build/visual-prototype-dev.xex` (replaceable working build). Run Atari800 with stereo POKEY enabled:

```sh
atari800 -1088xe -pal -nobasic -run build/visual-prototype-dev.xex
```

Install `requirements-dev.txt` in a virtual environment and run
`make check PYTHON=/path/to/venv/bin/python` for the required 6502 tests.
Numbered releases remain preserved; the current visual release is
`build/visual-prototype-v261.xex`; the matching numbered XEX is
`releases/less-i-know-demo-release-008.xex`. They are byte-identical.
V261 adds KEY-G and FALCON to the existing greetz without changing timing.
See `docs/V261_KEY_G_FALCON.md` and `docs/PLAN_STATUS.md`.
The current post-Trevor montage is the v256 layout restored in v260; its map
is `docs/AKTUALNY_MONTAZ_V256.md`. V260 withdrew the four comic cutaways from
v257. See `docs/V260_ROTATORY_BEZ_TREVORA.md`, `docs/V259_TREVOR_BEZ_SZACHOWNICY.md`,
`docs/V258_NAPIS_AI_SLOP_OGNJEN.md`, and `docs/V257_KOMIKSOWY_MONTAZ.md` for
the superseded experiment and recent text changes.
See `docs/V256_LOTY_PILEK_TREVORA.md`, `docs/V255_WYRAZNE_ORBITY_FINALU.md`,
`docs/V252_OCZY_DZIEWCZYNY.md`, `docs/V251_WIDOCZNE_ZMIANY_ORBITY.md`,
`docs/V250_PLYNNE_ORBITY_TEKSTU.md`, `docs/V249_PILKI_I_SATELITY_TREVORA.md`,
`docs/V248_WCZESNIEJSZE_OUTRO_PELNY_ROTATOR.md`, `docs/V247_TREVOR_PILKI_I_CIOSY.md`,
and `docs/V246_SERCE_CZASTECZKI.md`.
The Silly Venture preparation notes distinguish release 008 from the older
v260 candidate bundle: `docs/SV2026WE_PRZYGOTOWANIE.md`.
See `docs/V244_SUROWE_BANANY_I_BANKI_PO_TYTULE.md` for the banana-cache
preparation and `docs/V240_WCZESNIEJSZY_TERMINAL_I_PLANSZE.md` for the original
terminal page schedule.
See `docs/V243_GESTE_BANANY_SZYBSZY_DEKODER.md` and `build/banana-v243-variants.png`.
See `docs/V242_STALY_KADR_BEZ_RESETOW.md`.
See `docs/V241_SZYBKIE_BANANY_BEZ_RLE.md` and `build/banana-v241-variants.png`.
See `docs/V239_KISC_I_OBRANY_BANAN.md` and `build/banana-v239-variants.png`.
See `docs/V236_PELNY_OBROT_BANANOW.md` and `build/bananas-v236.gif`.
See `docs/V235_LLM_AI_W_CREDITS.md`.
See `docs/V234_SIODMY_WIERSZ_TERMINALA.md`.
See `docs/V233_OCZKO_BUZIAK_SERCE.md` and `build/launch-kiss-v233.gif`.
See `docs/V231_DYNAMICZNY_TUNEL_PO_TREVORZE.md` for tunnel texture, direction and speed changes synchronized to musical phrases.
See `docs/V230_TERMINAL_I_CHWYTY_SZARF.md` and `docs/V227_CZYSTE_PMG_NAD_GLOWA.md` and `docs/V225_PALETY_TERMINAL_I_TREVOR.md` (green letters on black, DLI palette split, matching Trevor entrance colours).
See `docs/V196_KOZLY_DWA_SZYBKIE_JEDEN_WOLNY.md`.
See `docs/V194_CIAGLY_CYKL_ROTATORA.md` for the timing update. Earlier releases: `docs/V193_TIMELINE_ROTOR_I_CREDITS.md`, `docs/V189_KOSZYKOWKA_I_TABLICA_V175.md`, `docs/V188_CIAGLE_PMG_BEZ_STROBO.md`, `docs/V187_DUZE_NUTY_PMG.md`, `docs/V186_DOMKNIETA_SCENA_SPOTKANIA.md`, `docs/V185_DLUZSZA_MELODIA.md`, `docs/V184_WCZESNIEJSZY_GWIZD.md`, `docs/V183_NUTY_PMG.md`, `docs/V182_REAKCJA_CHLOPCA.md`, `docs/V181_WEJSCIE_DZIEWCZYNY_V175.md`, `docs/V180_DLUZSZY_TUNEL.md`, `docs/V179_MASKA_I_REAKCJA_CHLOPCA.md`, `docs/V178_KADRY_OTWARCIA.md`, `docs/V177_GRAFIKA_PRODUKCYJNA_POSTACI.md`, `docs/V176_SPACER_WZDLUZ_ARENY.md`, `docs/V175_TREVOR_BNG.md`, `docs/V174_CZYTELNY_SZYLD_ARENY.md`, `docs/V173_DOPRACOWANIE_SOLOWKI.md`, then `docs/V172_POPRAWKA_DEKODERA_TANCA.md`, `docs/V171_DODATKOWE_KLATKI_SOLOWKI.md`, `docs/V170_GWIZDAJACY_ZIOMEK.md`, `docs/V169_ZMIANA_TEKSTURY_TUNELU.md`, `docs/V168_MORFUJACA_RAMKA_TREVORA.md`, `docs/V167_TECZOWY_CYKL_KOLOROW.md`, and `docs/V166_PLYNNIEJSZY_TANIEC.md`.
See `docs/V165_ORBITY_PRZY_WSADZIE.md` and `build/v165-dunk-orbits.gif`.
See `docs/V164_TECZOWE_RAKIETY.md` and `build/v164-title-fireworks.gif`.
See `docs/V163_PILKA_Z_SATELITAMI.md` and `build/v163-rebound-left.gif` / `build/v163-rebound-right.gif`.
See `docs/V162_STARE_EFEKTY_I_DWIE_PILKI.md` for the removed cycle, recovered memory and previews.
See `docs/V161_BEZ_DITHERINGU.md` for the artwork restoration.
See `docs/V160_SERCE_I_MASKOWANIE_EFEKTEM.md`, `build/v160-beating-heart.gif` and `build/v160-pmg-cycle.gif`.
See `docs/V159_DELIKATNY_DITHERING.md` and `build/v159-subtle-dither.png` for the texture update.
See `docs/V158_CYKL_PMG.md` and `build/v158-pmg-cycle.gif` for the complete cycle.
See `docs/V157_CIAGLE_SZARFY.md` and `build/v157-connected-ribbons.gif` for the fix.
See `docs/V156_TREVOR_WYBIJA_PILKE.md` and `build/v156-ball-punch.gif` for the new impact.
See `docs/V155_PELNA_MASKA_CHLOPCA.md` and `build/v155-opaque-boy.png` for the mask fix.
See `docs/V153_PILKA_RZUT_KOZIO_WSAD.md` for the shared sphere and previews.
See `docs/V151_ATARI_ARENA_I_PRZEBITKA.md`, `build/v151-arena-exterior.gif` and
`build/v151-launch-tunnel-dunk.gif` for the new setting and montage.
See `docs/V150_PSYCHODELICZNA_PILKA.md`, `build/v150-ball-rotator.gif` and
`build/v150-ball-tunnel.gif` for the new ball animation.
See `docs/V149_ZURAW_I_PIERWSZY_PLAN.md` and `build/v149-intro.gif` for the opening update.
See `docs/V148_DYNAMICZNY_WYRZUT.md` for the restored dance and fast action.
See `docs/V146_WYRZUT_FAJERWERKI.md` for the quiet background and launch bursts.
See `docs/V145_WYRZUT_TABLICA_FINAL.md` for the new scenes, source images,
prompts and validation. V166 adds 14 compressed inbetweens; v172/v173 add and
refine four solo-dance quarter phases. The old 27,323 B free-gap report is a
v178 snapshot and is not a current allocation figure.
See `docs/V144_DUZY_ZURAW.md` for the large crane, compact upper lettering and
the historical PMG protection, superseded by v149 foreground bursts.
See `docs/V143_PRZEJSCIE_Z_SZARFA.md` for the moving actor.
See `docs/V142_SZARFY_Z_BOKU_I_ARCHIWUM_POMPONOW.md` for the extraction
and the independent `projects/pompom-dance` archive. See `docs/V141_GDANSKI_ZURAW.md`
for the raised lettering and Żuraw skyline, `docs/V140_MIEJSKIE_FAJERWERKI.md`
for the fireworks and title order, `docs/V138_BANG_BAM_ROZPAD.md`
for the impacts, `docs/V137_TECZOWE_SZARFY.md`
and `docs/V136_TANIEC_Z_SZARFAMI.md` for the new ribbon dance. See `docs/V127_OPTYMALIZACJE.md` for
CPU measurements and validation. To test an archived build, set
`ATARI_TEST_XEX=build/visual-prototype-v127.xex`; its matching JSON is required.

## Opening sequence

| Music ticks | Approximate time | Scene |
| --- | --- | --- |
| 0–1495 | 0–7.5 s | TAME IMPALA over plasma, city skyline and PMG fireworks |
| 1496–2991 | 7.5–15 s | I KNOW enters first, then THE BETTER, then THE LESS at the top; final title layout preserved |
| 2992–3552 | 15–17.8 s | Boy facing camera |
| 3553–4113 | 17.8–20.6 s | Blonde girl passes the ATARI ARENA facade |
| 4114–4487 | 20.6–22.5 s | Boy facing camera again |
| 4488–5983 | 22.5–30 s | Girl appears at the left, then recedes toward ATARI ARENA with a Fuji on her back; boy turns after her |
| 5984–6980 | 30–35 s | Basketball player close-up |
| 6981–7977 | 35–40 s | Shot toward the basket |
| 7978–8974 | 40–45 s | Girls stretching at the wall bars |
| 8975–11966 | 45–60 s | Side-profile ribbon dancer crosses left to right; gym scrolls left with floor parallax, rainbow PMG ribbons and sparks move with her |
| 11967–14958 | 60–75 s | Breathing, color-cycling kaleidoscope |
| 14959–20941 | 75–105 s | Group/solo ribbons, more group dance, then one fast front/overhead throw with player wind, missile trails and fireworks |
| 20942–21689 | 105–108.75 s | Short spiral-tunnel cutaway with the neon ball, after the unchanged throw |
| 21690–23185 | 108.75–116.25 s | Low-angle dribble in ATARI ARENA, animated arm and PMG ball |
| 23186–23933 | 116.25–120 s | Fast dunk breaks the backboard: cracks, split panel, glass fragments and missile debris; spinning rainbow ball and light flash |
| 23934–28908 | 2:00–2:25 | Trevor fight, ending after 13 complete BUM/BAM hits and ball flights |
| 28909–31899 | 2:25–2:40 | 32-frame banana rotator |
| 31900–36387 | 2:40–3:02 | Spiral tunnel |
| 36388–37983 | 3:02–3:10 | Organic tunnel |
| 37984–39378 | 3:10–3:17 | Musically directed rotator/tunnel montage |
| 39379–40126 | 3:17–3:21 | Girl's four-phase eye close-up |
| 40127–49849 | 3:21–4:10 | Moving rotator/tunnel montage; v257 comic cutaways are withdrawn |
| 49850–52849 | 4:10–4:25 | Three credits pages above the fixed lying boy |
| 52850–59084 | 4:25–4:56 | Five greetz pages, with a blinking underscore cursor |
| 59085–59832 | 4:56–5:00 | Defeated boy, four orbiting PMG stars, fade to black |
| 59833 onward | 5:00 onward | Black picture; original music DLI layout retained |

The opening cards emerge from dark as full-screen GTIA 11 plasma with ordered dithering between hues. Each word emerges through an ordered raster and dissolves unevenly at the end. The artist lettering changes into the title while the same plasma continues behind it. Sixteen phases, cumulative text masks and dissolve masks occupy nine additional expansion banks; the current demo uses all 64 banks available on the tested 1 MB configuration. Compact lettering occupies the upper half; a 36×29 pixel Gdańsk Żuraw occupies the lower half, with cyan brick towers, warm tiled roofs and dark projecting timberwork. Complete PMG fireworks pass in front of the text and crane.
Artist and title each last 1496 ticks. The ATARI ARENA exterior runs from
2992–5983; the girl appears at four scales with a Fuji on her jacket, and the
boy's gaze/whistle reaction follows her pass. `tools/school_story.py` stages
the poses. From tick 5984 the camera cuts inside for three illustrated gym
shots, with cuts at 5984, 6981 and 7978; dance starts at 8975. A rainbow PMG
ball and missile spray animate the second shot. Source storyboard:
`assets/art/source/act1_practice_storyboard_v011.png`. This is the current
ATARI ARENA setting, not the former school/NORTH description in older notes.
The side-profile shot uses eight illustrated poses and sixteen gym phases.
The girl faces left and steps backwards from x=40 to x=128; windows
and wall bars move left, with the floor moving at half speed. Four players
draw rainbow ribbons and missiles add sparks. The later three shots gain four
compositions, bringing all ribbon footage to 36 compact 2560-byte frames.
These fill 90 KiB of the original six dance banks. Moving the later ribbon
frames out of Trevor banks and replacing the old 96 KiB dance recovers
46,633 bytes net in v142. V143 uses eight masked actors to move her independently
of the gym. V145 adds the approved story beats, leaving 25,303 bytes of net
recovery compared with v141 in v145. V146 replaces overhead ribbons with
fireworks and removes the court grid. V148 restores dance before the rapid
two-angle throw and adds air streaks. V149 refines the opening fireworks;
V150 adds the new 16-phase sphere; V151 adds the arena and cutaway.
All 64 expansion banks are allocated; historical free-gap totals above do not
describe v261. V244 reuses title banks 40–48 for banana playback after the
title, and later releases add further banked scene data. Do not infer current
free space from old net-recovery figures; use the latest build metadata and
the relevant release notes. See `docs/V244_SUROWE_BANANY_I_BANKI_PO_TYTULE.md`,
`docs/V247_TREVOR_PILKI_I_CIOSY.md`, `docs/V249_PILKI_I_SATELITY_TREVORA.md`,
`docs/V252_OCZY_DZIEWCZYNY.md`, and `docs/V256_LOTY_PILEK_TREVORA.md`.
The original pompom scene survives as a self-contained
project in `projects/pompom-dance`, with exact reference frames and a playable
`build/pompom-dance-v001.xex` inside that project.
`make` rebuilds the replaceable `visual-prototype-dev` pair. Preserve numbered
XEX releases and their matching JSON metadata; the v261 build metadata is
`build/visual-prototype-v261.json`. Scene timing and 6502 code are generated by
`tools/build_bitmap_sequence.py`.

## Continuous raster and memory

The two opening cards use ANTIC F with GTIA 11. Subsequent scenes use ANTIC E.
The original four music updates per PAL frame remain at raster lines 0, 78,
156 and 234. Display lists and PMG effects use inactive buffers and bounded
publication; the NMI wrapper restores the interrupted foreground bank.
Ribbon footage keeps its composition cache while PMG ribbons and sparks move.
The post-title banana worker prepares raw frames during ticks 3072–11775 by
reusing retired title assets; this is a forward-playback lifetime overlay, not
a warm-start guarantee for arbitrary late seeks. See
`docs/V244_SUROWE_BANANY_I_BANKI_PO_TYTULE.md`.

Current v261 metadata reports 2,560 bytes of main code (`$1400–$1DFF`), 298
unique shared rows (11,494 bytes), runtime helpers through `$0F3F`, and the
static row allocator beginning at `$1E00`. The exact generated row addresses
are in `build/visual-prototype-v261.json`. All 64 expansion banks are allocated;
older memory maps and free-gap totals are historical, not allocation authority.
For later bank overlays see the v247–v260 notes and `AGENTS.md`.

For the additional school frames, the executable uses RAM under OS ROM. The
asset INIT in `tools/os_ram.py` temporarily disables ROM, copies data into
`$C000–$CFFF` and `$D800–$FFFF`, then restores OS ROM before returning to the
loader. Runtime entry at `$13E0` disables OS ROM permanently for the demo.
The selected music-bank values retain their bank bits but have OS-enable bit 0
cleared. The RAM hardware NMI vector points to the bank-preserving wrapper at `$1BA7`,
which enters the original DLI at `$2218`; VBI remains disabled. Runtime no longer
calls the OS. Music data remains unchanged: banks 1–7 and offsets `$0000–$0B0F` of bank 8
are byte-identical. The old four performance portraits have been removed from
verified unused offsets `$0B10–$1FFF`; cleanup code remains there. The last
8 KiB holds the practice atlas. Banks 9–14 now hold 36 compact ribbon frames.
The original screen countdown digits were relocated to
`$83F0–$83F4`; its instruction timing is preserved. The old meter UI and font
initialization are disabled, freeing `$3300–$3BFF` for static artwork. `$D000–$D7FF` remains hardware.

Runtime layout (current high-level map):

- `$0C00–$0F3F`: runtime helpers; `$1400–$1DFF`: main scene callback and
  tables; `$1E00`: start of the shared-row allocator.
- `$0980–$0BFF` and `$8980–$8BFF`: alternating PMG buffers; clear only the
  owned spans, not their PMBASE prefixes.
- `$9000` and `$B000`: unbanked bitmap buffers; `$8000` and `$8400`:
  double-buffered display lists, each within one 1 KiB page.
- OS-RAM loader and intro assets have lifetime-dependent ownership; the outro
  reuses the retired framebuffer. Consult the current release notes before
  placing data in any formerly unused region.

Each 40-byte bitmap row stays within a 4 KiB DMA page. During dance, the CPU
reads video banks through `$4000–$7FFF`; the NMI wrapper restores bank
ownership around every music update. ANTIC always reads unbanked RAM. The
older standalone kaleidoscope can still be built with
`make build/kaleidoscope.xex`.

## Verification and artwork

Run `make check` for display-list and music-bank checks. Install optional
`requirements-dev.txt` into a virtual environment and use
`make check PYTHON=.venv/bin/python` to execute the 6502 callback, verify live
scanlines, scene boundaries, the readable Fuji jacket mark, ROM-loader behavior,
and the side-profile and three-shot ribbon compositions;
the original solo/duo/trio reference checks live in `projects/pompom-dance`.

Run `python3 tools/check_playback.py` for a full-track stereo POKEY comparison
with the original player in headless Atari800. The test aligns recordings once
at the first nonzero stereo sample to exclude differing startup silence, then
compares all common bytes without further alignment or dropped samples. It
requires at least 305 seconds of music. Increase `--seconds` if needed.
Physical-hardware and listening tests remain separate.

`tools/render_sequence_preview.py` (requires py65) executes the asset INIT and
scene callback, then renders live display lists into `build/*-raster.ppm`,
including blank raster lines and the hardware player masks. Preview RGB colors
approximate the hardware.

Original artwork is in `assets/art/source/`. Ribbon dancers use the front v136
and side-profile v142 sheets, sampled into 160×64 compositions with keylines.
School artwork uses 160×64 source pixels
and three output scanlines per source row; the girl's back sprite is composited
before packing the frames. Earlier small dance PNGs/GIF are previews only.

## Performance closeups (v016)

The following notes describe historical releases. The four performance
closeups were replaced by ribbons in v136; the earlier full-height pompom
dance was extracted into its own project in v142. Use `AGENTS.md` and the
current release notes for present memory ownership and scene content.

The 2C scene uses four views of the blonde cheerleader performing in the gym,
in her pink/cyan uniform with pompoms. The illustration follows European comic
proportions. Cuts remain at ticks 14960, 16456, 17952 and 19448; the scene ends
at 20944. Each 80×52 image expands horizontally and repeats rows to fill the
raster. Held frames update only PMG, with brief eye blinks and a swaying hair
accent. Leaving this scene restores the original dance PMG, including restart.
Source: `assets/art/source/act2_cheer_performance_v015.png`. Earlier jacket
portraits are reserved assets, not used in this scene. See `docs/V016_PERFORMANCE.md`.

The v019 school portrait cut uses one additional video bank and keeps the gym
cut at tick 5984. See `docs/V019_SCHOOL_CUT.md` for staging and bank details.

The v020 rainbow ball uses four colored player bands and four missile spray
streams in ticks 6981–7977. Bank 15 now loads 16 KiB, including the PMG
routines; see `docs/V020_RAINBOW_BALL.md` and `build/v020-rainbow-ball.gif`.

In v021 the ball is twice as wide and tall (16×32 logical pixels) and makes
one flight over the entire 997-tick shot. Eight rotating panel/seam masks
provide spin. See `docs/V021_SLOW_SPINNING_BALL.md` and
`build/v021-slow-spinning-ball.gif`.

In v023 all four performance closeups have animated pompom strands and
individual pink/cyan, violet/turquoise, red/blue and magenta/green palettes.
Skin and blonde-hair colors are preserved. Local patches occupy the remaining
part of video bank 15; see `docs/V023_ANIMATED_POMPOMS.md` and
`build/v023-pompoms.gif`.

Act 3 is implemented in v024 with six illustrated body poses and a hardware
player/missile ball. Bank 16 holds the actor frames and renderer. See
`docs/V024_BASKETBALL_HERO.md` for memory, validation, source artwork and prompt.

Act 4 is implemented in v027. The seventeenth bank is found by an alias probe
that restores the original bytes of all sixteen existing banks. See
`docs/V027_TREVOR_AWAKENS.md` for validation, memory layout and artwork prompt.

The v029 mosaic replaces the static kaleidoscope with 64 geometric rotozoom
and tunnel frames, beat accents and changing palettes. It uses 16 additional
video banks (33 total), copied into inactive unbanked framebuffers. Scene
boundaries and PMG basketball effects are unchanged. See `docs/V029_MOSAIC.md`
and `build/v029-mosaic.gif` for preview and full validation.

In v031 the tunnel has a spinning basketball at its vanishing point: four
players form its shaded body and seams, and four missiles orbit as colorful
sparks. No extra banks or scene timing changes. See `docs/V031_TUNNEL_BALL.md`
and `build/v031-tunnel-ball.gif`.

In v032 the tunnel ball has bright complementary rainbow panels and black
seams, with wider, brighter satellites in a third hue. See
`docs/V032_RAINBOW_BALL.md` and `build/v032-rainbow-ball.gif`.

In v033 the school cutaway shows the girl in profile mid-stride and lasts
187 ticks longer; the following foreground entrance retains its timing.
See `docs/V033_SCHOOL_SIDE.md`.

In v035 the existing school portrait is cut out and animated over a wider
reconstructed background, with separate pan speeds and wind in her hair.
See `docs/V035_SCHOOL_PARALLAX.md` and `build/v035-school-pan.gif`.

In v038 the mosaic and tunnel use 161 distinct hue pairs throughout the
track. See `docs/V038_MOSAIC_PALETTES.md` and `build/v038-palettes.png`.

In v039 all mosaic palette pairs are selected for color separation and
brightness contrast. See `docs/V039_MOSAIC_CONTRAST.md`.

In v040 three anchored strands sway independently while the girl’s original
hair silhouette remains fixed. See `docs/V040_SCHOOL_HAIR.md`.

In v041 the dunk holds its wind-up longer, then cuts faster between the
airborne poses; the PMG ball follows the hand until release at the rim.
See `docs/V041_DUNK.md` and `build/v041-dunk.gif`.

In v042 the PMG basketball and satellites sweep from the center to both sides
of the rotator and return to the tunnel center. See `docs/V042_ROTATOR_BALL.md`.

In v044 Trevor uses four detailed comic illustrations and moving missile
glints, replacing the very low-resolution sprite silhouette. See
`docs/V044_TREVOR_POLISH.md` and `build/v044-trevor.gif`.

In v046 the PMG basketball gently bobs in both axes in the tunnel while
covering its center; satellites follow it. See `docs/V046_TUNNEL_BOB.md`.

In v049 Trevor’s existing punch poses are cut out over an animated expanding
tunnel; see `docs/V049_TREVOR_TUNNEL.md` and `build/v049-trevor-tunnel.gif`.

In v051 Trevor’s punch produces an animated PMG comic BANG splash. See
`docs/V051_TREVOR_BANG.md` and `build/v051-trevor-bang.gif`.

Trevor raises the appropriate fist before fast combinations of right and left punches,
including repeated strikes from the same hand. The rhythm mixes one-and-a-half- and two-beat intervals; the comic burst and particles have longer holds. Mirrored wind-up and forward punch frames reuse established artwork; the BANG burst and departing
particles share one position, and the tunnel has moving edge glints.
See `docs/V090_TREVOR_ZAMACHY.md`.

Dribbling now shares one gym background. Once both display buffers are prepared,
pose changes update a 76×56 region containing the boy (1,064 packed bytes).
The second full-screen dribble bitmap is replaced by that region, freeing
1,176 bytes inside the hero bank. Trevor action poses use matching skin
brightness and stable rim lighting; see `docs/V106_TREVOR_I_KOZLOWANIE.md`.

Dribble correction v110: four articulated arm poses follow contact, push,
release and recovery, while the body and gym stay fixed. The patch is now
44×28 (308 bytes). The display-list buffer base is refreshed on every patch
update; live sequential playback is tested over two bounces.

Trevor v111 keeps the body registered across tunnel phases, cleans isolated
fist pixels, and uses a darker tunnel for contrast. The full 40-impact
sequence is checked on live alternating buffers; the final hit ends without
a wind-up for a nonexistent next punch.

The entrance now stays in the quiet poses until the action boundary. The first
wind-up begins at that boundary and the first impact follows 32 ticks later.
See `docs/V112_TREVOR_KOLEJNOSC.md`.

Dribbling v115 uses arm cutouts from the original illustrated v024/v100 poses,
preserving elbow, wrist and fingers. Two eased intermediate samples follow
the same PMG ball phase. The 308-byte arm patch and stable background remain.

Title v117 uses large two-line TAME / IMPALA and taller song-title lettering.
Solid per-letter inks and a narrow coloured extrusion remain readable over
the moving, dithered plasma; transparent pixels preserve the background.

For a current checklist against the original timeline and V1–V7 verification
items, see `docs/PLAN_STATUS.md`.
