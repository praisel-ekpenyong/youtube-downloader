from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any, Callable, Optional

import yt_dlp  # type: ignore[import-untyped]
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

import time
from youtube_downloader.diagnostics import diagnose_error
from youtube_downloader.models import DownloadTask, MediaProfile

console = Console()



def find_ffmpeg_location() -> Optional[str]:
    """Locate FFmpeg executable directory from system PATH or static_ffmpeg package."""
    if shutil.which("ffmpeg"):
        return None  # System FFmpeg is already in PATH
    try:
        import static_ffmpeg
        paths = static_ffmpeg.run.get_or_fetch_platform_executables_else_raise()
        if paths and len(paths) > 0:
            return os.path.dirname(paths[0])
    except Exception:
        pass
    return None


class MediaDownloader:
    """Core download engine wrapping yt-dlp with rich feedback and media profiles."""

    def __init__(self, ffmpeg_dir: Optional[str] = None):
        self.ffmpeg_dir = ffmpeg_dir or find_ffmpeg_location()

    def get_format_for_profile(self, profile: MediaProfile, custom_format: Optional[str] = None) -> str:
        """Resolve format selector string based on MediaProfile."""
        match profile:
            case MediaProfile.BEST:
                return "bestvideo+bestaudio/best"
            case MediaProfile.P1080:
                return "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
            case MediaProfile.P720:
                return "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
            case MediaProfile.AUDIO_MP3 | MediaProfile.AUDIO_FLAC:
                return "bestaudio/best"
            case MediaProfile.CUSTOM:
                return custom_format or "bestvideo+bestaudio/best"
            case _:
                return "bestvideo+bestaudio/best"

    def build_ytdl_options(
        self,
        task: DownloadTask,
        progress_hook: Optional[Callable[[dict[str, Any]], None]] = None,
    ) -> dict[str, Any]:
        """Construct yt-dlp options dictionary from a DownloadTask."""
        postprocessors: list[dict[str, Any]] = []

        default_category = "Audio" if task.media_profile.is_audio_only else "Videos"
        outtmpl_str = f"%(playlist_title&Playlists|{default_category})s/%(playlist_title&{{}}|.)s/%(playlist_index&{{:02d}} - |)s%(title)s [%(id)s].%(ext)s"

        opts: dict[str, Any] = {
            "format": self.get_format_for_profile(task.media_profile, task.custom_format),
            "outtmpl": {"default": outtmpl_str},
            "noplaylist": False,
            "quiet": True,
            "no_warnings": True,
            "concurrent_fragment_downloads": 6,
            "downloader": {"default": "m3u8:native"},
            "live_from_start": task.live_from_start,
        }

        if self.ffmpeg_dir:
            opts["ffmpeg_location"] = self.ffmpeg_dir

        if task.output_destination:
            opts["paths"] = {"home": str(task.output_destination)}

        if task.playlist_items:
            opts["playlist_items"] = task.playlist_items
            opts["noplaylist"] = False

        # Audio extraction postprocessors
        if task.media_profile == MediaProfile.AUDIO_MP3:
            postprocessors.append({
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            })
        elif task.media_profile == MediaProfile.AUDIO_FLAC:
            postprocessors.append({
                "key": "FFmpegExtractAudio",
                "preferredcodec": "flac",
                "preferredquality": "0",
            })

        # Subtitles (only for video profiles)
        if not task.media_profile.is_audio_only and task.embed_subtitles:
            opts["writesubtitles"] = True
            opts["writeautomaticsub"] = True
            opts["subtitleslangs"] = ["all", "-live_chat"]
            postprocessors.append({
                "key": "FFmpegEmbedSubtitle",
                "already_have_subtitle": False,
            })
        else:
            opts["writesubtitles"] = False
            opts["writeautomaticsub"] = False

        # Metadata & Chapters
        if task.embed_metadata or task.embed_chapters:
            postprocessors.append({
                "key": "FFmpegMetadata",
                "add_chapters": task.embed_chapters,
                "add_metadata": task.embed_metadata,
            })

        # Thumbnail embedding
        if task.embed_thumbnail:
            opts["writethumbnail"] = True
            postprocessors.append({
                "key": "EmbedThumbnail",
                "already_have_thumbnail": False,
            })

        if postprocessors:
            opts["postprocessors"] = postprocessors

        if progress_hook:
            opts["progress_hooks"] = [progress_hook]

        return opts

    def download(
        self,
        task: DownloadTask,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        """Execute the DownloadTask using yt-dlp with rich progress display and automatic retries."""
        if task.output_destination:
            task.output_destination.mkdir(parents=True, exist_ok=True)

        attempt = 0
        while True:
            attempt += 1
            try:
                with Progress(
                    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
                    BarColumn(bar_width=40),
                    "[progress.percentage]{task.percentage:>3.1f}%",
                    "•",
                    DownloadColumn(),
                    "•",
                    TransferSpeedColumn(),
                    "•",
                    TimeRemainingColumn(),
                    console=console,
                    transient=True,
                ) as progress:
                    progress_task_id: Optional[TaskID] = None

                    def progress_hook(d: dict[str, Any]) -> None:
                        nonlocal progress_task_id
                        status = d.get("status")
                        if status == "downloading":
                            filename = os.path.basename(d.get("filename", "Downloading..."))
                            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                            downloaded = d.get("downloaded_bytes", 0)

                            if progress_task_id is None:
                                progress_task_id = progress.add_task(
                                    "download",
                                    filename=filename,
                                    total=total,
                                    completed=downloaded,
                                )
                            else:
                                progress.update(
                                    progress_task_id,
                                    filename=filename,
                                    total=total,
                                    completed=downloaded,
                                )
                        elif status == "finished":
                            if progress_task_id is not None:
                                progress.update(progress_task_id, completed=progress.tasks[progress_task_id].total)

                    opts = self.build_ytdl_options(task, progress_hook=progress_hook)
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        ydl.download([task.target_url])
                return
            except Exception as exc:
                diagnostic = diagnose_error(exc)
                if diagnostic.is_transient and attempt < max_retries:
                    console.print(
                        f"[yellow]⚠ Download encountered transient error (attempt {attempt}/{max_retries}): {exc}. "
                        f"Retrying in {retry_delay * attempt:.1f}s...[/yellow]"
                    )
                    time.sleep(retry_delay * attempt)
                    continue
                raise

