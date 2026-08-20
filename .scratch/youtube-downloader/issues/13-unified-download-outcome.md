# 13 — Unified Download Outcome & Diagnostic Error Handling

**What to build:** Move transient failure recovery and error classification entirely within the download engine, returning a structured download outcome or typed error containing pre-computed diagnostic details. The CLI consumes the structured outcome directly to render diagnostics without redundant exception parsing.

**Blocked by:** 12 — Deep MediaDownloader & Option Translation Encapsulation

**Status:** ready-for-agent

- [ ] `MediaDownloader` handles transient retries internally and produces a structured result or typed domain exception.
- [ ] Diagnostic analysis is performed once within the engine upon non-recoverable failures.
- [ ] The CLI renders diagnostic panels directly from the structured outcome without re-analyzing raw exceptions.
- [ ] Unit tests verify diagnostic classification and retry behavior through the structured result.
