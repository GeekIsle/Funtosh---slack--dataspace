#!/usr/bin/env python3
"""
YouTube Video Downloader

Intended for downloading videos you own the rights to (your own channel's
uploads, or content you have explicit permission/license to download).
Downloading other people's copyrighted videos without permission generally
violates YouTube's Terms of Service and copyright law.

Requires: yt-dlp (pip install yt-dlp --break-system-packages)
"""

import sys
import argparse
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("yt-dlp not installed. Run: pip install yt-dlp --break-system-packages")
    sys.exit(1)


def download_video(url: str, output_dir: str = "downloads", quality: str = "best"):
    """
    Download a single video by URL.

    Args:
        url: The YouTube video URL
        output_dir: Folder to save the video into
        quality: yt-dlp format selector (default "best" = best available)
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "format": f"{quality}[ext=mp4]/best[ext=mp4]/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "progress_hooks": [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        print(f"\n✔ Downloaded: {filename}")
        return filename


def download_channel(channel_url: str, output_dir: str = "downloads", limit: int = None):
    """
    Download all videos from a channel (e.g. your own channel's /videos page).

    Args:
        channel_url: URL to the channel's videos page
        output_dir: Folder to save videos into
        limit: Optional max number of videos to download
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "progress_hooks": [progress_hook],
    }
    if limit:
        ydl_opts["playlistend"] = limit

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([channel_url])


def progress_hook(d):
    if d["status"] == "downloading":
        pct = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        print(f"\rDownloading... {pct} at {speed}", end="", flush=True)
    elif d["status"] == "finished":
        print("\nProcessing...")


def main():
    parser = argparse.ArgumentParser(
        description="Download YouTube videos you have rights to (e.g. your own channel)."
    )
    parser.add_argument("url", help="Video URL or channel URL")
    parser.add_argument("-o", "--output", default="downloads", help="Output directory")
    parser.add_argument("--channel", action="store_true", help="Treat URL as a channel and download all videos")
    parser.add_argument("--limit", type=int, default=None, help="Max videos to download (channel mode only)")

    args = parser.parse_args()

    if args.channel:
        download_channel(args.url, args.output, args.limit)
    else:
        download_video(args.url, args.output)


if __name__ == "__main__":
    main()
