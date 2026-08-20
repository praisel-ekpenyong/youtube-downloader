from pathlib import Path
from youtube_downloader.config import DEFAULT_OUTPUT_ROOT


def test_default_output_root():
    expected_root = Path.home() / "Downloads" / "YouTube"
    assert DEFAULT_OUTPUT_ROOT == expected_root





