# 02 — Core Downloader Engine & Video Media Profiles

**What to build:** Complete vertical slice for downloading single videos and livestreams using video profiles (`best`, `1080p`, `720p`), embedding metadata, chapter markers, and subtitles by default, with rich terminal progress reporting.

**Blocked by:** 01 — Project Skeleton, Configuration & Test Harness

**Status:** resolved

- [x] `MediaDownloader` engine correctly constructs `yt-dlp` options for video profiles (`best`, `1080p`, `720p`).
- [x] Subtitles, chapter markers, video tags, and thumbnail artwork are embedded by default with `--no-subs` and `--no-metadata` flags to disable them.
- [x] Livestreams are captured with `--live-from-start` and native HLS downloader options.
- [x] Downloads are saved into the resolved `Videos/` directory with proper title/id templating.
- [x] Unit tests verify format construction and mocked downloader execution.
