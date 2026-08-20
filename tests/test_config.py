from pathlib import Path
import pytest
from youtube_downloader.config import OutputDestinationResolver, DEFAULT_OUTPUT_ROOT
from youtube_downloader.models import DownloadTask, MediaProfile


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
    video_task = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=MediaProfile.BEST)
    video_tmpl = resolver.build_output_template(video_task)
    assert tmp_path.as_posix() in video_tmpl
    assert "Playlists|Videos" in video_tmpl
    assert "%(title)s [%(id)s].%(ext)s" in video_tmpl

    audio_task = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=MediaProfile.AUDIO_MP3)
    audio_tmpl = resolver.build_output_template(audio_task)
    assert tmp_path.as_posix() in audio_tmpl
    assert "Playlists|Audio" in audio_tmpl


def test_ensure_destination(tmp_path):
    dest = tmp_path / "created_dir"
    resolver = OutputDestinationResolver(root_dir=dest)
    assert not dest.exists()
    result = resolver.ensure_destination()
    assert dest.exists()
    assert result == dest


def test_resolve_destination_default():
    resolver = OutputDestinationResolver()
    assert resolver.resolve_destination() == DEFAULT_OUTPUT_ROOT


def test_resolve_destination_from_task(tmp_path):
    resolver = OutputDestinationResolver()
    custom_dest = tmp_path / "CustomTaskDest"
    task = DownloadTask(target_url="https://youtube.com/watch?v=123", output_destination=custom_dest)
    assert resolver.resolve_destination(task=task) == custom_dest


def test_ensure_destination_from_task(tmp_path):
    target_dir = tmp_path / "TaskFolder"
    task = DownloadTask(target_url="https://youtube.com/watch?v=123", output_destination=target_dir)
    resolver = OutputDestinationResolver()
    assert not target_dir.exists()
    res = resolver.ensure_destination(task=task)
    assert target_dir.exists()
    assert res == target_dir


def test_build_output_template_from_task(tmp_path):
    resolver = OutputDestinationResolver(root_dir=tmp_path / "Default")

    task1 = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=MediaProfile.BEST)
    tmpl1 = resolver.build_output_template(task1)
    assert (tmp_path / "Default").as_posix() in tmpl1
    assert "Playlists|Videos" in tmpl1
    assert "%(playlist_index&{:02d} - |)s%(title)s [%(id)s].%(ext)s" in tmpl1

    task2 = DownloadTask(
        target_url="https://youtube.com/watch?v=123",
        media_profile=MediaProfile.AUDIO_FLAC,
        output_destination=tmp_path / "CustomAudio",
    )
    tmpl2 = resolver.build_output_template(task2)
    assert (tmp_path / "CustomAudio").as_posix() in tmpl2
    assert "Playlists|Audio" in tmpl2


def test_destination_resolver_renders_paths_correctly(tmp_path):
    import yt_dlp  # type: ignore[import-untyped]
    resolver = OutputDestinationResolver(root_dir=tmp_path)

    # 1. Single video rendering
    video_task = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=MediaProfile.BEST)
    video_tmpl = resolver.build_output_template(video_task)
    ydl_video = yt_dlp.YoutubeDL({"outtmpl": {"default": video_tmpl}})
    single_vid_info = {"title": "Sample Video", "id": "vid001", "ext": "mp4"}
    vid_path = Path(ydl_video.prepare_filename(single_vid_info))
    assert vid_path == tmp_path / "Videos" / "Sample Video [vid001].mp4"

    # 2. Single audio rendering
    audio_task = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=MediaProfile.AUDIO_MP3)
    audio_tmpl = resolver.build_output_template(audio_task)
    ydl_audio = yt_dlp.YoutubeDL({"outtmpl": {"default": audio_tmpl}})
    single_aud_info = {"title": "Sample Song", "id": "aud001", "ext": "mp3"}
    aud_path = Path(ydl_audio.prepare_filename(single_aud_info))
    assert aud_path == tmp_path / "Audio" / "Sample Song [aud001].mp3"

    # 3. Playlist video rendering with isolation and track index
    pl_vid_info = {
        "title": "Episode 1",
        "id": "ep001",
        "ext": "mp4",
        "playlist_title": "Documentary Series",
        "playlist_index": 1,
    }
    pl_vid_path = Path(ydl_video.prepare_filename(pl_vid_info))
    assert pl_vid_path == tmp_path / "Playlists" / "Documentary Series" / "01 - Episode 1 [ep001].mp4"

    # 4. Playlist audio rendering with isolation and track index
    pl_aud_info = {
        "title": "Track 12",
        "id": "trk012",
        "ext": "flac",
        "playlist_title": "Symphony No 9",
        "playlist_index": 12,
    }
    flac_task = DownloadTask(target_url="https://youtube.com/watch?v=123", media_profile=MediaProfile.AUDIO_FLAC)
    ydl_flac = yt_dlp.YoutubeDL({"outtmpl": {"default": resolver.build_output_template(flac_task)}})
    pl_aud_path = Path(ydl_flac.prepare_filename(pl_aud_info))
    assert pl_aud_path == tmp_path / "Playlists" / "Symphony No 9" / "12 - Track 12 [trk012].flac"




