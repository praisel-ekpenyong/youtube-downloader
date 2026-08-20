import re
from pathlib import Path
from typing import Optional

from youtube_downloader.models import MediaProfile

DEFAULT_OUTPUT_ROOT = Path.home() / "Downloads" / "YouTube"


def sanitize_filename(name: str) -> str:
    """Sanitize string for use in directory/file names across Windows and Unix."""
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip()


class OutputDestinationResolver:
    """Resolves output directories and templates for media downloads."""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = Path(root_dir) if root_dir else DEFAULT_OUTPUT_ROOT

    def build_output_template(self, profile: MediaProfile) -> str:
        """Build the yt-dlp outtmpl string for a given MediaProfile under the root destination."""
        category = profile.category_folder
        return f"%(playlist_title&Playlists|{category})s/%(playlist_title&{{}}|.)s/%(playlist_index&{{:02d}} - |)s%(title)s [%(id)s].%(ext)s"

    def ensure_destination(self, path: Optional[Path] = None) -> Path:
        """Ensure the destination directory exists and return it."""
        target = Path(path) if path else self.root_dir
        target.mkdir(parents=True, exist_ok=True)
        return target

