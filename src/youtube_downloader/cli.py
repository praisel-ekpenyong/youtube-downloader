from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.panel import Panel

from youtube_downloader import __version__
from youtube_downloader.config import OutputDestinationResolver
from youtube_downloader.models import DownloadTask, MediaProfile

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
    if not target_url:
        console.print(
            Panel.fit(
                "[bold yellow]No Target URL provided.[/bold yellow]\n"
                "Run [cyan]ytdl --help[/cyan] for usage instructions, or provide a URL.",
                title="YouTube Downloader",
            )
        )
        return

    resolver = OutputDestinationResolver(root_dir=output_dir)
    dest_path = resolver.resolve_for_profile(profile)

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
    console.print(f"[bold magenta]Output Destination:[/bold magenta] {dest_path}")
    if dry_run:
        console.print("[yellow][Dry Run] Task constructed successfully. Exiting without download.[/yellow]")
        return


def main():
    app()


if __name__ == "__main__":
    main()
