import io
from unittest.mock import MagicMock
import pytest
from rich.console import Console

from youtube_downloader.progress import (
    ProgressReporter,
    RichProgressReporter,
    SilentProgressReporter,
    TerminalProgressReporter,
)


def test_silent_progress_reporter_protocol_and_lifecycle():
    reporter = SilentProgressReporter()
    assert isinstance(reporter, ProgressReporter)

    with reporter as active_reporter:
        assert active_reporter is reporter
        # Calling on_progress with various events should not raise
        active_reporter.on_progress({"status": "downloading", "filename": "video.mp4", "downloaded_bytes": 100, "total_bytes": 200})
        active_reporter.on_progress({"status": "finished", "filename": "video.mp4"})
        active_reporter.on_progress({"status": "other"})


def test_terminal_progress_reporter_is_rich_reporter():
    assert TerminalProgressReporter is RichProgressReporter
    reporter = TerminalProgressReporter()
    assert isinstance(reporter, ProgressReporter)


def test_rich_progress_reporter_lifecycle_and_updates():
    output = io.StringIO()
    test_console = Console(file=output, force_terminal=False)
    reporter = RichProgressReporter(console=test_console)
    assert isinstance(reporter, ProgressReporter)

    with reporter as active:
        assert active._progress is not None
        # First download event creates task
        active.on_progress({
            "status": "downloading",
            "filename": "C:/tmp/test_video.mp4",
            "downloaded_bytes": 500,
            "total_bytes": 1000,
        })
        assert active._task_id is not None
        task_id1 = active._task_id
        task1 = active._progress.tasks[task_id1]
        assert task1.total == 1000
        assert task1.completed == 500
        assert task1.fields["filename"] == "test_video.mp4"

        # Subsequent download event updates task
        active.on_progress({
            "status": "downloading",
            "filename": "C:/tmp/test_video.mp4",
            "downloaded_bytes": 800,
            "total_bytes": 1000,
        })
        assert active._task_id == task_id1
        assert task1.completed == 800

        # Finished event marks task complete and resets task_id for next item
        active.on_progress({
            "status": "finished",
            "filename": "C:/tmp/test_video.mp4",
        })
        assert task1.completed == 1000
        assert active._task_id is None

        # Next file in playlist creates a new task
        active.on_progress({
            "status": "downloading",
            "filename": "C:/tmp/second_video.mp4",
            "downloaded_bytes": 100,
            "total_bytes": 500,
        })
        assert active._task_id is not None
        assert active._task_id != task_id1
        task2 = active._progress.tasks[active._task_id]
        assert task2.fields["filename"] == "second_video.mp4"

        # Unknown status is ignored
        active.on_progress({"status": "unknown"})

    # After exiting context, progress is stopped and cleared
    assert active._progress is None
    assert active._task_id is None


def test_rich_progress_reporter_fallback_total_estimate():
    output = io.StringIO()
    test_console = Console(file=output, force_terminal=False)
    reporter = RichProgressReporter(console=test_console)

    with reporter as active:
        active.on_progress({
            "status": "downloading",
            "filename": "test.mp4",
            "downloaded_bytes": 100,
            "total_bytes_estimate": 500,
        })
        assert active._task_id is not None
        task = active._progress.tasks[active._task_id]
        assert task.total == 500
        assert task.completed == 100


def test_rich_progress_reporter_outside_context_is_noop():
    reporter = RichProgressReporter()
    # Calling on_progress when not in context manager should be a safe no-op
    reporter.on_progress({"status": "downloading", "filename": "test.mp4"})
    assert reporter._task_id is None


def test_custom_progress_reporter_protocol():
    class CustomReporter:
        def __init__(self):
            self.events = []

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def on_progress(self, d):
            self.events.append(d)

    custom = CustomReporter()
    assert isinstance(custom, ProgressReporter)
    with custom as r:
        r.on_progress({"status": "downloading"})
    assert len(custom.events) == 1
