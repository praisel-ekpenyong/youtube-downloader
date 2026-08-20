from unittest.mock import patch
import pytest
from rich.console import Console

from youtube_downloader.models import DownloadTask, MediaProfile
from youtube_downloader.wizard import prompt_interactive_task


def test_prompt_interactive_task_default_flow():
    console = Console(record=True)
    with patch("rich.prompt.Prompt.ask") as mock_ask:
        mock_ask.side_effect = [
            "https://www.youtube.com/watch?v=wizard123",  # URL
            "best",                                       # Media profile
            "",                                           # Playlist items
        ]
        task = prompt_interactive_task(console=console)

    assert task is not None
    assert task.target_url == "https://www.youtube.com/watch?v=wizard123"
    assert task.media_profile == MediaProfile.BEST
    assert task.playlist_items is None


def test_prompt_interactive_task_audio_flac():
    console = Console(record=True)
    with patch("rich.prompt.Prompt.ask") as mock_ask:
        mock_ask.side_effect = [
            "https://www.youtube.com/watch?v=music123",
            "audio-flac",
            "",
        ]
        task = prompt_interactive_task(console=console)

    assert task is not None
    assert task.target_url == "https://www.youtube.com/watch?v=music123"
    assert task.media_profile == MediaProfile.AUDIO_FLAC


def test_prompt_interactive_task_custom_profile():
    console = Console(record=True)
    with patch("rich.prompt.Prompt.ask") as mock_ask:
        mock_ask.side_effect = [
            "https://www.youtube.com/watch?v=custom123",
            "custom",
            "worstvideo+worstaudio",
            "1-3",
        ]
        task = prompt_interactive_task(console=console)

    assert task is not None
    assert task.target_url == "https://www.youtube.com/watch?v=custom123"
    assert task.media_profile == MediaProfile.CUSTOM
    assert task.custom_format == "worstvideo+worstaudio"
    assert task.playlist_items == "1-3"


def test_prompt_interactive_task_aborted():
    console = Console(record=True)
    with patch("rich.prompt.Prompt.ask", side_effect=KeyboardInterrupt):
        task = prompt_interactive_task(console=console)

    assert task is None
