import re
from pathlib import Path
from typing import Optional

from youtube_downloader.models import MediaProfile

DEFAULT_OUTPUT_ROOT = Path.home() / "Downloads" / "YouTube"


def sanitize_filename(name: str) -> str:
    """Sanitize string for use in directory/file names across Windows and Unix."""
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip()


class OutputDestinationResolver:
    """Resolves output directories for videos, audio, and playlists."""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = Path(root_dir) if root_dir else DEFAULT_OUTPUT_ROOT

    def resolve_video_dir(self) -> Path:
        """Resolve the output destination directory for video media."""
        return self.root_dir / "Videos"

    def resolve_audio_dir(self) -> Path:
        """Resolve the output destination directory for audio media."""
        return self.root_dir / "Audio"

    def resolve_playlist_folder(self, playlist_title: str) -> Path:
        """Resolve the output destination directory for a playlist."""
        sanitized = sanitize_filename(playlist_title)
        return self.root_dir / "Playlists" / sanitized

    def resolve_for_profile(
        self, profile: MediaProfile, playlist_title: Optional[str] = None
    ) -> Path:
        """Resolve destination directory based on MediaProfile and playlist context."""
        if playlist_title:
            return self.resolve_playlist_folder(playlist_title)
        if profile.is_audio_only:
            return self.resolve_audio_dir()
        return self.resolve_video_dir()

    def build_output_template(self, profile: MediaProfile) -> str:
        """Build the yt-dlp outtmpl string for a given MediaProfile."""
        category = profile.category_folder
        return f"%(playlist_title&Playlists|{category})s/%(playlist_title&{{}}|.)s/%(playlist_index&{{:02d}} - |)s%(title)s [%(id)s].%(ext)s"

    def ensure_destination(self, path: Optional[Path] = None) -> Path:
        """Ensure the destination directory exists and return it."""
        target = Path(path) if path else self.root_dir
        target.mkdir(parents=True, exist_ok=True)
        return target

