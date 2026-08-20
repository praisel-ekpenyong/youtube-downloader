# 05 — Interactive Rich Wizard, Retries & Error Diagnostics

**What to build:** Running `ytdl` without arguments launches an interactive Rich wizard for URL and profile selection. Adds smart transient retry logic (up to 3 attempts) and formatted diagnostic cards for errors (e.g. missing `ffmpeg`, age-restriction requiring cookies).

**Blocked by:** 03 — Audio Extraction Profiles (MP3 & Lossless FLAC), 04 — Playlist Routing & Index Filtering

**Status:** resolved

- [x] Executing `ytdl` with no arguments launches an interactive prompt asking for Target URL, Media Profile, and options.
- [x] Transient network/stream errors trigger automatic retries (up to 3 attempts) with backoff.
- [x] Actionable diagnostic cards are displayed for common issues (missing `ffmpeg`, age-restricted content, geo-blocking).
- [x] SIGINT (`Ctrl+C`) during livestream recording terminates cleanly without corrupting media files.
- [x] Unit tests verify interactive fallback triggering, retry handler, and error classification.

