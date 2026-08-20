# 07 — Interactive Wizard Option Granularity & Prompt Alignment

**What to build:** Add interactive prompt for livestream recording from start (`--live-from-start`), and decouple enrichment prompts in the wizard so users can independently configure subtitle tracks, chapter markers, thumbnail artwork, and metadata tags per ADR 0002.

**Blocked by:** None — can start immediately.

**Status:** resolved

- [x] Wizard prompts for `live_from_start` option.
- [x] Wizard prompts independently for subtitles, chapters, metadata tags, and thumbnail artwork.
- [x] Unit tests in `tests/test_wizard.py` verify all interactive prompt paths and flag assignments.
