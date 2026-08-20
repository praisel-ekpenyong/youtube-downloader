@echo off
setlocal EnableDelayedExpansion
title YouTube Video & Livestream Downloader

:: Set default output directory to user's Downloads folder
set "OUTPUT_DIR=%USERPROFILE%\Downloads"

echo ================================================================
echo           YouTube Video & Livestream Downloader
echo ================================================================
echo.

:: 1. Check for yt-dlp
where yt-dlp >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [!] yt-dlp was not found in PATH. Checking Python module...
    python -m yt_dlp --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set "YTDLP_CMD=python -m yt_dlp"
    ) else (
        echo [ERROR] yt-dlp is not installed!
        echo Please install it by running: pip install yt-dlp
        echo.
        pause
        exit /b 1
    )
) else (
    set "YTDLP_CMD=yt-dlp"
)

:: 2. Check for FFmpeg
set "FFMPEG_PARAM="
where ffmpeg >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [*] Using system FFmpeg.
) else (
    :: Try finding static_ffmpeg via Python
    for /f "delims=" %%I in ('python -c "import os, static_ffmpeg; print(os.path.dirname(static_ffmpeg.run.get_or_fetch_platform_executables_else_raise()[0]))" 2^>nul') do (
        set "FFMPEG_DIR=%%I"
    )
    if defined FFMPEG_DIR if exist "!FFMPEG_DIR!\ffmpeg.exe" (
        echo [*] Found static_ffmpeg at: !FFMPEG_DIR!
        set "FFMPEG_PARAM=--ffmpeg-location "!FFMPEG_DIR!""
    ) else (
        echo [WARNING] FFmpeg not found. Some formats and stream mergers may fail.
    )
)

echo [*] Output Directory: %OUTPUT_DIR%
echo.

:: 3. Get Video/Stream URL
set "TARGET_URL=%~1"
if "%TARGET_URL%"=="" (
    set /p "TARGET_URL=Enter YouTube URL (Video / Livestream / Playlist): "
)

if "%TARGET_URL%"=="" (
    echo [ERROR] No URL provided.
    echo.
    pause
    exit /b 1
)

:: Strip surrounding quotes if any
set "TARGET_URL=%TARGET_URL:"=%"

echo.
echo Select download mode:
echo [1] Best Quality Video + Audio (Streams / VODs / Regular Videos) [Default]
echo [2] Audio Only (Best MP3)
echo [3] 720p Max (Faster download)
echo [4] 1080p Max
echo.
set /p "CHOICE=Select an option [1-4, default=1]: "

if "%CHOICE%"=="2" (
    set "FORMAT_OPTS=-x --audio-format mp3 --audio-quality 0"
) else if "%CHOICE%"=="3" (
    set "FORMAT_OPTS=-f "bestvideo[height<=720]+bestaudio/best[height<=720]/best""
) else if "%CHOICE%"=="4" (
    set "FORMAT_OPTS=-f "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best""
) else (
    set "FORMAT_OPTS="
)

echo.
echo ================================================================
echo Starting Download...
echo ================================================================
echo URL: %TARGET_URL%
echo.

%YTDLP_CMD% %FFMPEG_PARAM% --extractor-args "youtube:player_client=android,web" --downloader "m3u8:native" --live-from-start -N 6 --paths "%OUTPUT_DIR%" -o "%%(title)s [%%(id)s].%%(ext)s" %FORMAT_OPTS% "%TARGET_URL%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================
    echo [SUCCESS] Download completed successfully!
    echo Saved to: %OUTPUT_DIR%
    echo ================================================================
    echo.
    choice /m "Open Downloads folder now"
    if !ERRORLEVEL! EQU 1 (
        explorer "%OUTPUT_DIR%"
    )
) else (
    echo.
    echo ================================================================
    echo [ERROR] Download encountered an issue (Exit Code: %ERRORLEVEL%).
    echo ================================================================
)

echo.
pause
