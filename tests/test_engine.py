from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from youtube_downloader.engine import MediaDownloader
from youtube_downloader.models import DownloadTask, MediaProfile


def test_format_selection_best():
    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=MediaProfile.BEST)
    opts = downloader.build_ytdl_options(task)
    assert opts["format"] == "bestvideo+bestaudio/best"


def test_format_selection_1080p():
    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=MediaProfile.P1080)
    opts = downloader.build_ytdl_options(task)
    assert opts["format"] == "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"


def test_format_selection_720p():
    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=MediaProfile.P720)
    opts = downloader.build_ytdl_options(task)
    assert opts["format"] == "bestvideo[height<=720]+bestaudio/best[height<=720]/best"


def test_format_selection_audio_mp3():
    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        media_profile=MediaProfile.AUDIO_MP3,
        embed_metadata=True,
        embed_thumbnail=True,
    )
    opts = downloader.build_ytdl_options(task)
    assert opts["format"] == "bestaudio/best"
    
    postprocessors = opts.get("postprocessors", [])
    audio_pp = next((pp for pp in postprocessors if pp.get("key") == "FFmpegExtractAudio"), None)
    assert audio_pp is not None
    assert audio_pp.get("preferredcodec") == "mp3"
    assert audio_pp.get("preferredquality") in ("320", "0")
    
    # Check that metadata and thumbnails are also configured
    assert any(pp.get("key") == "FFmpegMetadata" for pp in postprocessors)
    assert any(pp.get("key") == "EmbedThumbnail" for pp in postprocessors)
    # Audio tasks should not embed subtitles
    assert not any(pp.get("key") == "FFmpegEmbedSubtitle" for pp in postprocessors)


def test_format_selection_audio_flac():
    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        media_profile=MediaProfile.AUDIO_FLAC,
    )
    opts = downloader.build_ytdl_options(task)
    assert opts["format"] == "bestaudio/best"
    
    postprocessors = opts.get("postprocessors", [])
    audio_pp = next((pp for pp in postprocessors if pp.get("key") == "FFmpegExtractAudio"), None)
    assert audio_pp is not None
    assert audio_pp.get("preferredcodec") == "flac"


def test_format_selection_custom():
    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        media_profile=MediaProfile.CUSTOM,
        custom_format="worst",
    )
    opts = downloader.build_ytdl_options(task)
    assert opts["format"] == "worst"


def test_subtitles_enabled_and_disabled():
    downloader = MediaDownloader()
    
    task_with_subs = DownloadTask(target_url="https://youtube.com/watch?v=123", embed_subtitles=True)
    opts_with_subs = downloader.build_ytdl_options(task_with_subs)
    assert opts_with_subs.get("writesubtitles") is True
    assert opts_with_subs.get("writeautomaticsub") is True
    assert any(pp.get("key") == "FFmpegEmbedSubtitle" for pp in opts_with_subs.get("postprocessors", []))

    task_no_subs = DownloadTask(target_url="https://youtube.com/watch?v=123", embed_subtitles=False)
    opts_no_subs = downloader.build_ytdl_options(task_no_subs)
    assert opts_no_subs.get("writesubtitles") is False
    assert not any(pp.get("key") == "FFmpegEmbedSubtitle" for pp in opts_no_subs.get("postprocessors", []))


def test_metadata_and_chapters_and_thumbnail():
    downloader = MediaDownloader()
    
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        embed_metadata=True,
        embed_chapters=True,
        embed_thumbnail=True,
    )
    opts = downloader.build_ytdl_options(task)
    assert opts.get("writethumbnail") is True
    postprocessor_keys = [pp.get("key") for pp in opts.get("postprocessors", [])]
    assert "FFmpegMetadata" in postprocessor_keys
    assert "EmbedThumbnail" in postprocessor_keys


def test_livestream_and_concurrency_options():
    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123", live_from_start=True)
    opts = downloader.build_ytdl_options(task)
    assert opts.get("live_from_start") is True
    assert opts.get("concurrent_fragment_downloads") == 6


def test_output_template_and_paths(tmp_path):
    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        output_destination=tmp_path / "Videos",
    )
    opts = downloader.build_ytdl_options(task)
    assert "paths" in opts
    assert opts["paths"]["home"] == str(tmp_path / "Videos")
    assert "%(title)s [%(id)s].%(ext)s" in opts["outtmpl"]["default"]


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_download_execution(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123")
    
    downloader.download(task)

    mock_ytdl_class.assert_called_once()
    mock_instance.download.assert_called_once_with(["https://youtube.com/watch?v=123"])


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_download_retries_on_transient_error_and_succeeds(mock_ytdl_class):
    from yt_dlp.utils import DownloadError  # type: ignore[import-untyped]

    mock_instance = MagicMock()
    mock_instance.download.side_effect = [
        DownloadError("HTTP Error 503: Service Unavailable"),
        None,
    ]
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123")
    downloader.download(task, max_retries=3, retry_delay=0.001)

    assert mock_instance.download.call_count == 2


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_download_retries_exhaustion_raises(mock_ytdl_class):
    from yt_dlp.utils import DownloadError  # type: ignore[import-untyped]

    mock_instance = MagicMock()
    mock_instance.download.side_effect = DownloadError("HTTP Error 503: Service Unavailable")
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123")

    with pytest.raises(DownloadError):
        downloader.download(task, max_retries=3, retry_delay=0.001)

    assert mock_instance.download.call_count == 3


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_download_does_not_retry_on_non_transient_error(mock_ytdl_class):
    from yt_dlp.utils import DownloadError  # type: ignore[import-untyped]

    mock_instance = MagicMock()
    mock_instance.download.side_effect = DownloadError("Sign in to confirm your age.")
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123")

    with pytest.raises(DownloadError):
        downloader.download(task, max_retries=3, retry_delay=0.001)

    assert mock_instance.download.call_count == 1

