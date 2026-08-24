"""A small Flask web service for uploading and downloading video files.

Only MP4 and MOV files are accepted, up to 2 GB each. Uploaded files are
stored in a directory configurable via the ``UPLOAD_DIR`` environment
variable (default ``./uploads``).

Behavior note: ``POST /upload`` always returns JSON, EXCEPT when the request
accepts HTML (i.e. a browser form submission), in which case it redirects
back to ``/`` on success and re-renders ``/`` with an error message on
validation failure. API clients that send ``Accept: application/json`` (or
anything other than HTML) always get JSON.
"""

import logging
import os
import uuid
from datetime import datetime, timezone

import requests
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template_string,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"

# 2 GiB maximum upload size.
MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024

ALLOWED_EXTENSIONS = {"mp4", "mov"}

INDEX_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Video Upload / Download</title>
</head>
<body>
  <h1>Video Upload &amp; Download</h1>
  <p>Allowed types: <strong>MP4</strong> and <strong>MOV</strong> only.
     Maximum size: <strong>2 GB</strong> per file.</p>
  {% if error %}
  <p style="color: red;"><strong>Error:</strong> {{ error }}</p>
  {% endif %}
  <form action="{{ url_for('upload') }}" method="post" enctype="multipart/form-data">
    <input type="file" name="file" accept=".mp4,.mov" required>
    <button type="submit">Upload</button>
  </form>
  <h2>Uploaded files</h2>
  {% if files %}
  <ul>
    {% for f in files %}
    <li><a href="{{ f.download_url }}">{{ f.filename }}</a> ({{ f.size }} bytes)</li>
    {% endfor %}
  </ul>
  {% else %}
  <p>No files uploaded yet.</p>
  {% endif %}
</body>
</html>
"""


def allowed_file(filename):
    """Return True if ``filename`` has an allowed (case-insensitive) extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def _unique_path(upload_dir, filename):
    """Return a filesystem path in ``upload_dir`` that does not collide.

    If ``filename`` already exists, a short uuid suffix is inserted before the
    extension so existing uploads are never silently overwritten.
    """
    candidate = os.path.join(upload_dir, filename)
    if not os.path.exists(candidate):
        return filename, candidate
    stem, dot, ext = filename.rpartition(".")
    if not dot:
        stem, ext = filename, ""
    while True:
        suffix = uuid.uuid4().hex[:8]
        new_name = f"{stem}_{suffix}" + (f".{ext}" if ext else "")
        candidate = os.path.join(upload_dir, new_name)
        if not os.path.exists(candidate):
            return new_name, candidate


def _list_files(upload_dir):
    """Return metadata for every regular file in ``upload_dir``."""
    entries = []
    if os.path.isdir(upload_dir):
        for name in sorted(os.listdir(upload_dir)):
            full = os.path.join(upload_dir, name)
            if os.path.isfile(full):
                entries.append(
                    {
                        "filename": name,
                        "size": os.path.getsize(full),
                        "download_url": url_for("download", filename=name),
                    }
                )
    return entries


def log_upload_to_notion(filename, size_bytes, download_url):
    """Log a successful upload as a row in a Notion database.

    This is a no-op unless BOTH ``NOTION_API_KEY`` and ``NOTION_DATABASE_ID``
    environment variables are set, so local runs and tests never require Notion.

    Any failure talking to Notion is caught and logged as a warning — logging to
    Notion must never break the upload response returned to the user.
    """
    api_key = os.environ.get("NOTION_API_KEY")
    database_id = os.environ.get("NOTION_DATABASE_ID")
    if not api_key or not database_id:
        return

    size_mb = round(size_bytes / (1024 * 1024), 2)
    uploaded_at = datetime.now(timezone.utc).isoformat()

    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {"title": [{"text": {"content": filename}}]},
            "Filename": {"rich_text": [{"text": {"content": filename}}]},
            "Size (MB)": {"number": size_mb},
            "Uploaded At": {"date": {"start": uploaded_at}},
            "Download URL": {"url": download_url},
        },
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            NOTION_API_URL, headers=headers, json=payload, timeout=10
        )
        response.raise_for_status()
    except Exception as exc:  # noqa: BLE001 - never let Notion break uploads
        logger.warning("Failed to log upload to Notion: %s", exc)


def create_app(config=None):
    """Application factory.

    ``config`` is an optional dict merged into ``app.config`` so tests can
    inject, for example, a smaller ``MAX_CONTENT_LENGTH`` or a temporary
    ``UPLOAD_DIR``.
    """
    app = Flask(__name__)

    upload_dir = os.environ.get("UPLOAD_DIR", os.path.join(os.getcwd(), "uploads"))
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    app.config["UPLOAD_DIR"] = os.path.abspath(upload_dir)

    if config:
        app.config.update(config)

    # Resolve and create the upload directory after any config override.
    app.config["UPLOAD_DIR"] = os.path.abspath(app.config["UPLOAD_DIR"])
    os.makedirs(app.config["UPLOAD_DIR"], exist_ok=True)

    def _wants_json():
        """True when the client prefers JSON over HTML (i.e. not a browser form)."""
        best = request.accept_mimetypes.best_match(
            ["application/json", "text/html"]
        )
        return (
            best == "application/json"
            or request.accept_mimetypes["application/json"]
            >= request.accept_mimetypes["text/html"]
        )

    @app.route("/", methods=["GET"])
    def index():
        return render_template_string(
            INDEX_TEMPLATE, files=_list_files(app.config["UPLOAD_DIR"]), error=None
        )

    @app.route("/upload", methods=["POST"])
    def upload():
        def fail(message, status=400):
            if _wants_json():
                return jsonify({"error": message}), status
            return (
                render_template_string(
                    INDEX_TEMPLATE,
                    files=_list_files(app.config["UPLOAD_DIR"]),
                    error=message,
                ),
                status,
            )

        if "file" not in request.files:
            return fail("No file part in the request.")

        file = request.files["file"]
        if not file or file.filename == "":
            return fail("No file selected.")

        if not allowed_file(file.filename):
            return fail("Unsupported file type. Only MP4 and MOV files are allowed.")

        safe_name = secure_filename(file.filename)
        if not safe_name or not allowed_file(safe_name):
            return fail("Invalid file name.")

        final_name, dest = _unique_path(app.config["UPLOAD_DIR"], safe_name)
        file.save(dest)
        size = os.path.getsize(dest)

        download_url = url_for("download", filename=final_name, _external=True)
        log_upload_to_notion(final_name, size, download_url)

        if not _wants_json():
            return redirect(url_for("index"))

        return (
            jsonify(
                {
                    "filename": final_name,
                    "download_url": url_for("download", filename=final_name),
                    "size": size,
                }
            ),
            201,
        )

    @app.route("/download/<path:filename>", methods=["GET"])
    def download(filename):
        safe_name = secure_filename(filename)
        if not safe_name:
            return jsonify({"error": "Invalid file name."}), 400
        return send_from_directory(
            app.config["UPLOAD_DIR"], safe_name, as_attachment=True
        )

    @app.route("/files", methods=["GET"])
    def files():
        return jsonify(_list_files(app.config["UPLOAD_DIR"]))

    @app.errorhandler(RequestEntityTooLarge)
    def too_large(_error):
        return jsonify({"error": "File exceeds the 2 GB upload limit."}), 413

    return app


app = create_app()


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port)
