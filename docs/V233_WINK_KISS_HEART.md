> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V233 — wink, kiss and a spatial heart in the throw

## Image and synchronisation

- 20615–20661: penultimate close-up phase — one eye closed,
  the other open, a slight smile.
- 20662–20941: final close-up — eyes open and pout; one heart
  flies out of the mouth, grows towards the viewer and flies away
  diagonally to the right/up.
- 20942: the previous tunnel cut-in with the ball. Neither any scene boundary
  nor the throw timing was changed.

Only the interior of the face was corrected in the two existing bitmaps. Hair,
figure, hands, costume, the dancers underneath and the framing remain.
No further full character frames are needed.

The heart has eight phases every 32 ticks; the last one lasts until the
existing cut. The masks show two distinct lobes and a bottom tip, a pink front,
a white light reflection and a purple elongated side. The varying perspective
slightly rotates the surface, and successive phases increase the size. The
start point (82,67 in the 160×192 space) corresponds to the lower lip.

In the kiss phase itself all four players compose the heart; the preserved four
separately animated missile streaks maintain momentum on both sides.
Earlier throw phases still have the previous player wind/fireworks.
No wink loop, kiss loop or additional hearts were added.

## Memory and safety

[READ] Before the change, the six dance banks each had 1024 B of free tail,
6144 B in total. `launch_kiss.py` uses **992 B of one tail**:
$7C00–$7FDF, index 10 in the original player bank table (the third bank of
ribbon bitmaps, compositions 12–17). **5152 B** of the same tails remains.
No new extension banks and no new full bitmaps.

- 31 B of unbanked trampoline: $0F00–$0F1E, reserve up to $0F3F.
  The start of the shared-row region was moved to $0F40.
- Private foreground scratch: $0DDB/$0DDC.
- Ribbon controller: 2252 B, $5400–$5CCB, +6 B. The finale still starts at $5CD0.
- Main code: 2551 B, +27 B for the heart palette; 9 B before $1E00.
- The heart masks themselves: 512 B within the above 992 B. Each phase has
  four 8×16 streams; larger phases double rows and width in hardware.

The preparation clears and fills only the inactive PMG. It does not touch
the active bitmap. Its own trampoline preserves PORTB on the stack; the music
NMI restores the currently selected bank. The existing palette helper restores
the four heart hues after the music DLI, without banking and without the shared
scratch. The clock and the four music updates per PAL frame remain.

## Verification

[READ] 29 targeted tests passed, then 4/4 heart tests after adding late-raster
and NMI interrupt probes. All eight masks were checked in the running 6502,
along with scaling, positions, gloss, separated lobes, the exit to the tunnel
and the return to the dance. NMI injection covers the beginning, the middle and
the last heart phase; the register writes fit within the early blank.

[READ] Atari800 PAL/1088XE, stereo POKEY: **11 608 128 identical
bytes** relative to v035, the whole track. No test on physical Atari.

[READ] Full v233 suite: **172/172 tests passed**, no skips,
118,6 s. The numbered XEX and the working `visual-prototype-dev` are identical.
SHA-256: `81b78b474a360dd8bc9659eebc40afcb14186ef84c3160c9900308fb7a9d8ad0`.

CPU/PMG preview, with an approximate PAL palette: `build/launch-kiss-v233.gif`
and `build/launch-kiss-v233.png`. It is not an FPS measurement or a hardware
recording.
