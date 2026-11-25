> **Historical reference. Commands, addresses and findings describe the recorded snapshot.** See the [current documentation guide](README.md) for active instructions.

# v343 — animated loader dots

Restoring the v330 loader text in v342 lost the progress animation. v343
updates three dots after the initialisation of each of the 50 banks. The text
`LOADING BANKS` remains stationary, and the dots occupy fixed positions; no
blocks or addresses are displayed.

Preserved text:

- `THE LESS I KNOW THE BETTER`
- `LOADING BANKS` with animated dots on the right
- `A\SLOP BY OGNJEN / SILLY VENTURE 2026 WE`

Stereo build: `build/visual-prototype-v343.xex` (1 115 801 B), SHA-256
`495cf1a60c4048df81de69f187df3d70177c80ce0bf5248ba38226cbe9e92ef4`.
The generator reported 298 shared rows and 2560 B of main code;
`git diff --check` passes. No tests, emulator or hardware were run.
