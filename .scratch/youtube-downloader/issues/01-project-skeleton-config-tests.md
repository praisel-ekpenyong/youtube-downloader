# 01 — Project Skeleton, Configuration & Test Harness

**What to build:** A runnable Python package (`pyproject.toml`, `src/youtube_downloader/`, CLI entrypoint `ytdl`), test harness with `pytest`, default configuration/output directory resolution (`%USERPROFILE%\Downloads\YouTube`), and basic CLI options with `--help`.

**Blocked by:** None — can start immediately.

**Status:** resolved

- [x] Python package structure with `pyproject.toml` is configured with `typer`, `rich`, `yt-dlp`, and `pytest`.
- [x] Output directory resolver locates default user directories (`Downloads/YouTube/Videos`, `Downloads/YouTube/Audio`, etc.) and handles custom overrides.
- [x] CLI entrypoint `ytdl` provides standard `--help`, `--version`, and argument parsing.
- [x] Test suite configured with `pytest` and initial unit tests pass cleanly.
