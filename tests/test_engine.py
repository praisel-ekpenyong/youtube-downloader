from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from youtube_downloader.engine import MediaDownloader, find_ffmpeg_location
from youtube_downloader.models import DownloadTask, MediaProfile
from youtube_downloader.progress import (
    ProgressReporter,
    RichProgressReporter,
    SilentProgressReporter,
)


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_format_selection_best(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=MediaProfile.BEST)
    downloader.download(task)

    mock_instance.download.assert_called_once_with(["https://youtube.com/watch?v=123"])
    opts = mock_ytdl_class.call_args[0][0]
    assert opts["format"] == "bestvideo+bestaudio/best"


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_format_selection_1080p(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=MediaProfile.P1080)
    downloader.download(task)

    mock_instance.download.assert_called_once_with(["https://youtube.com/watch?v=123"])
    opts = mock_ytdl_class.call_args[0][0]
    assert opts["format"] == "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_format_selection_720p(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=MediaProfile.P720)
    downloader.download(task)

    mock_instance.download.assert_called_once_with(["https://youtube.com/watch?v=123"])
    opts = mock_ytdl_class.call_args[0][0]
    assert opts["format"] == "bestvideo[height<=720]+bestaudio/best[height<=720]/best"


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_format_selection_audio_mp3(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        media_profile=MediaProfile.AUDIO_MP3,
        embed_metadata=True,
        embed_thumbnail=True,
    )
    downloader.download(task)

    mock_instance.download.assert_called_once_with(["https://youtube.com/watch?v=123"])
    opts = mock_ytdl_class.call_args[0][0]
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


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_format_selection_audio_flac(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        media_profile=MediaProfile.AUDIO_FLAC,
    )
    downloader.download(task)

    mock_instance.download.assert_called_once_with(["https://youtube.com/watch?v=123"])
    opts = mock_ytdl_class.call_args[0][0]
    assert opts["format"] == "bestaudio/best"

    postprocessors = opts.get("postprocessors", [])
    audio_pp = next((pp for pp in postprocessors if pp.get("key") == "FFmpegExtractAudio"), None)
    assert audio_pp is not None
    assert audio_pp.get("preferredcodec") == "flac"


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_format_selection_custom(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        media_profile=MediaProfile.CUSTOM,
        custom_format="worst",
    )
    downloader.download(task)

    mock_instance.download.assert_called_once_with(["https://youtube.com/watch?v=123"])
    opts = mock_ytdl_class.call_args[0][0]
    assert opts["format"] == "worst"


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_format_selection_custom_default_fallback(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        media_profile=MediaProfile.CUSTOM,
        custom_format=None,
    )
    downloader.download(task)

    opts = mock_ytdl_class.call_args[0][0]
    assert opts["format"] == "bestvideo+bestaudio/best"


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_subtitles_enabled_and_disabled(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()

    task_with_subs = DownloadTask(target_url="https://youtube.com/watch?v=123", embed_subtitles=True)
    downloader.download(task_with_subs)
    opts_with_subs = mock_ytdl_class.call_args[0][0]
    assert opts_with_subs.get("writesubtitles") is True
    assert opts_with_subs.get("writeautomaticsub") is True
    assert any(pp.get("key") == "FFmpegEmbedSubtitle" for pp in opts_with_subs.get("postprocessors", []))

    task_no_subs = DownloadTask(target_url="https://youtube.com/watch?v=123", embed_subtitles=False)
    downloader.download(task_no_subs)
    opts_no_subs = mock_ytdl_class.call_args[0][0]
    assert opts_no_subs.get("writesubtitles") is False
    assert not any(pp.get("key") == "FFmpegEmbedSubtitle" for pp in opts_no_subs.get("postprocessors", []))


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_metadata_and_chapters_and_thumbnail(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()

    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        embed_metadata=True,
        embed_chapters=True,
        embed_thumbnail=True,
    )
    downloader.download(task)
    opts = mock_ytdl_class.call_args[0][0]
    assert opts.get("writethumbnail") is True
    postprocessor_keys = [pp.get("key") for pp in opts.get("postprocessors", [])]
    assert "FFmpegMetadata" in postprocessor_keys
    assert "EmbedThumbnail" in postprocessor_keys


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_livestream_and_concurrency_options(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123", live_from_start=True)
    downloader.download(task)
    opts = mock_ytdl_class.call_args[0][0]
    assert opts.get("live_from_start") is True
    assert opts.get("concurrent_fragment_downloads") == 6


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_output_template_and_paths(mock_ytdl_class, tmp_path):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        output_destination=tmp_path / "Videos",
    )
    downloader.download(task)
    opts = mock_ytdl_class.call_args[0][0]
    assert (tmp_path / "Videos").as_posix() in opts["outtmpl"]["default"]
    assert "%(title)s [%(id)s].%(ext)s" in opts["outtmpl"]["default"]


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_download_execution(mock_ytdl_class, tmp_path):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        output_destination=tmp_path / "Videos",
    )

    downloader.download(task)

    mock_ytdl_class.assert_called_once()
    mock_instance.download.assert_called_once_with(["https://youtube.com/watch?v=123"])


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_download_retries_on_transient_error_and_succeeds(mock_ytdl_class, tmp_path):
    from yt_dlp.utils import DownloadError  # type: ignore[import-untyped]

    mock_instance = MagicMock()
    mock_instance.download.side_effect = [
        DownloadError("HTTP Error 503: Service Unavailable"),
        None,
    ]
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        output_destination=tmp_path / "Videos",
    )
    downloader.download(task, max_retries=3, retry_delay=0.001)

    assert mock_instance.download.call_count == 2


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_download_retries_exhaustion_raises(mock_ytdl_class, tmp_path):
    from yt_dlp.utils import DownloadError  # type: ignore[import-untyped]

    mock_instance = MagicMock()
    mock_instance.download.side_effect = DownloadError("HTTP Error 503: Service Unavailable")
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        output_destination=tmp_path / "Videos",
    )

    with pytest.raises(DownloadError):
        downloader.download(task, max_retries=3, retry_delay=0.001)

    assert mock_instance.download.call_count == 3


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_download_does_not_retry_on_non_transient_error(mock_ytdl_class, tmp_path):
    from yt_dlp.utils import DownloadError  # type: ignore[import-untyped]

    mock_instance = MagicMock()
    mock_instance.download.side_effect = DownloadError("Sign in to confirm your age.")
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        output_destination=tmp_path / "Videos",
    )

    with pytest.raises(DownloadError):
        downloader.download(task, max_retries=3, retry_delay=0.001)

    assert mock_instance.download.call_count == 1


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_video_profiles_do_not_configure_audio_postprocessors(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    for profile in (MediaProfile.BEST, MediaProfile.P1080, MediaProfile.P720, MediaProfile.CUSTOM):
        task = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=profile)
        downloader.download(task)
        opts = mock_ytdl_class.call_args[0][0]
        postprocessors = opts.get("postprocessors", [])
        assert not any(pp.get("key") == "FFmpegExtractAudio" for pp in postprocessors)


def test_downloader_encapsulates_translation_internals():
    downloader = MediaDownloader()
    assert not hasattr(downloader, "build_ytdl_options")
    assert not hasattr(downloader, "get_format_for_profile")
    assert not hasattr(downloader, "get_audio_postprocessor_for_profile")


def test_media_profile_domain_properties():
    assert MediaProfile.BEST.category_folder == "Videos"
    assert MediaProfile.P1080.category_folder == "Videos"
    assert MediaProfile.P720.category_folder == "Videos"
    assert MediaProfile.AUDIO_MP3.category_folder == "Audio"
    assert MediaProfile.AUDIO_FLAC.category_folder == "Audio"

    assert MediaProfile.BEST.supports_subtitles is True
    assert MediaProfile.AUDIO_MP3.supports_subtitles is False
    assert MediaProfile.AUDIO_FLAC.supports_subtitles is False

    # Models must remain decoupled from backend library specifics
    assert not hasattr(MediaProfile.BEST, "audio_postprocessor")
    assert not hasattr(MediaProfile.BEST, "get_format_selector")


def test_find_ffmpeg_location_in_path():
    with patch("shutil.which", return_value="C:/ffmpeg/bin/ffmpeg.exe"):
        assert find_ffmpeg_location() is None


def test_find_ffmpeg_location_not_in_path_with_env():
    with patch("shutil.which", return_value=None), patch.dict("os.environ", {"FFMPEG_LOCATION": "C:/custom_ffmpeg/bin"}):
        assert find_ffmpeg_location() == "C:/custom_ffmpeg/bin"


def test_find_ffmpeg_location_not_found():
    with patch("shutil.which", return_value=None), patch.dict("os.environ", {"FFMPEG_LOCATION": "", "FFMPEG_PATH": ""}, clear=False):
        with patch.dict("os.environ", {}, clear=True):
            assert find_ffmpeg_location() is None


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_extractor_args_configured(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader()
    task = DownloadTask(target_url="https://youtube.com/watch?v=123")
    downloader.download(task)
    opts = mock_ytdl_class.call_args[0][0]
    assert "extractor_args" in opts
    assert opts["extractor_args"]["youtube"]["player_client"] == ["android", "web"]


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_ffmpeg_location_configured(mock_ytdl_class):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    downloader = MediaDownloader(ffmpeg_dir="C:/custom_ffmpeg/bin")
    task = DownloadTask(target_url="https://youtube.com/watch?v=123")
    downloader.download(task)
    opts = mock_ytdl_class.call_args[0][0]
    assert opts["ffmpeg_location"] == "C:/custom_ffmpeg/bin"


def test_find_ffmpeg_location_static_ffmpeg():
    with patch("shutil.which", side_effect=[None, "C:/static_ffmpeg/bin/ffmpeg.exe"]):
        with patch.dict("os.environ", {}, clear=True):
            assert find_ffmpeg_location() is None


def test_downloader_default_progress_reporter_is_silent():
    downloader = MediaDownloader()
    assert isinstance(downloader.progress_reporter, SilentProgressReporter)


def test_downloader_accepts_progress_reporter_at_init():
    custom_reporter = SilentProgressReporter()
    downloader = MediaDownloader(progress_reporter=custom_reporter)
    assert downloader.progress_reporter is custom_reporter


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_downloader_uses_progress_reporter_during_download(mock_ytdl_class, tmp_path):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    class TrackingReporter:
        def __init__(self):
            self.entered = False
            self.exited = False
            self.events = []

        def __enter__(self):
            self.entered = True
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.exited = True

        def on_progress(self, data):
            self.events.append(data)

    reporter = TrackingReporter()
    downloader = MediaDownloader(progress_reporter=reporter)
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        output_destination=tmp_path / "Videos",
    )

    downloader.download(task)

    assert reporter.entered is True
    assert reporter.exited is True
    opts = mock_ytdl_class.call_args[0][0]
    assert opts.get("progress_hooks") == [reporter.on_progress]


@patch("youtube_downloader.engine.yt_dlp.YoutubeDL")
def test_downloader_download_override_progress_reporter(mock_ytdl_class, tmp_path):
    mock_instance = MagicMock()
    mock_ytdl_class.return_value.__enter__.return_value = mock_instance

    default_reporter = MagicMock(spec=ProgressReporter)
    default_reporter.__enter__.return_value = default_reporter

    override_reporter = MagicMock(spec=ProgressReporter)
    override_reporter.__enter__.return_value = override_reporter

    downloader = MediaDownloader(progress_reporter=default_reporter)
    task = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        output_destination=tmp_path / "Videos",
    )

    downloader.download(task, progress_reporter=override_reporter)

    default_reporter.__enter__.assert_not_called()
    override_reporter.__enter__.assert_called_once()

