from pathlib import Path
from typing import Optional

from youtube_downloader.models import MediaProfile

DEFAULT_OUTPUT_ROOT = Path.home() / "Downloads" / "YouTube"


class OutputDestinationResolver:
    """Resolves Output Destination paths and media templates for Download Tasks."""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = Path(root_dir) if root_dir else DEFAULT_OUTPUT_ROOT

    def build_output_template(self, profile: MediaProfile) -> str:
        """Construct the complete yt-dlp output template under the configured Output Destination."""
        category = profile.category_folder
        return (
            f"{self.root_dir.as_posix()}/"
            f"%(playlist_title&Playlists|{category})s/"
            f"%(playlist_title&{{}}|.)s/"
            f"%(playlist_index&{{:02d}} - |)s%(title)s [%(id)s].%(ext)s"
        )

    def ensure_destination(self, path: Optional[Path] = None) -> Path:
        """Ensure the Output Destination directory exists on the filesystem and return it."""
        target = Path(path) if path else self.root_dir
        target.mkdir(parents=True, exist_ok=True)
        return target

