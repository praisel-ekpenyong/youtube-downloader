# 09 — Media Profile Format & Postprocessor Decoupling

**What to build:** Encapsulate `yt-dlp` format selector resolution and FFmpeg audio postprocessor configuration within the engine layer or dedicated profile adapter, keeping domain models in `models.py` decoupled from backend library specifics while eliminating repeated conditional switches in `engine.py`.

**Blocked by:** 08 — Output Destination Resolver Unification & Dead Code Elimination

**Status:** resolved

- [x] Domain models in `models.py` remain pure dataclasses and enums without backend `yt-dlp`/`ffmpeg` postprocessor dictionary payloads.
- [x] Engine format selection and audio postprocessor configuration are encapsulated in engine profile mappings.
- [x] Unit tests verify format selector strings and postprocessor dictionary structures for all `MediaProfile` values.

