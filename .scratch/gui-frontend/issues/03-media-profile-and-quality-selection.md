# 03 — Media Profile & Quality Selection Controls

**What to build:** Interactive quality and format selection controls on the GUI. Provides one-click visual preset buttons (`Best Video`, `1080p`, `720p`, `Audio MP3 320k`, `Audio Lossless FLAC`) and a collapsible advanced settings accordion for subtitles, chapter markers, thumbnail embedding, live-stream capture, playlist item filtering, and custom format strings.

**Blocked by:** 02 — Target URL Metadata Preview & Inspection

**Status:** ready-for-agent

- [ ] Visual preset chips for Best, 1080p, 720p, Audio MP3 (320k), and Audio FLAC (Lossless) with active selection states.
- [ ] Audio presets automatically hide or disable irrelevant video-only options (like resolution).
- [ ] Collapsible "Advanced Settings" accordion containing toggles for subtitles, chapters, thumbnail embedding, and live-from-start.
- [ ] Subtitle language selector and playlist item range text input (`1-5, 8`) in advanced settings.
- [ ] Unit tests verify that UI selection states serialize accurately into `DownloadTask` configuration objects.
