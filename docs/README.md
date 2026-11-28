# Documentation Guide

Use this page to find the current project documentation. Write new and
maintained project documentation in English.

## Current references

- [Project status](PLAN_STATUS.md) — approved release, current development
  state, validation limits and memory/loader constraints.
- [Final polish](PLAN_STATUS.md#final-polish) — pending graphics work and
  hardware validation.
- [Current demo timeline](TIMELINE_MAP.md) — concise scene overview.
- [Post-Trevor montage](CURRENT_MONTAGE_V330.md) — detailed current cuts.
- [Technical overview](TECHNICAL_OVERVIEW_EN.md) — rendering and runtime
  architecture.
- [Hardware loader contract](HARDWARE_LOADER_CONTRACT.md) — mandatory rules
  for AVG loading and hardware packaging.
- [Loader documentation](loader/README.md) — XEX layout, bank handling,
  startup and diagnostics.
- [Opening and title reflection](TERMINAL_OPENING_IMPLEMENTATION.md) — current startup, player handoff and reflection implementation.
- [Main-act terminal](TERMINAL_MAIN_ACTS_IMPLEMENTATION.md) — caption timing, palette and display-list handoff.
- [Music data](../assets/music/README.md) — original v035 source blocks and the development soundtrack.

## Current screen text

- [Loader and opening](terminal_opening.md)
- [Main-act captions](main_act_terminal.md)
- [Greetings](greetings_terminal.md)
- [Credits and ending cards](outro_text.md)

The four text references transcribe the current build inputs and link to the
Python sources. Update the affected reference when the source copy changes.

## Keeping the references current

Use the Makefile and builders for build options, the generated JSON for
allocation and timing, and Project Status for release approval and hardware
evidence. Update the corresponding reference when one of those facts changes.
Only associate a validation result with the artifact actually exercised.

## Documentation backup

The [documentation backup](backup/README.md) contains the numbered version
notes, older audits and superseded plans. Dated dumps and art reviews sit
with their associated assets. The loader chapters remain linked from the
[loader guide](loader/README.md).

`projects/` contains separate experiments with their own instructions.
The imported `docs/boruta-atari8/` library is external reference material.
