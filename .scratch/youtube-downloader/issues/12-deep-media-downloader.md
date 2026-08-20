# 12 — Deep MediaDownloader & Option Translation Encapsulation

**What to build:** Encapsulate backend option construction, format selection, and postprocessor mapping inside `MediaDownloader.download`, removing shallow public translation methods. Refactor tests to exercise the complete download task workflow through the primary interface using the silent progress adapter.

**Blocked by:** 11 — Progress Reporter Seam & Headless Test Harness

**Status:** ready-for-agent

- [ ] Option building, format selector resolution, and audio postprocessor configuration are private implementation details of the download engine.
- [ ] Callers and tests interact solely with `MediaDownloader.download` passing a `DownloadTask`.
- [ ] Tests verify download execution and behavior through the public interface rather than inspecting private dictionary options.
- [ ] All existing media profile formats, subtitle embedding, and metadata features remain fully functional.
