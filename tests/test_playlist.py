from pathlib import Path
import pytest
import yt_dlp  # type: ignore[import-untyped]

from youtube_downloader.engine import MediaDownloader
from youtube_downloader.models import DownloadTask, MediaProfile


def test_playlist_items_options():
    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/playlist?list=PL123",
        playlist_items="1-5",
    )
    opts = downloader.build_ytdl_options(task)
    assert opts.get("noplaylist") is False
    assert opts.get("playlist_items") == "1-5"


def test_playlist_without_items_allows_full_playlist():
    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/playlist?list=PL123",
        playlist_items=None,
    )
    opts = downloader.build_ytdl_options(task)
    assert opts.get("noplaylist") is False


def test_playlist_output_template_routing(tmp_path):
    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/playlist?list=PL123",
        output_destination=tmp_path,
        media_profile=MediaProfile.BEST,
    )
    opts = downloader.build_ytdl_options(task)
    ydl = yt_dlp.YoutubeDL(opts)

    # Test single video rendering
    single_info = {"title": "Single Video", "id": "abc123", "ext": "mp4"}
    single_path = Path(ydl.prepare_filename(single_info))
    assert single_path == tmp_path / "Videos" / "Single Video [abc123].mp4"

    # Test playlist video rendering with track numbering and folder
    playlist_info = {
        "title": "Track One",
        "id": "trk001",
        "ext": "mp4",
        "playlist_title": "Best Hits",
        "playlist_index": 1,
    }
    playlist_path = Path(ydl.prepare_filename(playlist_info))
    assert playlist_path == tmp_path / "Playlists" / "Best Hits" / "01 - Track One [trk001].mp4"


def test_playlist_audio_output_template_routing(tmp_path):
    downloader = MediaDownloader()
    task = DownloadTask(
        target_url="https://youtube.com/playlist?list=PL123",
        output_destination=tmp_path,
        media_profile=MediaProfile.AUDIO_MP3,
    )
    opts = downloader.build_ytdl_options(task)
    ydl = yt_dlp.YoutubeDL(opts)

    # Single audio
    single_info = {"title": "Single Song", "id": "aud123", "ext": "mp3"}
    single_path = Path(ydl.prepare_filename(single_info))
    assert single_path == tmp_path / "Audio" / "Single Song [aud123].mp3"

    # Playlist audio
    playlist_info = {
        "title": "Album Track",
        "id": "alb005",
        "ext": "mp3",
        "playlist_title": "Greatest Album",
        "playlist_index": 5,
    }
    playlist_path = Path(ydl.prepare_filename(playlist_info))
    assert playlist_path == tmp_path / "Playlists" / "Greatest Album" / "05 - Album Track [alb005].mp3"
