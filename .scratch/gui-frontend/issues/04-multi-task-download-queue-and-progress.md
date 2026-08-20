# 04 — Multi-Task Download Queue & Live Progress Streaming

**What to build:** Asynchronous download execution and queue management. Users can queue single or batch URLs; background worker threads execute the downloads without blocking the UI, streaming live progress percentages, download speed, ETA, and status badges (`Queued`, `Downloading`, `Converting`, `Completed`, `Failed`) with cancel/retry actions per task.

**Blocked by:** 03 — Media Profile & Quality Selection Controls

**Status:** ready-for-agent

- [ ] "Add to Queue" / "Download Now" creates a visual task card in the download queue list.
- [ ] Support for batch URL input (multi-line paste) creating multiple queued tasks.
- [ ] Background thread pool executes downloads concurrently or sequentially without freezing window interactions.
- [ ] Real-time progress updates (percentage bar, transfer speed, ETA, fragment counts) stream smoothly to active task cards.
- [ ] Cancel button aborts an in-progress or queued download cleanly.
- [ ] Unit tests verify queue scheduling, multi-task dispatch, cancellation, and progress event emission at the bridge seam.
