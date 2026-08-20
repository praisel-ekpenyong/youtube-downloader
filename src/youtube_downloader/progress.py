from __future__ import annotations

import os
from typing import Any, Optional, Protocol, runtime_checkable

from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)


@runtime_checkable
class ProgressReporter(Protocol):
    """Protocol defining the progress reporting seam for download operations."""

    def __enter__(self) -> ProgressReporter:
        ...

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        ...

    def on_progress(self, status: dict[str, Any]) -> None:
        ...


class SilentProgressReporter:
    """A no-op progress reporter adapter for headless runs, scripts, and tests."""

    def __enter__(self) -> SilentProgressReporter:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass

    def on_progress(self, status: dict[str, Any]) -> None:
        pass


class RichProgressReporter:
    """Terminal progress reporter adapter using Rich for interactive CLI runs."""

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self._progress: Optional[Progress] = None
        self._task_id: Optional[TaskID] = None

    def __enter__(self) -> RichProgressReporter:
        self._progress = Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=40),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
            console=self.console,
            transient=True,
        )
        self._progress.start()
        self._task_id = None
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._progress is not None:
            self._progress.stop()
            self._progress = None
            self._task_id = None

    def on_progress(self, status: dict[str, Any]) -> None:
        if self._progress is None:
            return

        state = status.get("status")
        if state == "downloading":
            filename = os.path.basename(status.get("filename", "Downloading..."))
            total = status.get("total_bytes") or status.get("total_bytes_estimate") or 0
            downloaded = status.get("downloaded_bytes", 0)

            if self._task_id is None:
                self._task_id = self._progress.add_task(
                    "download",
                    filename=filename,
                    total=total,
                    completed=downloaded,
                )
            else:
                self._progress.update(
                    self._task_id,
                    filename=filename,
                    total=total,
                    completed=downloaded,
                )
        elif state == "finished":
            if self._task_id is not None:
                task_obj = self._progress.tasks[self._task_id]
                self._progress.update(self._task_id, completed=task_obj.total)
                self._task_id = None


TerminalProgressReporter = RichProgressReporter
