# Specification: Desktop GUI Frontend

Status: ready-for-agent

## Problem Statement

Users who prefer visual desktop applications or who download videos and audio playlists frequently find command-line interfaces, terminal prompts, and batch scripts cumbersome. They lack an intuitive visual dashboard to paste URLs, instantly preview video thumbnails and metadata, configure media quality presets with one click, manage a multi-task download queue with live progress bars, and easily open downloaded files or folders in Windows Explorer.

## Solution

A modern, responsive desktop GUI application built using `pywebview` with an HTML5, Tailwind CSS, and Vanilla JS frontend. The interface connects directly to the core Python `DownloadEngine` via an in-process Python API bridge, offering:
1. **Target URL Input & Metadata Preview**: Automatic async fetching of video title, channel, duration, and thumbnail upon pasting a link, with support for single URLs, multi-line batch inputs, and playlists.
2. **Two-Tier Media Profile Selection**: One-click quick presets (`Best`, `1080p`, `720p`, `Audio MP3 320k`, `Audio FLAC Lossless`) and a collapsible advanced panel for subtitles, chapter markers, thumbnail embedding, live-stream capture, playlist item filtering, and custom format selectors.
3. **Interactive Multi-Task Download Queue**: Visual task cards displaying live animated progress bars, download speed, ETA, and status indicators (`Queued`, `Downloading`, `Converting`, `Completed`, `Failed`) with cancel/retry controls.
4. **Actionable Diagnostics & Error Recovery**: Direct integration with the diagnostic engine to display clear, structured remediation cards for failures (e.g. 403 Forbidden, missing FFmpeg, bot check) alongside a collapsible raw log drawer.
5. **Native Desktop Integration**: OS folder picker dialog, one-click "Show in Folder" (highlighting the file in Windows File Explorer), and "Play Media" actions.

## User Stories

1. As a visual desktop user, I want to launch the YouTube Downloader GUI via `ytdl-gui` or a desktop shortcut, so that I can download media without interacting with a terminal command line.
2. As a user pasting a Target URL, I want to see an immediate Metadata Preview showing the video title, channel name, duration, and thumbnail artwork, so that I can confirm I pasted the correct link before starting the download.
3. As a user pasting a playlist URL, I want the Metadata Preview to identify it as a playlist and indicate the total track count, so that I know what to expect.
4. As a user downloading music, I want to select the `Audio MP3 (320kbps)` or `Audio Lossless (FLAC)` preset with one click, so that the audio stream is automatically extracted, converted, and tagged with album art.
5. As a user with bandwidth limits, I want to select `720p` or `1080p` video presets with one click, so that the download matches my desired resolution.
6. As a power user, I want to expand the "Advanced Options" panel to configure subtitle tracks, chapter markers, thumbnail embedding, and custom yt-dlp format strings, so that I have complete control over media enrichment.
7. As a user downloading a playlist, I want to specify an item range (e.g. `1-5, 8`) in the advanced options, so that I only retrieve the specific tracks I need.
8. As a user downloading multiple links, I want to paste a batch list of URLs into the input box, so that multiple Download Tasks are created and added to the Download Queue simultaneously.
9. As a user downloading media, I want to see real-time progress for each active task (download percentage, current transfer speed, and ETA), so that I know how long the download will take.
10. As a user with an active download, I want to cancel an in-progress or queued task, so that I can free up bandwidth or stop unwanted downloads.
11. As a user whose download finishes, I want to click "Show in Folder" on the completed task card, so that Windows File Explorer opens with the downloaded media file selected and highlighted.
12. As a user whose download finishes, I want to click "Play Media" on the completed task card, so that the file immediately opens in my default media player.
13. As a user choosing an Output Destination, I want to click "Browse..." to select a custom destination folder via the native Windows folder picker dialog, so that my files are saved where I want.
14. As a user encountering a download failure (such as missing FFmpeg or a 403 Forbidden error), I want to see an actionable Diagnostic Report explaining the cause and suggesting a fix, so that I can easily resolve the problem.
15. As a developer/power user debugging a failed download, I want to expand a "Raw Output Log" drawer on the task card, so that I can inspect the exact yt-dlp command output.
16. As a user in low-light environments, I want a sleek, modern YouTube-Studio-inspired dark slate theme, so that the application is comfortable to view.

## Implementation Decisions

- **Desktop Shell**: `pywebview` utilizing native Microsoft Edge WebView2 on Windows. Zero Node.js / Electron runtime dependencies, zero open network ports.
- **Frontend Architecture**: Single-page application hosted in `src/youtube_downloader/gui/web/` using semantic HTML5, utility-first Tailwind CSS, and modular Vanilla JS (ES6+).
- **In-Process Python Bridge**: A `GUIBridge` class exposed to `window.pywebview.api` providing methods for `fetch_metadata`, `start_task`, `cancel_task`, `select_folder`, `open_path`, and `get_diagnostics`.
- **Progress Dispatch**: The Python bridge hooks into `DownloadEngine`'s progress reporter and evaluates JavaScript events (`window.onDownloadProgress(...)`) in real time.
- **Concurrency & Queue**: A background `ThreadPoolExecutor` within the GUI bridge to process Download Tasks asynchronously without blocking the UI thread or window events.
- **Native OS Hooks**: Uses `os.startfile` and `explorer.exe /select,"<path>"` for native Windows file/folder interactions.
- **Entry Points**: Registered `ytdl-gui` console script in `pyproject.toml` pointing to `youtube_downloader.gui.app:main`.

## Testing Decisions

- **Single High-Level Seam (`GUIBridge`)**: All GUI testing will be conducted against the `GUIBridge` interface. The bridge represents the complete boundary between the web UI and the Python engine.
- **Good Test Criteria**: Tests verify external behavior and contract fulfillment (e.g. metadata extraction returning structured dicts, queue addition and execution triggering callbacks, cancellation stopping active workers, error handling returning structured `DiagnosticReport` objects) without spinning up a real graphical window.
- **Mocked Engine & yt-dlp**: External network operations and `yt-dlp` calls are mocked using existing test patterns from `tests/test_engine.py` and `tests/test_diagnostics.py`.
- **Zero Headless Display Dependencies**: Tests run reliably in headless CI/CD environments with `pytest`.

## Out of Scope

- Remote web hosting or multi-user web server deployment.
- Direct video editing or trimming timeline features.
- Support for non-yt-dlp download protocols (e.g. raw BitTorrent).

## Further Notes

- Maintains full compatibility and shared domain vocabulary with the existing CLI tool, `DownloadEngine`, and `DownloadTask` models.
