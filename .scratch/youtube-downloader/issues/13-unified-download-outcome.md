# 13 — Unified Download Outcome & Diagnostic Error Handling

**What to build:** Move transient failure recovery and error classification entirely within the download engine, returning a structured download outcome or typed error containing pre-computed diagnostic details. The CLI consumes the structured outcome directly to render diagnostics without redundant exception parsing.

**Blocked by:** 12 — Deep MediaDownloader & Option Translation Encapsulation

**Status:** resolved

- [x] `MediaDownloader` handles transient retries internally and produces a structured result or typed domain exception.
- [x] Diagnostic analysis is performed once within the engine upon non-recoverable failures.
- [x] The CLI renders diagnostic panels directly from the structured outcome without re-analyzing raw exceptions.
- [x] Unit tests verify diagnostic classification and retry behavior through the structured result.

## Answer

Introduced the `DownloadOutcome` dataclass in `youtube_downloader.models` to encapsulate download execution state, attempt counts, raw exceptions, and diagnostic reports. `MediaDownloader.download` now executes transient retry recovery internally and classifies non-recoverable failures once via `diagnose_error`, returning a structured `DownloadOutcome`. The CLI in `cli.py` consumes `DownloadOutcome` directly to render diagnostic panels without redundant exception catching or diagnosis. All unit and CLI tests were updated to verify structured outcomes and diagnostic classification across all failure categories. All 77 tests pass with 100% type safety.
