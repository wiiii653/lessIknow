# V181 — walk and framing from v175

[READ] All 18 side frames of the girl were restored directly
from the preserved v175 XEX: direction, character proportions, camera position and
background offsets are identical. The frame source was kept in
`assets/art/reference/v175/arena-pan.bin`; the generator repacks them
into the existing five panorama banks, with the current controller.

The boy and girl shots returned to the order and scales from v175. In the zoom-out
sequence the girl's positions were corrected: the centre of her feet reaches the
left door of the arena, near the logical point (82,52). The previous end
point (64,48) fell at the post beside the entrance. The large foreground and
the boy's portrait keep their framing. The jacket mask covers the whole
interior of the torso outline; the black hair is still opaque.

The note preview was also normalised to the actual display of the school shot:
each logical row is repeated three times, as in the display list.
The appearance of the notes in the XEX remains as it was before this normalisation.

## Build and verification

- `build/visual-prototype-v181.xex` and the corresponding JSON.
- SHA-256: `c43fb25f554f3c48d02041b9b2fb90852cbaaad0079d3a3900d4cc9e7f8324cb`.
- 275 shared rows, 10,630 B of row data, 2552 B of code.
- No change to ticks, act boundaries or bank allocation; the longer v180 tunnel
  remains active.
- Comparison of 64 banks with v180: only panorama banks 19–23 changed;
  the other 59 banks are byte-for-byte identical.
- Six tests passed: 18 panorama frames after the callback, comparison
  with the archived v175 banks, hair/jacket opacity in both boy poses,
  meeting composition, foreground framing, and convergence of the girl's path
  to the entrance.
- Preview after running the 6502 callbacks: `build/v181-opening-preview.png`.
  py65 does not model ANTIC DMA or real FPS.
- The stereo POKEY comparison attempt in Atari800 ended before the emulator
  started: the installed AppImage requires an unavailable FUSE. This release
  did not confirm emulator or hardware playback.
