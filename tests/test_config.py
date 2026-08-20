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


def test_build_output_template(tmp_path):
    resolver = OutputDestinationResolver(root_dir=tmp_path)
    video_tmpl = resolver.build_output_template(MediaProfile.BEST)
    assert tmp_path.as_posix() in video_tmpl
    assert "Playlists|Videos" in video_tmpl
    assert "%(title)s [%(id)s].%(ext)s" in video_tmpl

    audio_tmpl = resolver.build_output_template(MediaProfile.AUDIO_MP3)
    assert tmp_path.as_posix() in audio_tmpl
    assert "Playlists|Audio" in audio_tmpl


def test_ensure_destination(tmp_path):
    dest = tmp_path / "created_dir"
    resolver = OutputDestinationResolver(root_dir=dest)
    assert not dest.exists()
    result = resolver.ensure_destination()
    assert dest.exists()
    assert result == dest

