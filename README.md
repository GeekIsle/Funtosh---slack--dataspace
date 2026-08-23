# YouTube Video Downloader

A simple CLI for downloading YouTube videos you own the rights to (your own
channel's uploads, or content you have explicit permission/license to
download). Downloading other people's copyrighted videos without permission
generally violates YouTube's Terms of Service and copyright law.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Download a single video:

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download all videos from a channel:

```bash
python youtube_downloader.py --channel "https://www.youtube.com/@yourchannel/videos"
```

### Options

- `-o, --output` — output directory (default: `downloads`)
- `--channel` — treat the URL as a channel and download all its videos
- `--limit` — max number of videos to download (channel mode only)
