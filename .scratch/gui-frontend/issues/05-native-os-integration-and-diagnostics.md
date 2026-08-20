# 05 — Native OS Integration & Actionable Diagnostics

**What to build:** Complete native desktop experience and error recovery. Adds a native folder picker dialog for custom output destinations, "Show in Folder" (opens Windows Explorer with the file selected) and "Play Media" actions on completed cards. For failed downloads, surfaces structured diagnostic reports with actionable fix suggestions and a collapsible raw log drawer.

**Blocked by:** 04 — Multi-Task Download Queue & Live Progress Streaming

**Status:** ready-for-agent

- [ ] "Browse..." button opens native OS folder picker dialog to choose a custom output destination.
- [ ] Completed task cards include a "Show in Folder" button that highlights the downloaded file in Windows File Explorer.
- [ ] Completed task cards include a "Play" button that opens the media file in the default system media player.
- [ ] Failed task cards display actionable diagnostic reports (e.g. missing FFmpeg, 403 Forbidden, bot check) with remediation tips.
- [ ] Collapsible "Raw Logs" drawer on task cards allows inspecting raw yt-dlp execution logs.
- [ ] Unit tests verify native file helper invocation, diagnostic translation, and log drawer formatting.
