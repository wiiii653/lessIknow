# Music data from v035

`v035/` contains the fourteen 16 KiB blocks loaded through `$8000-$BFFF` by
`less-i-know-release-v035.xex`, in their original load order. Recreate them with:

```sh
python3 tools/extract_music.py less-i-know-release-v035.xex assets/music/v035
```

Choose a new output directory if `v035/` already exists. The manifest records
the original XEX and bank SHA-256 hashes. Banks 9–14 consist entirely of `$FF`;
bank 8 contains data followed by `$FF`. All banks are retained until playback
access is verified (V3 in `TLIKTB_Technical_Constraints.md`).

The source banks preserve the original player data. The post-party stereo
build uses the v035 player, four music updates per PAL frame, the stereo mix
and the re-rendered ending in `v035-unfaded-ending.bin`. The release command
and verification results are in the [project README](../../README.md) and
[project status](../../docs/PLAN_STATUS.md).

## v035 display-list inspection

Run `python3 tools/inspect_display_list.py less-i-know-release-v035.xex` to
inspect the static XEX contents. The list at `$3300` schedules DLIs on lines
0, 78, 156 and 234 relative to its start and jumps back to `$3300` with JVB.
The list accounts for 235 scanlines before JVB; the remaining frame timing is
controlled by ANTIC. A replacement display list must preserve the four DLI
positions relative to the PAL frame. This inspection does not execute INIT/RUN
or establish whether the player changes the list at runtime.
