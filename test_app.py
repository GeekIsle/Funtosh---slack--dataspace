"""Tests for the Flask upload/download service."""

import io

import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"UPLOAD_DIR": str(tmp_path), "TESTING": True})
    with app.test_client() as client:
        yield client


def _fake_video(name="clip.mp4", data=b"fake video bytes"):
    return {"file": (io.BytesIO(data), name)}


def test_upload_mp4_succeeds_and_appears_in_files(client):
    resp = client.post(
        "/upload",
        data=_fake_video(),
        content_type="multipart/form-data",
        headers={"Accept": "application/json"},
    )
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["filename"] == "clip.mp4"
    assert body["size"] == len(b"fake video bytes")
    assert body["download_url"].endswith("/download/clip.mp4")

    listing = client.get("/files").get_json()
    names = [f["filename"] for f in listing]
    assert "clip.mp4" in names


def test_upload_mov_succeeds(client):
    resp = client.post(
        "/upload",
        data=_fake_video(name="movie.mov"),
        content_type="multipart/form-data",
        headers={"Accept": "application/json"},
    )
    assert resp.status_code == 201


def test_upload_rejects_disallowed_extension(client):
    resp = client.post(
        "/upload",
        data=_fake_video(name="bad.txt", data=b"hello"),
        content_type="multipart/form-data",
        headers={"Accept": "application/json"},
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_upload_no_file_rejected(client):
    resp = client.post(
        "/upload",
        data={},
        content_type="multipart/form-data",
        headers={"Accept": "application/json"},
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_upload_empty_filename_rejected(client):
    resp = client.post(
        "/upload",
        data={"file": (io.BytesIO(b"data"), "")},
        content_type="multipart/form-data",
        headers={"Accept": "application/json"},
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_download_round_trip(client):
    payload = b"some binary content \x00\x01\x02"
    client.post(
        "/upload",
        data=_fake_video(name="round.mp4", data=payload),
        content_type="multipart/form-data",
        headers={"Accept": "application/json"},
    )
    resp = client.get("/download/round.mp4")
    assert resp.status_code == 200
    assert resp.data == payload


def test_collision_does_not_overwrite(client):
    for _ in range(2):
        client.post(
            "/upload",
            data=_fake_video(name="dup.mp4", data=b"x"),
            content_type="multipart/form-data",
            headers={"Accept": "application/json"},
        )
    listing = client.get("/files").get_json()
    names = [f["filename"] for f in listing]
    assert "dup.mp4" in names
    assert len(names) == 2


def test_exceeding_size_limit_returns_413(tmp_path):
    app = create_app(
        {"UPLOAD_DIR": str(tmp_path), "MAX_CONTENT_LENGTH": 10, "TESTING": True}
    )
    with app.test_client() as client:
        resp = client.post(
            "/upload",
            data=_fake_video(name="big.mp4", data=b"this is definitely more than ten bytes"),
            content_type="multipart/form-data",
            headers={"Accept": "application/json"},
        )
        assert resp.status_code == 413
        assert resp.get_json()["error"] == "File exceeds the 2 GB upload limit."


def test_path_traversal_download_does_not_escape(client):
    resp = client.get("/download/..%2fapp.py")
    assert resp.status_code in (400, 404)
    # The response must not be the source file's contents.
    assert b"create_app" not in resp.data


def test_html_form_upload_redirects(client):
    resp = client.post(
        "/upload",
        data=_fake_video(name="form.mp4"),
        content_type="multipart/form-data",
        headers={"Accept": "text/html"},
    )
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")
