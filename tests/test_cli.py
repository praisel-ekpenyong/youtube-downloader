from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from typer.testing import CliRunner
from yt_dlp.utils import DownloadError  # type: ignore[import-untyped]


from youtube_downloader import __version__
from youtube_downloader.cli import app, render_diagnostic_panel
from youtube_downloader.diagnostics import DiagnosticCategory, DiagnosticReport
from youtube_downloader.models import DownloadOutcome, DownloadTask, MediaProfile
from youtube_downloader.progress import RichProgressReporter

runner = CliRunner()


def test_cli_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "YouTube Downloader" in result.stdout
    assert "--profile" in result.stdout or "-p" in result.stdout
    assert "--output-destination" in result.stdout or "-o" in result.stdout
    assert "--custom-format" in result.stdout or "-f" in result.stdout
    assert "--items" in result.stdout or "--playlist-items" in result.stdout
    assert "--dry-run" not in result.stdout


@patch("youtube_downloader.cli.prompt_interactive_task")
@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_no_args_launches_wizard_and_downloads(mock_downloader_cls, mock_wizard):
    mock_downloader = mock_downloader_cls.return_value
    mock_wizard.return_value = DownloadTask(
        target_url="https://www.youtube.com/watch?v=wizard123",
        media_profile=MediaProfile.P1080,
    )

    result = runner.invoke(app, [])
    assert result.exit_code == 0
    mock_wizard.assert_called_once()
    mock_downloader.download.assert_called_once()
    assert "Download completed successfully" in result.stdout


@patch("youtube_downloader.cli.prompt_interactive_task")
@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_no_args_wizard_cancelled(mock_downloader_cls, mock_wizard):
    mock_downloader = mock_downloader_cls.return_value
    mock_wizard.return_value = None

    result = runner.invoke(app, [])
    assert result.exit_code == 0
    mock_wizard.assert_called_once()
    mock_downloader.download.assert_not_called()


@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_parse_arguments_and_custom_format(mock_downloader_cls):
    mock_downloader = mock_downloader_cls.return_value
    result = runner.invoke(app, [
        "https://www.youtube.com/watch?v=example123",
        "--profile", "custom",
        "--custom-format", "bestvideo[height<=480]+bestaudio/best",
        "--output-destination", "C:/tmp/yt_test",
        "--no-subs",
        "--no-metadata",
        "--items", "1-3",
    ])
    assert result.exit_code == 0
    mock_downloader.download.assert_called_once()
    task = mock_downloader.download.call_args[0][0]
    assert task.target_url == "https://www.youtube.com/watch?v=example123"
    assert task.media_profile == MediaProfile.CUSTOM
    assert task.custom_format == "bestvideo[height<=480]+bestaudio/best"
    assert task.output_destination == Path("C:/tmp/yt_test")
    assert task.embed_subtitles is False
    assert task.embed_metadata is False
    assert task.playlist_items == "1-3"


@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_short_flags(mock_downloader_cls):
    mock_downloader = mock_downloader_cls.return_value
    result = runner.invoke(app, [
        "https://www.youtube.com/watch?v=example123",
        "-p", "custom",
        "-f", "worst",
        "-o", "C:/tmp/yt_test2",
    ])
    assert result.exit_code == 0
    task = mock_downloader.download.call_args[0][0]
    assert task.media_profile == MediaProfile.CUSTOM
    assert task.custom_format == "worst"
    assert task.output_destination == Path("C:/tmp/yt_test2")


@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_output_dir_alias(mock_downloader_cls):
    mock_downloader = mock_downloader_cls.return_value
    result = runner.invoke(app, [
        "https://www.youtube.com/watch?v=example123",
        "--output-dir", "C:/tmp/yt_alias",
    ])
    assert result.exit_code == 0
    task = mock_downloader.download.call_args[0][0]
    assert task.output_destination == Path("C:/tmp/yt_alias")


@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_executes_download(mock_downloader_cls):
    mock_downloader = mock_downloader_cls.return_value
    result = runner.invoke(app, [
        "https://www.youtube.com/watch?v=example123",
        "--profile", "720p",
    ])
    assert result.exit_code == 0
    mock_downloader_cls.assert_called_once()
    mock_downloader.download.assert_called_once()
    task = mock_downloader.download.call_args[0][0]
    assert task.target_url == "https://www.youtube.com/watch?v=example123"
    assert task.media_profile.value == "720p"
    assert task.output_destination is None
    assert "Download completed successfully" in result.stdout


@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_executes_audio_mp3_download(mock_downloader_cls):
    mock_downloader = mock_downloader_cls.return_value
    result = runner.invoke(app, [
        "https://www.youtube.com/watch?v=example123",
        "--profile", "audio-mp3",
    ])
    assert result.exit_code == 0
    mock_downloader_cls.assert_called_once()
    mock_downloader.download.assert_called_once()
    task = mock_downloader.download.call_args[0][0]
    assert task.target_url == "https://www.youtube.com/watch?v=example123"
    assert task.media_profile.value == "audio-mp3"
    assert task.output_destination is None
    assert "Download completed successfully" in result.stdout


@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_executes_audio_flac_download(mock_downloader_cls):
    mock_downloader = mock_downloader_cls.return_value
    result = runner.invoke(app, [
        "https://www.youtube.com/watch?v=example123",
        "--profile", "audio-flac",
    ])
    assert result.exit_code == 0
    mock_downloader_cls.assert_called_once()
    mock_downloader.download.assert_called_once()
    task = mock_downloader.download.call_args[0][0]
    assert task.target_url == "https://www.youtube.com/watch?v=example123"
    assert task.media_profile.value == "audio-flac"
    assert task.output_destination is None
    assert "Download completed successfully" in result.stdout


@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_executes_playlist_items_download(mock_downloader_cls):
    mock_downloader = mock_downloader_cls.return_value
    result = runner.invoke(app, [
        "https://www.youtube.com/playlist?list=PL123",
        "--playlist-items", "1-5",
    ])
    assert result.exit_code == 0
    mock_downloader_cls.assert_called_once()
    mock_downloader.download.assert_called_once()
    task = mock_downloader.download.call_args[0][0]
    assert task.target_url == "https://www.youtube.com/playlist?list=PL123"
    assert task.playlist_items == "1-5"


@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_handles_download_error_with_diagnostic_card(mock_downloader_cls):
    mock_downloader = mock_downloader_cls.return_value
    mock_downloader.download.return_value = DownloadOutcome(
        task=DownloadTask(target_url="https://www.youtube.com/watch?v=age123"),
        success=False,
        diagnostic=DiagnosticReport(
            category=DiagnosticCategory.AUTH_OR_AGE_RESTRICTED,
            title="Age-Restricted or Authentication Required",
            message="This video requires authentication or age verification.",
            suggestion="Provide a valid cookies file (cookies.txt) or ensure your account has access.",
            is_transient=False,
        ),
        attempts=1,
    )

    result = runner.invoke(app, [
        "https://www.youtube.com/watch?v=age123",
    ])
    assert result.exit_code != 0
    assert "Age-Restricted" in result.stdout or "Authentication Required" in result.stdout
    assert "cookie" in result.stdout.lower()


@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_handles_missing_ffmpeg_diagnostic_card(mock_downloader_cls):
    mock_downloader = mock_downloader_cls.return_value
    mock_downloader.download.return_value = DownloadOutcome(
        task=DownloadTask(target_url="https://www.youtube.com/watch?v=audio123"),
        success=False,
        diagnostic=DiagnosticReport(
            category=DiagnosticCategory.MISSING_FFMPEG,
            title="FFmpeg Not Found",
            message="FFmpeg or FFprobe executable is required for audio extraction, muxing, and subtitles.",
            suggestion="Install FFmpeg to your system PATH or install the static-ffmpeg package.",
            is_transient=False,
        ),
        attempts=1,
    )

    result = runner.invoke(app, [
        "https://www.youtube.com/watch?v=audio123",
    ])
    assert result.exit_code == 1
    assert "FFmpeg Not Found" in result.stdout
    assert "static-ffmpeg" in result.stdout


@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_handles_keyboard_interrupt_gracefully(mock_downloader_cls):
    mock_downloader = mock_downloader_cls.return_value
    mock_downloader.download.side_effect = KeyboardInterrupt()

    result = runner.invoke(app, [
        "https://www.youtube.com/watch?v=live123",
    ])
    assert "interrupted" in result.stdout.lower()
    assert result.exit_code == 130


@patch("youtube_downloader.cli.MediaDownloader")
def test_cli_configures_rich_progress_reporter(mock_downloader_cls):
    mock_downloader = mock_downloader_cls.return_value
    result = runner.invoke(app, [
        "https://www.youtube.com/watch?v=example123",
    ])
    assert result.exit_code == 0
    mock_downloader_cls.assert_called_once()
    kwargs = mock_downloader_cls.call_args[1]
    assert "progress_reporter" in kwargs
    assert isinstance(kwargs["progress_reporter"], RichProgressReporter)


def test_render_diagnostic_panel():
    report = DiagnosticReport(
        category=DiagnosticCategory.MISSING_FFMPEG,
        title="FFmpeg Not Found",
        message="FFmpeg is required for audio extraction.",
        suggestion="Install FFmpeg.",
        is_transient=False,
    )
    panel = render_diagnostic_panel(report)
    assert panel is not None
    assert "FFmpeg Not Found" in panel.title

