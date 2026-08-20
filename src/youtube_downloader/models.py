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

