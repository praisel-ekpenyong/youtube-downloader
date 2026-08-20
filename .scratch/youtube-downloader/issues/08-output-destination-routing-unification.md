# 08 — Output Destination Resolver Unification & Dead Code Elimination

**What to build:** Unify output destination template generation and directory creation within the destination resolver so that `MediaDownloader` receives the complete download template without manual string concatenation or throwaway resolver instances. Remove obsolete and unused helper methods from the resolver.

**Blocked by:** 07 — Interactive Wizard Option Granularity & Prompt Alignment

**Status:** resolved

- [x] `OutputDestinationResolver` provides a unified method to construct the full `yt-dlp` output template using its configured root directory and the given `MediaProfile`.
- [x] `MediaDownloader` uses `OutputDestinationResolver` directly for destination directory verification and template generation without manual path string formatting.
- [x] Obsolete unused helper methods (`resolve_video_dir`, `resolve_audio_dir`, `resolve_playlist_folder`, `resolve_for_profile`) are removed.
- [x] All unit and integration tests for path resolution and output template generation pass cleanly.
