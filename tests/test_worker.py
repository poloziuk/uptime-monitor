import asyncio
from unittest.mock import AsyncMock, patch

from src.worker import MonitorState, handle_result

URL = "https://example.test"


def run(coro):
    return asyncio.run(coro)


def _down():
    return {"url": URL, "status": False, "time": None}


def _up():
    return {"url": URL, "status": True, "time": 42}


def test_no_alert_below_failure_threshold():
    state = MonitorState()
    alert = AsyncMock()
    with patch("src.worker.send_slack_alert", alert), patch(
        "src.worker.save_result"
    ), patch("src.worker.FAILURE_THRESHOLD", 3):
        run(handle_result(_down(), state))
        run(handle_result(_down(), state))

    alert.assert_not_called()
    assert state.failures == 2


def test_alerts_once_on_sustained_failure():
    state = MonitorState()
    alert = AsyncMock()
    with patch("src.worker.send_slack_alert", alert), patch(
        "src.worker.save_result"
    ), patch("src.worker.FAILURE_THRESHOLD", 3):
        for _ in range(6):
            run(handle_result(_down(), state))

    # Six failed checks, one alert — not six.
    assert alert.await_count == 1
    assert "DOWN" in alert.await_args[0][0]
    assert state.alerted is True


def test_recovery_alert_after_down():
    state = MonitorState()
    alert = AsyncMock()
    with patch("src.worker.send_slack_alert", alert), patch(
        "src.worker.save_result"
    ), patch("src.worker.FAILURE_THRESHOLD", 2), patch(
        "src.worker.SUCCESS_THRESHOLD", 1
    ):
        run(handle_result(_down(), state))
        run(handle_result(_down(), state))
        run(handle_result(_up(), state))

    assert alert.await_count == 2
    assert "back UP" in alert.await_args[0][0]
    assert state.alerted is False
    assert state.failures == 0


def test_no_recovery_alert_if_never_alerted():
    state = MonitorState()
    alert = AsyncMock()
    with patch("src.worker.send_slack_alert", alert), patch(
        "src.worker.save_result"
    ), patch("src.worker.FAILURE_THRESHOLD", 3):
        run(handle_result(_down(), state))
        run(handle_result(_up(), state))

    alert.assert_not_called()


def test_db_failure_does_not_propagate():
    state = MonitorState()
    alert = AsyncMock()
    with patch("src.worker.send_slack_alert", alert), patch(
        "src.worker.save_result", side_effect=Exception("db is down")
    ), patch("src.worker.FAILURE_THRESHOLD", 1):
        run(handle_result(_down(), state))

    # Save blew up, but the alert still fired and nothing escaped.
    assert alert.await_count == 1
