from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from youtube_downloader import __version__
from youtube_downloader.cli import app

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
    assert "--output-dir" in result.stdout or "-o" in result.stdout
    assert "--items" in result.stdout or "--playlist-items" in result.stdout


def test_cli_no_args_shows_prompt_message():
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "No Target URL provided" in result.stdout


def test_cli_parse_arguments():
    result = runner.invoke(app, [
        "https://www.youtube.com/watch?v=example123",
        "--profile", "1080p",
        "--no-subs",
        "--no-metadata",
        "--items", "1-3",
        "--dry-run"
    ])
    assert result.exit_code == 0
    assert "https://www.youtube.com/watch?v=example123" in result.stdout
    assert "1080p" in result.stdout


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
    assert task.output_destination == Path.home() / "Downloads" / "YouTube"
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
    assert task.output_destination == Path.home() / "Downloads" / "YouTube"
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
    assert task.output_destination == Path.home() / "Downloads" / "YouTube"
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
