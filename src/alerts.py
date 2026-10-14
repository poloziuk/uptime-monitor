import logging

import httpx

from src.config import ALERT_TIMEOUT, SLACK_WEBHOOK

log = logging.getLogger(__name__)


async def send_slack_alert(message: str) -> None:
    """Best-effort notification. Never raises — a broken webhook must not
    take down the monitoring loop."""
    if not SLACK_WEBHOOK:
        return
    try:
        async with httpx.AsyncClient(timeout=ALERT_TIMEOUT) as client:
            resp = await client.post(SLACK_WEBHOOK, json={"text": message})
        if resp.status_code >= 400:
            log.warning("slack webhook returned %s", resp.status_code)
    except Exception:
        log.exception("failed to send slack alert")
