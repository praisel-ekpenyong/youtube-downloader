from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


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


@dataclass
class DownloadQueue:
    """An ordered collection of Download Tasks to be executed."""
    tasks: list[DownloadTask] = field(default_factory=list)

    def add(self, task: DownloadTask) -> None:
        self.tasks.append(task)

    def __len__(self) -> int:
        return len(self.tasks)
