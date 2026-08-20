import pytest
from yt_dlp.utils import DownloadError  # type: ignore[import-untyped]

from youtube_downloader.diagnostics import (
    DiagnosticCategory,
    DiagnosticReport,
    diagnose_error,
    render_diagnostic_panel,
)


def test_diagnose_missing_ffmpeg():
    err = Exception("ffmpeg not found, please install or specify ffmpeg_location")
    report = diagnose_error(err)
    assert report.category == DiagnosticCategory.MISSING_FFMPEG
    assert "FFmpeg" in report.title
    assert "ffmpeg" in report.suggestion.lower()


def test_diagnose_age_restricted_auth():
    err = DownloadError("Sign in to confirm your age. This video may be inappropriate for some users.")
    report = diagnose_error(err)
    assert report.category == DiagnosticCategory.AUTH_OR_AGE_RESTRICTED
    assert "Age-Restricted" in report.title or "Authentication" in report.title
    assert "cookie" in report.suggestion.lower()


def test_diagnose_geo_blocked():
    err = DownloadError("The uploader has not made this video available in your country.")
    report = diagnose_error(err)
    assert report.category == DiagnosticCategory.GEO_BLOCKED
    assert "Geo-Blocked" in report.title or "Region" in report.title
    assert "proxy" in report.suggestion.lower() or "vpn" in report.suggestion.lower()


def test_diagnose_format_unavailable():
    err = DownloadError("Requested format is not available. Use --list-formats for a list of available formats")
    report = diagnose_error(err)
    assert report.category == DiagnosticCategory.FORMAT_UNAVAILABLE
    assert "Format" in report.title
    assert "Profile" in report.suggestion or "format" in report.suggestion.lower()


def test_diagnose_not_found():
    err = DownloadError("Video unavailable. This video is private or removed.")
    report = diagnose_error(err)
    assert report.category == DiagnosticCategory.NOT_FOUND_OR_UNAVAILABLE
    assert "Unavailable" in report.title or "Not Found" in report.title


def test_diagnose_transient_network():
    err = DownloadError("HTTP Error 503: Service Unavailable. Retrying...")
    report = diagnose_error(err)
    assert report.category == DiagnosticCategory.TRANSIENT_NETWORK
    assert report.is_transient is True


def test_render_diagnostic_panel():
    report = DiagnosticReport(
        category=DiagnosticCategory.MISSING_FFMPEG,
        title="FFmpeg Not Found",
        message="FFmpeg is required for audio extraction and muxing.",
        suggestion="Install FFmpeg or use static-ffmpeg.",
        is_transient=False,
    )
    panel = render_diagnostic_panel(report)
    assert panel is not None
    assert "FFmpeg Not Found" in panel.title
