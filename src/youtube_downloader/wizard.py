from __future__ import annotations

from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from youtube_downloader.models import DownloadTask, MediaProfile


def prompt_interactive_task(console: Optional[Console] = None) -> Optional[DownloadTask]:
    """Guide the user interactively through configuring a DownloadTask."""
    c = console or Console()
    c.print(
        Panel.fit(
            "[bold cyan]YouTube Downloader — Interactive Wizard[/bold cyan]\n"
            "Configure your download step-by-step. Press [yellow]Ctrl+C[/yellow] at any time to cancel.",
            title="ytdl wizard",
            border_style="cyan",
        )
    )

    try:
        # 1. Target URL
        target_url = ""
        while not target_url:
            target_url = Prompt.ask("[bold green]Enter Target URL[/bold green]", console=c).strip()
            if not target_url:
                c.print("[red]Target URL cannot be empty. Please enter a valid URL.[/red]")

        # 2. Media Profile
        profile_choices = [p.value for p in MediaProfile]
        profile_str = Prompt.ask(
            "[bold cyan]Select Media Profile[/bold cyan]",
            choices=profile_choices,
            default=MediaProfile.BEST.value,
            console=c,
        )
        media_profile = MediaProfile(profile_str)

        custom_format: Optional[str] = None
        if media_profile == MediaProfile.CUSTOM:
            custom_format = Prompt.ask(
                "[bold cyan]Enter custom yt-dlp format selector[/bold cyan]",
                default="bestvideo+bestaudio/best",
                console=c,
            ).strip()

        # 3. Playlist items range
        items_input = Prompt.ask(
            "[bold magenta]Playlist item range (optional, e.g. '1-5', leave blank for all)[/bold magenta]",
            default="",
            console=c,
        ).strip()
        playlist_items = items_input if items_input else None

        # 4. Enrichment and recording options
        embed_subtitles = False
        if not media_profile.is_audio_only:
            embed_subtitles = Confirm.ask(
                "[bold cyan]Embed subtitle tracks (if available)?[/bold cyan]",
                default=True,
                console=c,
            )

        embed_chapters = Confirm.ask(
            "[bold cyan]Embed chapter markers?[/bold cyan]",
            default=True,
            console=c,
        )

        embed_metadata = Confirm.ask(
            "[bold cyan]Embed metadata tags?[/bold cyan]",
            default=True,
            console=c,
        )

        embed_thumbnail = Confirm.ask(
            "[bold cyan]Embed thumbnail artwork?[/bold cyan]",
            default=True,
            console=c,
        )

        live_from_start = Confirm.ask(
            "[bold cyan]Record livestreams from start (if applicable)?[/bold cyan]",
            default=True,
            console=c,
        )

        return DownloadTask(
            target_url=target_url,
            media_profile=media_profile,
            custom_format=custom_format,
            playlist_items=playlist_items,
            embed_subtitles=embed_subtitles,
            embed_metadata=embed_metadata,
            embed_chapters=embed_chapters,
            embed_thumbnail=embed_thumbnail,
            live_from_start=live_from_start,
        )

    except (KeyboardInterrupt, EOFError):
        c.print("\n[yellow]Interactive wizard cancelled.[/yellow]")
        return None
