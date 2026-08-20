# 08 — Codebase Cleanup, Routing Unification & Dependency Integrity

**What to build:** Remove unused speculative code (`DownloadQueue`), resolve undeclared `static_ffmpeg` import, unify `OutputDestinationResolver` with engine routing to eliminate dead helper code and middle-man indirection, and encapsulate `MediaProfile` format/postprocessor mappings in `engine.py`.

**Blocked by:** 06 — Custom Profile CLI Support & Terminology Alignment, 07 — Interactive Wizard Option Granularity & Prompt Alignment

**Status:** ready-for-agent

- [ ] Remove unused `DownloadQueue` dataclass.
- [ ] Handle `ffmpeg` location detection cleanly without importing undeclared `static_ffmpeg` at runtime or declare dependency.
- [ ] Unify `OutputDestinationResolver` with `MediaDownloader` routing.
- [ ] Encapsulate `MediaProfile` format and postprocessor mappings to remove repeated switch smells in `engine.py`.
- [ ] All unit and integration tests pass cleanly.
