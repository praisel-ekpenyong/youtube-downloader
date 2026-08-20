from __future__ import annotations

import os
import shutil
from pathlib import Path
import time
from typing import Any, Callable, Optional

import yt_dlp  # type: ignore[import-untyped]

from youtube_downloader.config import OutputDestinationResolver
from youtube_downloader.diagnostics import diagnose_error
from youtube_downloader.models import DownloadOutcome, DownloadTask, MediaProfile
from youtube_downloader.progress import ProgressReporter, SilentProgressReporter


def find_ffmpeg_location() -> Optional[str]:
    """Locate FFmpeg executable directory from system PATH, environment, or static_ffmpeg."""
    if shutil.which("ffmpeg"):
        return None  # System FFmpeg is already in PATH
    ffmpeg_env = os.environ.get("FFMPEG_LOCATION") or os.environ.get("FFMPEG_PATH")
    if ffmpeg_env:
        return ffmpeg_env
    try:
        import static_ffmpeg  # type: ignore[import-untyped]
        static_ffmpeg.add_paths()
        if shutil.which("ffmpeg"):
            return None
    except Exception:
        pass
    return None


_PROFILE_FORMAT_SELECTORS: dict[MediaProfile, str] = {
    MediaProfile.BEST: "bestvideo+bestaudio/best",
    MediaProfile.P1080: "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
    MediaProfile.P720: "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
    MediaProfile.AUDIO_MP3: "bestaudio/best",
    MediaProfile.AUDIO_FLAC: "bestaudio/best",
}

_PROFILE_AUDIO_POSTPROCESSORS: dict[MediaProfile, dict[str, Any]] = {
    MediaProfile.AUDIO_MP3: {
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "320",
    },
    MediaProfile.AUDIO_FLAC: {
        "key": "FFmpegExtractAudio",
        "preferredcodec": "flac",
        "preferredquality": "0",
    },
}


class MediaDownloader:
    """Core download engine wrapping yt-dlp with rich feedback and media profiles."""

    def __init__(
        self,
        ffmpeg_dir: Optional[str] = None,
        destination_resolver: Optional[OutputDestinationResolver] = None,
        progress_reporter: Optional[ProgressReporter] = None,
    ):
        self.ffmpeg_dir = ffmpeg_dir or find_ffmpeg_location()
        self.destination_resolver = destination_resolver or OutputDestinationResolver()
        self.progress_reporter: ProgressReporter = progress_reporter or SilentProgressReporter()

    @staticmethod
    def _get_format_for_profile(profile: MediaProfile, custom_format: Optional[str] = None) -> str:
        """Resolve format selector string based on MediaProfile."""
        if profile == MediaProfile.CUSTOM:
            return custom_format or _PROFILE_FORMAT_SELECTORS[MediaProfile.BEST]
        return _PROFILE_FORMAT_SELECTORS.get(profile, _PROFILE_FORMAT_SELECTORS[MediaProfile.BEST])

    @staticmethod
    def _get_audio_postprocessor_for_profile(profile: MediaProfile) -> Optional[dict[str, Any]]:
        """Resolve audio extraction postprocessor configuration for MediaProfile, if applicable."""
        postprocessor = _PROFILE_AUDIO_POSTPROCESSORS.get(profile)
        return dict(postprocessor) if postprocessor is not None else None

    def _build_ytdl_options(
        self,
        task: DownloadTask,
        progress_hook: Optional[Callable[[dict[str, Any]], None]] = None,
    ) -> dict[str, Any]:
        """Construct yt-dlp options dictionary from a DownloadTask."""
        postprocessors: list[dict[str, Any]] = []

        outtmpl_str = self.destination_resolver.build_output_template(task)

        opts: dict[str, Any] = {
            "format": self._get_format_for_profile(task.media_profile, task.custom_format),
            "outtmpl": {"default": outtmpl_str},
            "noplaylist": False,
            "quiet": True,
            "no_warnings": True,
            "concurrent_fragment_downloads": 6,
            "downloader": {"default": "m3u8:native"},
            "live_from_start": task.live_from_start,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"],
                }
            },
        }

        if self.ffmpeg_dir:
            opts["ffmpeg_location"] = self.ffmpeg_dir

        if task.playlist_items:
            opts["playlist_items"] = task.playlist_items
            opts["noplaylist"] = False

        # Audio extraction postprocessors
        audio_pp = self._get_audio_postprocessor_for_profile(task.media_profile)
        if audio_pp:
            postprocessors.append(audio_pp)

        # Subtitles (only for video profiles)
        if task.media_profile.supports_subtitles and task.embed_subtitles:
            opts["writesubtitles"] = True
            opts["writeautomaticsub"] = True
            opts["subtitleslangs"] = ["en.*", "en", "-live_chat"]
            opts["subtitlesignoreerrors"] = True
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
        progress_reporter: Optional[ProgressReporter] = None,
    ) -> DownloadOutcome:
        """Execute the DownloadTask using yt-dlp with progress reporting and automatic retries."""
        self.destination_resolver.ensure_destination(task=task)
        reporter = progress_reporter or self.progress_reporter
        opts = self._build_ytdl_options(task, progress_hook=reporter.on_progress)

        attempt = 0
        while True:
            attempt += 1
            try:
                with reporter:
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        ydl.download([task.target_url])
                return DownloadOutcome(
                    task=task,
                    success=True,
                    attempts=attempt,
                )
            except Exception as exc:
                diagnostic = diagnose_error(exc)
                if diagnostic.is_transient and attempt <= max_retries:
                    time.sleep(retry_delay * attempt)
                    continue
                return DownloadOutcome(
                    task=task,
                    success=False,
                    diagnostic=diagnostic,
                    attempts=attempt,
                    error=exc,
                )

