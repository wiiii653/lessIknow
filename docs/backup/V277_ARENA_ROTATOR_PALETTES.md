> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](../README.md) for active instructions.

# V277 — stronger rotators and a new palette before the arena

The rotator shades keep the order and rhythm of the changes. The brighter pulse
phase is darker than before, and the second colour has a controlled brightness
margin: the pairs remain distinguishable. This gives a stronger impression of
colour on PAL, whose saturation is not a separate GTIA register parameter. The
yellow bananas keep the v275 palette.

The shots of the meeting before the arena and of the boy's reaction (scenes
8–12) now use a warm `$38`, a blue `$88` and a bright `$2C`. The setting is in
the existing banked helper; before the whistling code the checked `$6900`
boundary remains. The other scenes receive the earlier palette.

The stereo build `releases/less-i-know-demo-release-015-stereo.xex` uses the
compact AVG loader and a late start; no other sound versions were built. The new
palette and this build have not yet been evaluated on physical Atari.

[READ] Atari800 PAL/1088XE: 16 234 920 identical stereo POKEY bytes compared
with v035; covers the whole track. Targeted tests: 50/50; full suite: 200/200 in
144.522 s.
