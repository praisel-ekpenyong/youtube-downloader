from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Union


class DiagnosticCategory(str, Enum):
    """Categorized root causes for download and post-processing failures."""
    MISSING_FFMPEG = "missing_ffmpeg"
    AUTH_OR_AGE_RESTRICTED = "auth_or_age_restricted"
    GEO_BLOCKED = "geo_blocked"
    FORMAT_UNAVAILABLE = "format_unavailable"
    NOT_FOUND_OR_UNAVAILABLE = "not_found_or_unavailable"
    TRANSIENT_NETWORK = "transient_network"
    UNKNOWN = "unknown"


@dataclass
class DiagnosticReport:
    """Actionable diagnostic report for a failure."""
    category: DiagnosticCategory
    title: str
    message: str
    suggestion: str
    is_transient: bool = False


def diagnose_error(error: Union[Exception, str]) -> DiagnosticReport:
    """Analyze an exception or error message and return an actionable DiagnosticReport."""
    err_str = str(error).strip()
    err_lower = err_str.lower()

    # 1. Missing FFmpeg
    if "ffmpeg" in err_lower or "ffprobe" in err_lower:
        return DiagnosticReport(
            category=DiagnosticCategory.MISSING_FFMPEG,
            title="FFmpeg Not Found",
            message="FFmpeg or FFprobe executable is required for audio extraction, muxing, and subtitles.",
            suggestion="Install FFmpeg to your system PATH or install the static-ffmpeg package.",
            is_transient=False,
        )

    # 2. Age-restricted or Private requiring authentication
    if (
        "sign in" in err_lower
        or "confirm your age" in err_lower
        or "inappropriate for some users" in err_lower
        or "login" in err_lower
        or "members-only" in err_lower
    ):
        return DiagnosticReport(
            category=DiagnosticCategory.AUTH_OR_AGE_RESTRICTED,
            title="Age-Restricted or Authentication Required",
            message="This video requires authentication or age verification.",
            suggestion="Provide a valid cookies file (cookies.txt) or ensure your account has access.",
            is_transient=False,
        )

    # 3. Geo-blocked / Regional restrictions
    if (
        "available in your country" in err_lower
        or "blocked in your country" in err_lower
        or "geo" in err_lower
        or "region" in err_lower
    ):
        return DiagnosticReport(
            category=DiagnosticCategory.GEO_BLOCKED,
            title="Geo-Blocked Content",
            message="The uploader has restricted this video in your geographical location.",
            suggestion="Use a VPN or configure a proxy to download from an allowed region.",
            is_transient=False,
        )

    # 4. Format Unavailable
    if (
        "format is not available" in err_lower
        or "requested format not available" in err_lower
        or "no video formats" in err_lower
        or "format not available" in err_lower
    ):
        return DiagnosticReport(
            category=DiagnosticCategory.FORMAT_UNAVAILABLE,
            title="Requested Format Unavailable",
            message=f"The selected resolution or codec is not available for this media: {err_str}",
            suggestion="Try selecting a different Media Profile (e.g. 'best', '720p', or 'audio-mp3').",
            is_transient=False,
        )

    # 5. Transient Network / HTTP 5xx errors
    if (
        re.search(r"http error 5\d\d", err_lower)
        or "service unavailable" in err_lower
        or "timed out" in err_lower
        or "timeout" in err_lower
        or "connection reset" in err_lower
        or "temporary failure" in err_lower
        or "retrying" in err_lower
    ):
        return DiagnosticReport(
            category=DiagnosticCategory.TRANSIENT_NETWORK,
            title="Transient Network Error",
            message=f"Network or remote server error encountered: {err_str}",
            suggestion="Check your network connection or try again later.",
            is_transient=True,
        )

    # 6. Video Unavailable / Not Found / Deleted
    if (
        "unavailable" in err_lower
        or "private video" in err_lower
        or "does not exist" in err_lower
        or "not found" in err_lower
        or "removed" in err_lower
    ):
        return DiagnosticReport(
            category=DiagnosticCategory.NOT_FOUND_OR_UNAVAILABLE,
            title="Media Unavailable or Not Found",
            message="The requested video, playlist, or stream does not exist or has been removed.",
            suggestion="Verify that the Target URL is correct and the video is still publicly viewable.",
            is_transient=False,
        )

    # 7. Unknown / Generic fallback
    return DiagnosticReport(
        category=DiagnosticCategory.UNKNOWN,
        title="Download Error",
        message=err_str or "An unknown error occurred during download.",
        suggestion="Check the Target URL and parameters, or verify yt-dlp is updated to the latest version.",
        is_transient=False,
    )

