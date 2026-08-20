# 11 — Progress Reporter Seam & Headless Test Harness

**What to build:** Decouple download execution from terminal side-effects by introducing a progress reporting seam. Provide a Rich-based adapter for interactive CLI runs and a silent adapter for automated testing and scripting, enabling clean test execution without terminal mocking or stdout pollution.

**Blocked by:** None — can start immediately

**Status:** resolved

- [x] MediaDownloader accepts a progress reporter interface at initialization or execution.
- [x] Rich progress reporting is encapsulated in a dedicated terminal progress adapter used by the CLI.
- [x] A silent progress adapter is available for tests and automated scripts.
- [x] Existing download tests run cleanly without mocking Rich console or progress bars.

## Answer

Introduced the `ProgressReporter` protocol seam in `youtube_downloader.progress` along with `RichProgressReporter` (for interactive CLI runs) and `SilentProgressReporter` (for headless automated runs and tests). `MediaDownloader` accepts a `progress_reporter` at initialization and execution, defaulting to `SilentProgressReporter` to eliminate terminal side-effects and stdout pollution. `cli.py` configures and supplies `RichProgressReporter`. All tests pass cleanly without mocking Rich console or progress bars.
