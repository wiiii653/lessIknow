# Technical Constraints

This is a stereo Atari XL/XE demo targeting PAL and a 1 MB expansion. Current
development constraints are summarized in `AGENTS.md` and
`docs/PLAN_STATUS.md`; the detailed AVG packaging rules are in
`docs/HARDWARE_LOADER_CONTRACT.md`.

## Runtime

- Keep the original v035 music player and four evenly spaced updates per PAL
  frame. Use player ticks for scene transitions.
- Preserve PORTB across music NMI and banked callbacks.
- All 64 expansion banks are allocated. Confirm the generated allocator map
  and overlap checks before changing ownership.
- Main code occupies `$1400–$1DFF`; the shared scanline pool begins at `$1E00`
  and currently contains 298 rows.
- The music player is stereo. Mono releases are retired.

## Video and PMG

- Prepare inactive bitmap and PMG buffers, then publish them in an early,
  bounded blanking window.
- A late `VCOUNT >= 124` check alone is not a safe deadline for long PMG writes.
- PMG buffers span `$0980–$0BFF` and `$8980–$8BFF`; clear only these ranges.
- Preserve dance PMG double buffering, Trevor impact protections and the
  tunnel renderer's opaque hole coverage.

## Hardware packaging

Raw visual prototypes do not include the confirmed AVG startup protocol. Use
`make hardware` or `tools/build_hardware_xex.py`. Release 058 / v330 remains
the immutable hardware reference; it is the last full run confirmed on the
user's Atari 1088 Rambo.

py65 and Atari800 checks cannot confirm ANTIC DMA deadlines or physical raster
behavior. Report emulator and hardware evidence separately.
