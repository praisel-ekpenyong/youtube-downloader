from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel

from youtube_downloader import __version__
from youtube_downloader.config import OutputDestinationResolver
from youtube_downloader.diagnostics import diagnose_error, render_diagnostic_panel
from youtube_downloader.engine import MediaDownloader
from youtube_downloader.models import DownloadTask, MediaProfile
from youtube_downloader.wizard import prompt_interactive_task

app = typer.Typer(
    name="ytdl",
    help="YouTube Downloader - Download, convert, and organize media from YouTube.",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"[bold cyan]ytdl[/bold cyan] version: [green]{__version__}[/green]")
        raise typer.Exit()


@app.command(help="YouTube Downloader — Download, convert, and organize media from YouTube.")
def download(
    target_url: Optional[str] = typer.Argument(
        None,
        help="The Target URL of the video, livestream, or playlist.",
        metavar="TARGET_URL",
    ),
    profile: MediaProfile = typer.Option(
        MediaProfile.BEST,
        "--profile",
        "-p",
        help="Media Profile specifying resolution, bitrate, codec, and container format.",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Custom Output Destination directory override.",
    ),
    embed_subs: bool = typer.Option(
        True,
        "--subs/--no-subs",
        help="Embed available subtitle tracks.",
    ),
    embed_metadata: bool = typer.Option(
        True,
        "--metadata/--no-metadata",
        help="Embed video tags and description metadata.",
    ),
    embed_chapters: bool = typer.Option(
        True,
        "--chapters/--no-chapters",
        help="Embed chapter markers.",
    ),
    embed_thumbnail: bool = typer.Option(
        True,
        "--thumbnail/--no-thumbnail",
        help="Embed video thumbnail artwork.",
    ),
    live_from_start: bool = typer.Option(
        True,
        "--live-from-start/--no-live-from-start",
        help="Capture livestreams from the start.",
    ),
    items: Optional[str] = typer.Option(
        None,
        "--items",
        "--playlist-items",
        help="Playlist items filter (e.g. '1-5', '1,3,5').",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Simulate execution without downloading media.",
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show ytdl version and exit.",
    ),
):
    """YouTube Downloader — Download, convert, and organize media from YouTube."""
    resolver = OutputDestinationResolver(root_dir=output_dir)
    dest_path = resolver.root_dir

    if not target_url:
        task = prompt_interactive_task(console=console)
        if task is None:
            return
        if not task.output_destination:
            task.output_destination = dest_path
    else:
        task = DownloadTask(
            target_url=target_url,
            media_profile=profile,
            output_destination=dest_path,
            embed_subtitles=embed_subs,
            embed_metadata=embed_metadata,
            embed_chapters=embed_chapters,
            embed_thumbnail=embed_thumbnail,
            live_from_start=live_from_start,
            playlist_items=items,
        )

    console.print(f"[bold green]Target URL:[/bold green] {task.target_url}")
    console.print(f"[bold cyan]Media Profile:[/bold cyan] {task.media_profile.value}")
    console.print(f"[bold magenta]Output Destination:[/bold magenta] {task.output_destination or dest_path}")

    if dry_run:
        console.print("[yellow][Dry Run] Task constructed successfully. Exiting without download.[/yellow]")
        return

    downloader = MediaDownloader()
    try:
        downloader.download(task)
        console.print("[bold green]✔ Download completed successfully![/bold green]")
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Download interrupted by user. Saved media has been finalized.[/bold yellow]")
        raise typer.Exit(code=130)
    except Exception as exc:
        report = diagnose_error(exc)
        panel = render_diagnostic_panel(report)
        console.print(panel)
        raise typer.Exit(code=1)


def main():
    app()


if __name__ == "__main__":
    main()
