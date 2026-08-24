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

---

# Video Upload / Download Service

A small Flask web service (`app.py`) that lets you upload and download video
files through a browser or a JSON API.

- **Allowed types:** MP4 and MOV only (`.mp4`, `.mov`). Anything else is
  rejected with a `400` error.
- **Maximum size:** 2 GB per file. Exceeding it returns a clean `413` with a
  message stating the 2 GB limit.
- **Storage:** files are saved to the directory set by the `UPLOAD_DIR`
  environment variable (default `./uploads`, created automatically and
  git-ignored). Colliding filenames are disambiguated so uploads are never
  silently overwritten.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

The host and port are configurable via the `HOST` and `PORT` environment
variables (defaults `0.0.0.0` and `5000`). Then open http://localhost:5000/.

## Endpoints

- `GET /` — HTML page with an upload form and a list of uploaded files.
- `POST /upload` — upload a file via `multipart/form-data` (field name
  `file`). Returns JSON `{"filename", "download_url", "size"}` with `201` on
  success, or `{"error": ...}` with `400` on validation failure. Browser form
  submissions (requests that accept HTML) are redirected back to `/` instead
  of receiving JSON.
- `GET /download/<filename>` — download a stored file as an attachment.
  Returns `404` if the file does not exist. Filenames are sanitized to guard
  against path traversal.
- `GET /files` — JSON list of `{"filename", "size", "download_url"}` for every
  stored file.

## Notion logging (optional)

When configured, each successful upload is logged as a row in a Notion
database ("Dataspace Uploads") with the filename, size, upload time, and
download URL. This is controlled by two environment variables:

- `NOTION_API_KEY` — a Notion internal integration token.
- `NOTION_DATABASE_ID` — the id of the target Notion database.

If either variable is unset, uploads work exactly as normal and Notion
logging is simply skipped. A Notion API failure is caught and logged as a
warning — it never breaks the upload response.

The database lives here:
https://app.notion.com/p/c454311973244ed19c6fb262fc764cf4

### One-time setup

1. Create a Notion internal integration at
   https://www.notion.so/my-integrations and copy its token into
   `NOTION_API_KEY`.
2. Share the "Dataspace Uploads" database with that integration: open the
   database, click the `⋯` menu → **Connections**, and add your integration.
3. Set `NOTION_DATABASE_ID` to the database id (the id from the database URL,
   e.g. `c454311973244ed19c6fb262fc764cf4`).

```bash
export NOTION_API_KEY="secret_..."
export NOTION_DATABASE_ID="c454311973244ed19c6fb262fc764cf4"
python app.py
```

## Tests

```bash
pytest
```
