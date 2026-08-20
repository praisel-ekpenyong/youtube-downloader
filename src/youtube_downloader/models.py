from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class MediaProfile(str, Enum):
    """Predefined configuration specifying video resolution, audio bitrate, codec, and container format."""
    BEST = "best"
    P1080 = "1080p"
    P720 = "720p"
    AUDIO_MP3 = "audio-mp3"
    AUDIO_FLAC = "audio-flac"
    CUSTOM = "custom"

    @property
    def is_audio_only(self) -> bool:
        return self in (MediaProfile.AUDIO_MP3, MediaProfile.AUDIO_FLAC)

    @property
    def category_folder(self) -> str:
        """Subdirectory name under the output destination for this profile."""
        return "Audio" if self.is_audio_only else "Videos"

    @property
    def supports_subtitles(self) -> bool:
        """Whether this profile supports embedding subtitle tracks."""
        return not self.is_audio_only

    @property
    def audio_postprocessor(self) -> Optional[dict[str, Any]]:
        """Audio extraction postprocessor configuration, if applicable."""
        match self:
            case MediaProfile.AUDIO_MP3:
                return {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            case MediaProfile.AUDIO_FLAC:
                return {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "flac",
                    "preferredquality": "0",
                }
            case _:
                return None

    def get_format_selector(self, custom_format: Optional[str] = None) -> str:
        """Resolve the yt-dlp format selector string for this profile."""
        match self:
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


@dataclass
class DownloadTask:
    """A single discrete unit of work representing retrieval, post-processing, and storage."""
    target_url: str
    media_profile: MediaProfile = MediaProfile.BEST
    output_destination: Optional[Path] = None
    embed_subtitles: bool = True
    embed_metadata: bool = True
    embed_chapters: bool = True
    embed_thumbnail: bool = True
    live_from_start: bool = True
    playlist_items: Optional[str] = None
    custom_format: Optional[str] = None

