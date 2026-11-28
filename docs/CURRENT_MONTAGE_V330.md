# Current Post-Trevor Timeline

This page records the current post-Trevor scene cuts. Times use the v035
player's integer update counter (ticks). The cut ranges below describe the
[current development build](PLAN_STATUS.md#current-development-build).
Use `post_trevor_cuts` in the generated build JSON to check the exact cuts
after timing edits.

| Player ticks | Scene |
|---:|---|
| 11,967–14,958 | First rotators: spiral and organic tunnels; direction and speed change each bar |
| 20,942–21,689 | Tunnel before the dunk, selected by the director |
| 23,934–29,655 | Trevor enters, then punches and deflects the ball |
| 29,656–41,803 | Post-Trevor montage; bananas begin on the first callback after the fight, preserving phase |
| 29,917–41,803 | Short passages: peeled/golden bananas, spiral and organic tunnels, changing directions |
| 38,705–39,378 | Bananas before the eyes, with yellow fruit and a slowly cycling backdrop and BUM/BAM from bar 104 |
| 39,379–40,126 | Girl's eyes within the montage |
| 40,127–41,135 | Bananas after the eyes, with yellow fruit and a slowly cycling backdrop, BUM/BAM and departing bubbles; motion changes on bars 108–109 |
| 41,804–41,875 | Brief black transition while the credits bitmap and terminal are prepared |
| 41,876–51,231 | Credits portrait and terminal. The shoe lifts before the first kick and lands on it. |
| 51,232–51,979 | Final shot with orbiting sprites and fade |
| 51,980 onward | Final card with star and orbits; music continues to five minutes |

The first post-Trevor direction/speed change occurs on bar 80 (tick 29,917);
subsequent passes generally cut once per bar. The final tunnel before the eyes
cuts to bananas halfway through bar 103. A 4,000-tick internal motif-clock offset
selects the texture. The final card starts on bar 139, about 4:20.7 after
playback begins. The music ends after five minutes.

The mosaic renderer prepares its inactive framebuffer and display list, then
publishes the list when `124 <= VCOUNT < 128`. A late draw keeps the old
list visible until the next window. The 24 montage banks share 381 bytes of
row and palette lookup tables at `$DFC0–$E13C`. The build JSON lists the
reclaimable tail of each bank.

Earlier editorial decisions are recorded in the historical V248, V260 and V330
notes. Those records are archival and may describe superseded edits.
