from unittest.mock import patch

from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)

FAKE_RESULTS = [
    {
        "id": 1,
        "url": "https://google.com",
        "status": True,
        "response_time": 120,
        "timestamp": None,
    }
]


def test_status_returns_list():
    with patch("src.api.get_last_results", return_value=FAKE_RESULTS):
        resp = client.get("/status")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["url"] == "https://google.com"
    assert data[0]["status"] is True


def test_status_limit_param():
    with patch("src.api.get_last_results", return_value=[]) as mock_fn:
        client.get("/status?limit=5")
    mock_fn.assert_called_once_with(5)


def test_status_rejects_unbounded_limit():
    with patch("src.api.get_last_results", return_value=[]):
        resp = client.get("/status?limit=99999999")
    assert resp.status_code == 422


def test_home_returns_html():
    with patch("src.api.get_last_results", return_value=FAKE_RESULTS):
        resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "https://google.com" in resp.text
