# 0001: Python CLI Architecture

We decided to migrate the downloader from a Windows Batch script to a modular Python CLI application using the `yt-dlp` library, `typer` for command-line parsing, `rich` for terminal interface/progress display, and `pytest` for automated testing.

While a batch script requires no Python environment setup when `yt-dlp.exe` is present, it is platform-locked to Windows, brittle in string/quote handling, and impossible to unit test reliably. A modular Python application provides cross-platform support, structured error recovery, testable seams, and programmatic control over download hooks and metadata post-processing.
