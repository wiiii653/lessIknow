> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# V282 — scene, hall and loading screen palette

The first school sequence uses the same palette throughout the shot as
the approved frame: black, muted pink, steel blue and peach.
The RGB samples after preview match the reference colours exactly:
`#000000`, `#9D5058`, `#426FA7`, `#DE988A`. The Atari palette `$38/$88/$2C`
also covers the opening shot, the panorama and the boy's reactions.

The hall has a separate GTIA palette `$38/$68/$2A` — warmer and darker.
It preserves the original colour separation of the source graphics, so the costumes, parquet,
walls and ball remain readable. The setting covers the group dance shots,
training and basketball.

The loading screen gives the title, Atari XE stereo, production by Ognjen and Silly
Venture 2026. The bank-loading information remains. The background is dark navy,
and the text peach; the OS shadows and GTIA registers have the same values.

Stereo XEX for AVG: `releases/less-i-know-demo-release-019-stereo.xex`
(935 281 B, SHA-256 `10f0c7cc2ed7b67b22e01cbb658195381b35b772f75708775f3c2715953a1752`).
Metadata: `releases/less-i-know-demo-release-019-stereo.json`.
The compact late-start staging now also covers `$07E5–$07E8`, in line
with the current low-memory segment.

[READ] Build: 298 shared rows, main code 2560 B. Rendered
previews of the school and hall scenes were checked; the first contains exactly
the four specified colours, and the hall three distinguishable warm colours plus black.
The final XEX is 0.892 MiB.

[LIMITATION] No automated tests or full music comparison were run.
This build was not checked on physical Atari.
