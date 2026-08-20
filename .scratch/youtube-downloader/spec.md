# Specification: YouTube Downloader CLI

## Problem Statement
Users downloading YouTube videos, livestreams, and playlists currently rely on fragile batch scripts or ad-hoc terminal commands. These scripts lack structured error handling, automated testing, flexible media profiles (e.g. lossless audio vs. resolution-capped video), automatic playlist folder organization, and rich terminal feedback.

## Solution
A modern, modular Python CLI tool that provides:
1. A hybrid interface: direct CLI command execution for scripts/power users, and an interactive Rich wizard for interactive runs.
2. Comprehensive Media Profiles (Best video, 1080p, 720p, High-Quality MP3, Lossless FLAC, and Custom).
3. Rich media defaults (embedding chapters, metadata, thumbnails, and subtitles).
4. Automatic folder routing (separating Videos vs. Audio and isolating Playlists into sequenced subfolders).
5. Resilient livestream recording from the start with graceful interrupt handling.
6. A test-driven codebase with unit and integration tests.

## User Stories

1. As a user, I want to run `ytdl <URL>` with no additional flags, so that it automatically downloads the highest quality video and audio with embedded metadata and subtitles.
2. As a user, I want to run `ytdl` with no arguments, so that an interactive wizard guides me to enter a URL, pick a Media Profile, and choose options.
3. As a music listener, I want to select the `audio-mp3` profile, so that the audio stream is extracted into a 320kbps MP3 with embedded album artwork and tags.
4. As an audiophile, I want to select the `audio-flac` profile, so that I can extract lossless audio when available.
5. As a user with limited bandwidth/storage, I want to select `720p` or `1080p` profiles, so that downloads do not exceed my preferred resolution.
6. As a user downloading a playlist, I want all playlist items saved into a dedicated folder named after the playlist with track numbering (e.g. `01 - Track.mp4`), so that my main downloads folder is not cluttered.
7. As a user downloading a large playlist, I want to specify an item range (e.g. `--items 1-5`), so that I only download the specific tracks I want.
8. As a user watching an active livestream, I want to record it from the start (`--live-from-start`), so that I don't miss the beginning of the broadcast.
9. As a user recording a livestream, I want to press `Ctrl+C` to stop recording cleanly, so that the recorded video remains uncorrupted and playable.
10. As a user with network fluctuations, I want transient download errors to retry automatically up to 3 times, so that temporary drops do not abort the entire task.
11. As a user encountering an age-restricted or private video, I want clear diagnostic messages explaining how to provide cookies or authenticate, so that I understand why the download failed.
12. As a developer, I want all core modules tested via `pytest` without making live network calls, so that the codebase remains robust against regressions.

## Implementation Decisions

- **Package Layout**: Standard `src/` layout under `src/youtube_downloader/` with `pyproject.toml`.
- **CLI Framework**: `typer` for declarative command and option parsing, coupled with `rich` for terminal UI, tables, and progress display.
- **Engine Core**: A `MediaDownloader` class wrapping `yt-dlp` options and execution hooks.
- **Output Organization**: Default root `%USERPROFILE%\Downloads\YouTube` routing to `/Videos/`, `/Audio/`, and `/Playlists/<Playlist Title>/`.
- **Default Media Enrichment**: Enabled by default (subtitles, chapters, metadata tags, thumbnail embedding), with `--no-subs` and `--no-metadata` flags to opt out.
- **Error Diagnostics**: Specific handler catching `DownloadError` to classify errors (missing ffmpeg, auth required, geo-blocked, format unavailable) into user-friendly diagnostic cards.

## Testing Decisions

- Tests will focus exclusively on external behavior and contract boundaries at the `MediaDownloader` and CLI runner level.
- `pytest` will test:
  - Argument parsing and default value assignments.
  - Media Profile resolution and corresponding format selector construction.
  - Output path generation for single videos vs. playlists vs. audio files.
  - Retry logic and error diagnostic categorization with a mocked `yt-dlp` runner.
- Zero network dependencies during test execution.

## Out of Scope

- Graphical User Interface (GUI) desktop window (focused strictly on CLI / TUI).
- Direct BitTorrent or non-yt-dlp supported protocol streaming.
- Built-in video editing or clipping timelines.

## Further Notes

- Retains backward compatibility with double-click / drag-and-drop workflows via interactive fallback.
