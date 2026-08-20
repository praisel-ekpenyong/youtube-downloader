from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

from youtube_downloader.models import MediaProfile

if TYPE_CHECKING:
    from youtube_downloader.models import DownloadTask

DEFAULT_OUTPUT_ROOT = Path.home() / "Downloads" / "YouTube"


class OutputDestinationResolver:
    """Resolves Output Destination and media templates for Download Tasks."""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = Path(root_dir) if root_dir else DEFAULT_OUTPUT_ROOT

    def resolve_destination(self, task: Optional[DownloadTask] = None) -> Path:
        """Resolve the active Output Destination for a Download Task or fallback to root_dir."""
        if task is not None and task.output_destination is not None:
            return Path(task.output_destination)
        return self.root_dir

    def ensure_destination(self, task: Optional[DownloadTask] = None) -> Path:
        """Ensure the Output Destination directory exists on the filesystem and return it."""
        destination = self.resolve_destination(task=task)
        destination.mkdir(parents=True, exist_ok=True)
        return destination

    def build_output_template(self, target: Union[DownloadTask, MediaProfile]) -> str:
        """Construct the complete yt-dlp output template for a Download Task or Media Profile."""
        if isinstance(target, MediaProfile):
            destination = self.root_dir
            profile = target
        else:
            destination = self.resolve_destination(task=target)
            profile = target.media_profile

        category = profile.category_folder
        return (
            f"{destination.as_posix()}/"
            f"%(playlist_title&Playlists|{category})s/"
            f"%(playlist_title&{{}}|.)s/"
            f"%(playlist_index&{{:02d}} - |)s%(title)s [%(id)s].%(ext)s"
        )



