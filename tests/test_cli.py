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
