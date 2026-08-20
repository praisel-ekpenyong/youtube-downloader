# 15 — Output Destination Resolver Collapse, Download Queue & UI Decoupling

**What to build:** Collapse the shallow OutputDestinationResolver into MediaDownloader, introduce native DownloadQueue batch orchestration matching CONTEXT.md, and decouple Rich UI panel rendering from diagnostics.py.

**Blocked by:** 14 — Deep Output Destination & Playlist Folder Management

**Status:** resolved

- [x] OutputDestinationResolver is removed and destination resolution/template formatting is absorbed into MediaDownloader.
- [x] DownloadQueue is introduced in models.py and supported in MediaDownloader.download().
- [x] diagnostics.py is decoupled from rich.panel.Panel and returns pure data DiagnosticReport.
- [x] cli.py handles render_diagnostic_panel and passes destination paths directly to MediaDownloader.
- [x] Automated tests and static typing verify full coverage and type safety.

## Answer

Collapsed OutputDestinationResolver into MediaDownloader in youtube_downloader.engine, simplifying youtube_downloader.config to DEFAULT_OUTPUT_ROOT. Introduced the DownloadQueue dataclass in youtube_downloader.models to support ordered batch executions, deepening MediaDownloader.download() to accept either a single DownloadTask or a DownloadQueue while managing progress reporter lifecycles across tasks. Decoupled youtube_downloader.diagnostics from Rich UI rendering by moving render_diagnostic_panel into youtube_downloader.cli. All 82 tests pass with 100% type safety (mypy src tests).
