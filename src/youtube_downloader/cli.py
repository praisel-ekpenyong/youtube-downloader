from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel

from youtube_downloader import __version__
from youtube_downloader.config import OutputDestinationResolver
from youtube_downloader.diagnostics import render_diagnostic_panel
from youtube_downloader.engine import MediaDownloader
from youtube_downloader.models import DownloadTask, MediaProfile
from youtube_downloader.progress import RichProgressReporter
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
    output_destination: Optional[Path] = typer.Option(
        None,
        "--output-destination",
        "--output-dir",
        "-o",
        help="Custom Output Destination directory override.",
    ),
    custom_format: Optional[str] = typer.Option(
        None,
        "--custom-format",
        "-f",
        help="Custom yt-dlp format selector string when using custom profile.",
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
    resolver = OutputDestinationResolver(root_dir=output_destination)
    resolved_destination = resolver.resolve_destination()

    if not target_url:
        task = prompt_interactive_task(console=console)
        if task is None:
            return
        if not task.output_destination:
            task.output_destination = resolved_destination
    else:
        task = DownloadTask(
            target_url=target_url,
            media_profile=profile,
            custom_format=custom_format,
            output_destination=resolved_destination,
            embed_subtitles=embed_subs,
            embed_metadata=embed_metadata,
            embed_chapters=embed_chapters,
            embed_thumbnail=embed_thumbnail,
            live_from_start=live_from_start,
            playlist_items=items,
        )

    console.print(f"[bold green]Target URL:[/bold green] {task.target_url}")
    console.print(f"[bold cyan]Media Profile:[/bold cyan] {task.media_profile.value}")
    console.print(f"[bold magenta]Output Destination:[/bold magenta] {resolver.resolve_destination(task=task)}")

    reporter = RichProgressReporter(console=console)
    downloader = MediaDownloader(destination_resolver=resolver, progress_reporter=reporter)
    try:
        outcome = downloader.download(task)
        if outcome.success:
            console.print("[bold green]Download completed successfully![/bold green]")
        else:
            if outcome.diagnostic:
                panel = render_diagnostic_panel(outcome.diagnostic)
                console.print(panel)
            raise typer.Exit(code=1)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Download interrupted by user. Saved media has been finalized.[/bold yellow]")
        raise typer.Exit(code=130)


def main():
    app()


if __name__ == "__main__":
    main()
