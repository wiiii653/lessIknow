# Documentation Guide

Use this page to find the current project documentation. Write new and
maintained project documentation in English.

## Current references

- [Project status](PLAN_STATUS.md) — approved release, current development
  state, validation limits and memory/loader constraints.
- [Current demo timeline](TIMELINE_MAP.md) — concise scene overview.
- [Post-Trevor montage](CURRENT_MONTAGE_V330.md) — detailed current cuts.
- [Technical overview](TECHNICAL_OVERVIEW_EN.md) — rendering and runtime
  architecture.
- [Hardware loader contract](HARDWARE_LOADER_CONTRACT.md) — mandatory rules
  for AVG loading and hardware packaging.
- [Loader documentation](loader/README.md) — XEX layout, bank handling,
  startup and diagnostics.
- [Music bank audit](MUSIC_BANK_AUDIT.md) — measured v035 decoder reads and
  unused music-bank space.

## Keeping the references current

Use the Makefile and builders for build options, the generated JSON for
allocation and timing, and Project Status for release approval and hardware
evidence. Update the corresponding reference when one of those facts changes.
Only associate a validation result with the artifact actually exercised.

## Historical records and proposals

Version notes, audits, dumps and the numbered loader chapters describe their
recorded snapshots. Use the current source, generated build map and hardware
loader contract for implementation decisions. Resolve conflicts in favor of
those sources and update the affected plan before implementing it.

The [opening plan](TERMINAL_OPENING_IMPLEMENTATION.md) and
[main-act strip plan](TERMINAL_MAIN_ACTS_IMPLEMENTATION.md) target prerelease
182 as their regression baseline. The older terminal briefs provide draft
copy and visual direction. The outro text review and the basketball hero
redraw are preserved as proposals.

`projects/` contains separate experiments with their own instructions.
The imported `docs/boruta-atari8/` library is external reference material.
