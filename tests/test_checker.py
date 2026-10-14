import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from src.checker import check_url


def run(coro):
    return asyncio.run(coro)


def _mock_response(status_code: int):
    resp = MagicMock()
    resp.status_code = status_code
    return resp


def test_check_url_up():
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=_mock_response(200))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("src.checker.httpx.AsyncClient", return_value=mock_client):
        result = run(check_url("https://example.com"))

    assert result["url"] == "https://example.com"
    assert result["status"] is True
    assert isinstance(result["time"], int)


def test_check_url_non_200_is_down():
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=_mock_response(503))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("src.checker.httpx.AsyncClient", return_value=mock_client):
        result = run(check_url("https://example.com"))

    assert result["status"] is False


def test_check_url_connection_error():
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=Exception("connection refused"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)

    with patch("src.checker.httpx.AsyncClient", return_value=mock_client):
        result = run(check_url("https://unreachable.example"))

    assert result["status"] is False
    assert result["time"] is None
