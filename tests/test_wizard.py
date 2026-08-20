from unittest.mock import patch
import pytest
from rich.console import Console

from youtube_downloader.models import DownloadTask, MediaProfile
from youtube_downloader.wizard import prompt_interactive_task


def test_prompt_interactive_task_default_flow():
    console = Console(record=True)
    with patch("rich.prompt.Prompt.ask") as mock_ask, patch("rich.prompt.Confirm.ask", return_value=True):
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
    assert task.embed_subtitles is True
    assert task.embed_chapters is True
    assert task.embed_metadata is True
    assert task.embed_thumbnail is True
    assert task.live_from_start is True


def test_prompt_interactive_task_audio_flac_skips_subtitles():
    console = Console(record=True)
    with patch("rich.prompt.Prompt.ask") as mock_ask, patch("rich.prompt.Confirm.ask") as mock_confirm:
        mock_ask.side_effect = [
            "https://www.youtube.com/watch?v=music123",
            "audio-flac",
            "",
        ]
        # Chapters, Metadata, Thumbnail, Live from start (4 prompts, subtitles skipped)
        mock_confirm.side_effect = [True, True, True, False]
        task = prompt_interactive_task(console=console)

    assert task is not None
    assert task.target_url == "https://www.youtube.com/watch?v=music123"
    assert task.media_profile == MediaProfile.AUDIO_FLAC
    assert task.embed_subtitles is False
    assert task.embed_chapters is True
    assert task.embed_metadata is True
    assert task.embed_thumbnail is True
    assert task.live_from_start is False
    assert mock_confirm.call_count == 4


def test_prompt_interactive_task_audio_mp3_skips_subtitles():
    console = Console(record=True)
    with patch("rich.prompt.Prompt.ask") as mock_ask, patch("rich.prompt.Confirm.ask") as mock_confirm:
        mock_ask.side_effect = [
            "https://www.youtube.com/watch?v=podcast123",
            "audio-mp3",
            "",
        ]
        # Chapters, Metadata, Thumbnail, Live from start (4 prompts, subtitles skipped)
        mock_confirm.side_effect = [True, False, True, False]
        task = prompt_interactive_task(console=console)

    assert task is not None
    assert task.target_url == "https://www.youtube.com/watch?v=podcast123"
    assert task.media_profile == MediaProfile.AUDIO_MP3
    assert task.embed_subtitles is False
    assert task.embed_chapters is True
    assert task.embed_metadata is False
    assert task.embed_thumbnail is True
    assert task.live_from_start is False
    assert mock_confirm.call_count == 4


def test_prompt_interactive_task_video_profile_prompts_subtitles():
    console = Console(record=True)
    for profile_name, profile_enum in [("720p", MediaProfile.P720), ("1080p", MediaProfile.P1080), ("best", MediaProfile.BEST)]:
        with patch("rich.prompt.Prompt.ask") as mock_ask, patch("rich.prompt.Confirm.ask") as mock_confirm:
            mock_ask.side_effect = [
                "https://www.youtube.com/watch?v=vid123",
                profile_name,
                "",
            ]
            # Subtitles, Chapters, Metadata, Thumbnail, Live from start (5 prompts)
            mock_confirm.side_effect = [True, True, True, True, True]
            task = prompt_interactive_task(console=console)

        assert task is not None
        assert task.media_profile == profile_enum
        assert task.embed_subtitles is True
        assert mock_confirm.call_count == 5


def test_prompt_interactive_task_custom_profile():
    console = Console(record=True)
    with patch("rich.prompt.Prompt.ask") as mock_ask, patch("rich.prompt.Confirm.ask", return_value=True):
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
    assert task.embed_subtitles is True
    assert task.embed_chapters is True
    assert task.embed_metadata is True
    assert task.embed_thumbnail is True
    assert task.live_from_start is True


def test_prompt_interactive_task_granular_options():
    console = Console(record=True)
    with patch("rich.prompt.Prompt.ask") as mock_ask, patch("rich.prompt.Confirm.ask") as mock_confirm:
        mock_ask.side_effect = [
            "https://www.youtube.com/watch?v=wizard123",  # URL
            "1080p",                                      # Media profile
            "2-4",                                        # Playlist items
        ]
        mock_confirm.side_effect = [
            False,  # embed_subtitles
            True,   # embed_chapters
            False,  # embed_metadata
            True,   # embed_thumbnail
            False,  # live_from_start
        ]
        task = prompt_interactive_task(console=console)

    assert task is not None
    assert task.target_url == "https://www.youtube.com/watch?v=wizard123"
    assert task.media_profile == MediaProfile.P1080
    assert task.playlist_items == "2-4"
    assert task.embed_subtitles is False
    assert task.embed_chapters is True
    assert task.embed_metadata is False
    assert task.embed_thumbnail is True
    assert task.live_from_start is False
    assert mock_confirm.call_count == 5


def test_prompt_interactive_task_empty_url_retry():
    console = Console(record=True)
    with patch("rich.prompt.Prompt.ask") as mock_ask, patch("rich.prompt.Confirm.ask", return_value=True):
        mock_ask.side_effect = [
            "",                                           # Empty URL first
            "   ",                                        # Whitespace URL second
            "https://www.youtube.com/watch?v=valid123",   # Valid URL
            "best",                                       # Media profile
            "",                                           # Playlist items
        ]
        task = prompt_interactive_task(console=console)

    assert task is not None
    assert task.target_url == "https://www.youtube.com/watch?v=valid123"


def test_prompt_interactive_task_aborted_keyboard_interrupt():
    console = Console(record=True)
    with patch("rich.prompt.Prompt.ask", side_effect=KeyboardInterrupt):
        task = prompt_interactive_task(console=console)

    assert task is None


def test_prompt_interactive_task_aborted_eof_error():
    console = Console(record=True)
    with patch("rich.prompt.Prompt.ask", side_effect=EOFError):
        task = prompt_interactive_task(console=console)

    assert task is None
