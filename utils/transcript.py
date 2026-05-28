"""
utils/transcript.py
--------------------
Extracts YouTube transcript and video metadata.
Uses youtube-transcript-api (free, no API key needed).
"""

import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
)


def _extract_video_id(url: str) -> str | None:
    """Extracts video ID from any YouTube URL format."""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"(?:youtu\.be\/)([0-9A-Za-z_-]{11})",
        r"(?:embed\/)([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript(url: str) -> tuple[str, str | None]:
    """
    Fetches the transcript of a YouTube video.

    Returns
    -------
    (transcript_text, error_message)
    If successful: (text, None)
    If failed:     ("", error_string)
    """
    video_id = _extract_video_id(url)
    if not video_id:
        return "", "Invalid YouTube URL. Please check and try again."

    try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id)

        transcript = " ".join(
            [item.text for item in transcript_list]
        )

        return transcript, None

    except Exception as e:
        return "", str(e)
        full_text = " ".join(
            segment["text"].strip()
            for segment in transcript_list
            if segment.get("text", "").strip()
        )

        # Clean up common transcript artifacts
        full_text = re.sub(r"\[.*?\]", "", full_text)   # remove [Music], [Applause]
        full_text = re.sub(r"\s+", " ", full_text).strip()

        if not full_text:
            return "", "Transcript is empty. The video may not have readable captions."

        return full_text, None

    except TranscriptsDisabled:
        return "", "Transcripts are disabled for this video."
    except VideoUnavailable:
        return "", "Video is unavailable or private."
    except NoTranscriptFound:
        return "", (
            "No transcript found. The video may not have subtitles. "
            "Try a video with auto-generated captions enabled."
        )
    except Exception as e:
        return "", f"Could not fetch transcript: {str(e)}"


def get_video_info(url: str) -> dict:
    """
    Returns basic video metadata using yt-dlp (optional).
    Falls back gracefully if yt-dlp is not installed.
    """
    video_id = _extract_video_id(url)
    if not video_id:
        return {}

    try:
        import yt_dlp

        ydl_opts = {
            "quiet":     True,
            "no_warnings": True,
            "skip_download": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            duration_sec = info.get("duration", 0)
            minutes      = duration_sec // 60
            seconds      = duration_sec % 60

            return {
                "title":    info.get("title",    "Unknown Title"),
                "channel":  info.get("uploader", "Unknown Channel"),
                "duration": f"{minutes}:{seconds:02d}",
                "views":    f"{info.get('view_count', 0):,}",
                "video_id": video_id,
            }
    except Exception:
        # yt-dlp not installed or failed — return minimal info
        return {
            "title":    "YouTube Video",
            "channel":  "—",
            "duration": "—",
            "video_id": video_id,
        }
