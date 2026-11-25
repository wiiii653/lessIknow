> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# Engine profile v011

## V1 — music instruction cost

[READ] The full track was run in py65 with RuntimeMemory, the v011 NMI
wrapper, the original restart and the decoder. 59,833 interrupts: min 347, mean
680.81, max 1427 instruction cycles (tick indexed from zero: 23933).
Maximum sum of four consecutive interrupts: 4881 cycles.
The measurement covers the NMI entry modelled by py65, it does not cover the WSYNC
wait or cycle stealing by ANTIC. It does not close the hardware profiling of V1.

## Renderer

[READ] Cost of a callback invocation with VCOUNT=124 set (without waiting
for vblank, without DMA and without injecting NMI):

- title: 16166 cycles.
- school: 16340 cycles.
- practice1: 93424 cycles.
- practice2: 93620 cycles.
- practice3: 93601 cycles.
- solo: 93788 cycles.
- duo: 93773 cycles.
- trio: 93754 cycles.
- kaleidoscope: 19394 cycles.

[READ] Each invocation in practice and dance copies 8192 B and builds a list
of 192 LMS. Practice copies the same atlas even when the shot does not change.
PMG remains disabled in v011.

[CONCLUSION] First optimisation: keep the practice atlas in the buffers,
and rebuild the static lists when the shot changes. In the dance, consider the differences
between poses, taking into account the contents of each of the two buffers.
Small animations via PMG and palette registers require less CPU work than
further full-screen copies, but the additional DMA still requires measurement.

[ASSUMPTION] No guaranteed free cycle budget per line with PMG enabled
has been determined yet. Without such a measurement we do not declare a fixed
number of free cycles for additional effects.
