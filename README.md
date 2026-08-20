# YouTube Video & Livestream Downloader

### How to Use:
1. **Option A (Interactive)**: Double-click `download_video.bat`, paste your YouTube URL when prompted, and choose your format.
2. **Option B (Command Line / Drag & Drop)**: 
   - Drag and drop a URL or shortcut onto `download_video.bat`
   - Or run from command prompt: `download_video.bat "https://www.youtube.com/watch?v=..."`

### Features:
- **Livestream Support**: Uses native HLS downloader (`--downloader "m3u8:native"`) and `--live-from-start` to avoid YouTube 403 Forbidden errors and download from the start of streams.
- **Fast Multithreaded Downloads**: Uses 6 concurrent connections (`-N 6`) for faster fragment retrieval.
- **Automatic FFmpeg Detection**: Automatically locates FFmpeg (including your Python `static_ffmpeg` installation) to merge video and audio streams seamlessly.
- **Saved Location**: All downloaded files are saved directly into your `Downloads` folder (`%USERPROFILE%\Downloads`).
