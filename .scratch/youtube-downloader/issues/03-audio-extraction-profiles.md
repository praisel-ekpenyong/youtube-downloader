# 03 — Audio Extraction Profiles (MP3 & Lossless FLAC)

**What to build:** End-to-end audio extraction for `audio-mp3` (320kbps + embedded thumbnail/tags) and `audio-flac`, routing output to `Downloads/YouTube/Audio/`.

**Blocked by:** 02 — Core Downloader Engine & Video Media Profiles

**Status:** resolved

- [x] `MediaDownloader` supports `audio-mp3` profile with 320kbps MP3 post-processing and embedded cover art.
- [x] `MediaDownloader` supports `audio-flac` profile for lossless audio extraction.
- [x] Extracted audio files are automatically routed to the `Audio/` subfolder.
- [x] Unit tests verify audio post-processor option generation and output routing.
