# 12 — Deep MediaDownloader & Option Translation Encapsulation

**What to build:** Encapsulate backend option construction, format selection, and postprocessor mapping inside `MediaDownloader.download`, removing shallow public translation methods. Refactor tests to exercise the complete download task workflow through the primary interface using the silent progress adapter.

**Blocked by:** 11 — Progress Reporter Seam & Headless Test Harness

**Status:** resolved

- [x] Option building, format selector resolution, and audio postprocessor configuration are private implementation details of the download engine.
- [x] Callers and tests interact solely with `MediaDownloader.download` passing a `DownloadTask`.
- [x] Tests verify download execution and behavior through the public interface rather than inspecting private dictionary options.
- [x] All existing media profile formats, subtitle embedding, and metadata features remain fully functional.

## Answer

Encapsulated backend option construction (`_build_ytdl_options`), format selector resolution (`_get_format_for_profile`), and audio postprocessor mapping (`_get_audio_postprocessor_for_profile`, `_PROFILE_FORMAT_SELECTORS`, `_PROFILE_AUDIO_POSTPROCESSORS`) as private implementation details inside `MediaDownloader` in `youtube_downloader.engine`. The public interface of `MediaDownloader` is now solely `download(task, ...)` (along with `__init__`). All test suites in `tests/test_engine.py` and `tests/test_playlist.py` were refactored to exercise full task workflows through `MediaDownloader.download` using `SilentProgressReporter` and mocked `yt_dlp.YoutubeDL`. All 72 tests pass cleanly with 100% type safety.
