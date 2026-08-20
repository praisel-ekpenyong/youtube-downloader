from pathlib import Path
import pytest
from youtube_downloader.config import OutputDestinationResolver, DEFAULT_OUTPUT_ROOT
from youtube_downloader.models import MediaProfile


def test_default_output_root():
    resolver = OutputDestinationResolver()
    expected_root = Path.home() / "Downloads" / "YouTube"
    assert resolver.root_dir == expected_root


def test_custom_output_root(tmp_path):
    custom_dir = tmp_path / "MyDownloads"
    resolver = OutputDestinationResolver(root_dir=custom_dir)
    assert resolver.root_dir == custom_dir


def test_resolve_video_destination():
    resolver = OutputDestinationResolver()
    dest = resolver.resolve_video_dir()
    assert dest == Path.home() / "Downloads" / "YouTube" / "Videos"


def test_resolve_audio_destination():
    resolver = OutputDestinationResolver()
    dest = resolver.resolve_audio_dir()
    assert dest == Path.home() / "Downloads" / "YouTube" / "Audio"


def test_resolve_playlist_destination():
    resolver = OutputDestinationResolver()
    dest = resolver.resolve_playlist_dir("Favorite Tracks")
    assert dest == Path.home() / "Downloads" / "YouTube" / "Playlists" / "Favorite Tracks"


def test_resolve_for_media_profile_video():
    resolver = OutputDestinationResolver()
    assert resolver.resolve_for_profile(MediaProfile.BEST) == resolver.resolve_video_dir()
    assert resolver.resolve_for_profile(MediaProfile.P1080) == resolver.resolve_video_dir()
    assert resolver.resolve_for_profile(MediaProfile.P720) == resolver.resolve_video_dir()


def test_resolve_for_media_profile_audio():
    resolver = OutputDestinationResolver()
    assert resolver.resolve_for_profile(MediaProfile.AUDIO_MP3) == resolver.resolve_audio_dir()
    assert resolver.resolve_for_profile(MediaProfile.AUDIO_FLAC) == resolver.resolve_audio_dir()
