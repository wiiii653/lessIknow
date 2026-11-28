> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# v016 — cheerleader during the performance

## Realisation

[READ] New scene 2C: ticks 14960–20943, cuts every 1496 ticks.
A blonde in a cheerleader uniform, with pompoms, in four poses during the
performance in the hall. European comic style, natural facial proportions.
Source: `assets/art/source/act2_cheer_performance_v015.png`.

[READ] The variants in the jacket were set aside for possible use:
`assets/art/source/act1_blonde_portraits_reserved_v014.png` (outdoors)
and `assets/art/source/act2_crush_gym_portraits_v014.png` (hall).
They were not inserted at the start of the demo.

## V2 / V3 — memory

[READ] Bank 8, offsets `$0000–$0B0F`, remain identical to the original.
Before insertion the builder checks the `$FF` fill in `$0B10–$1FFF`.
At `$4B10` the portrait renderer runs, `$4F00` restores the dance PMG,
`$4FC0–$5FFF` contains four 80×52 images (4160 B).
The first image is unpacked into the inactive buffer, then a 192 LMS
list is built. The static frame is not copied again.
The NMI restores the bank of the interrupted code, also while the helper
is executing in extended memory. The scene clock remains the player counter.

## V1 / V6 — verification

[READ] 29 tests OK: images of all four shots, cache, blinking,
return after restart, and the existing music, bank and raster tests.
In Atari800 PAL `-1088xe` the shot memory dumps and their persistence were checked,
along with the final transition and the restart. The portrait raster agrees with the source.

[READ] Full stereo POKEY test:

```sh
make check PYTHON=/tmp/tliktb-girl-venv/bin/python
APPIMAGE_EXTRACT_AND_RUN=1 python3 tools/check_playback.py --demo build/visual-prototype-v016.xex --seconds 12
```

9 238 464 identical bytes, about 2573.4 s of emulation, the whole piece covered by the
comparison with the original. After tick 20944 the return to the kaleidoscope is
a placeholder for the basketball player act.

[ASSUMPTION] Listening and profiling on physical Atari remain to be done. The colour and pixel
proportion preview is an approximation: `build/v016-performance-preview.png`.

## Graphics and prompt

The built-in image_gen was used, in accordance with the imagegen skill. Final prompt:

```text
Use case illustration-story. NEW production 2x2 contact sheet for an Atari audiovisual demo. Input1 is character face identity and European ligne claire drawing reference ONLY; input2 is cheerleading uniform and performance poses reference ONLY, do NOT adopt its cartoon/anime face. Show the SAME dark blonde/blonde European teenage CHEERLEADER DURING HER PERFORMANCE INSIDE SCHOOL GYM in four expressive medium closeups. Natural European comic proportions, small realistically sized eyes, natural nose, clear bold black contours. Pink sleeveless cheerleading uniform with cyan V-neck trim and pink/cyan pompoms, pink hair bow, blonde hair with movement. Absolutely no jacket, no varsity collar, no casual clothes. Four panels: 1 front, one pompom lifted beside shoulder, energetic smile; 2 looking left midturn, raised arm and pompom toward upper corner; 3 looking right midroutine, other arm raised, relaxed smile; 4 front, both pompom hands beside shoulders, confident smile. Frame from chest or waist up so costume and movement visible, face large and center; keep eyes open. Upper arms and pompoms visible, do not obscure face. Tall INDOOR windows, wooden wall bars, roof beams, basketball backboard in sparse gym backgrounds. No outdoor scenery. Match clean European bande dessinee drawing, NOT manga/anime, NOT giant eyes, NOT doll face. Four flat palette colors black #000000 hotpink #ff32a0 cyan #00dcff peach/gold #ffbe96; hair uses peach/gold large masses with thin black shadows. Broad shapes readable at80x52 each panel. EXACTLY four equal landscape panels 2 columns 2rows, no gutters, no borders, no text.
```
