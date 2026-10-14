import asyncio
import logging
import time
from dataclasses import dataclass

from src.alerts import send_slack_alert
from src.checker import check_url
from src.config import (
    CHECK_INTERVAL,
    FAILURE_THRESHOLD,
    SUCCESS_THRESHOLD,
    URLS,
)
from src.db import init_db, save_result

log = logging.getLogger(__name__)


@dataclass
class MonitorState:
    failures: int = 0
    successes: int = 0
    alerted: bool = False


async def handle_result(result: dict, state: MonitorState) -> None:
    url = result["url"]

    try:
        save_result(result)
    except Exception:
        log.exception("failed to persist result for %s", url)

    if result["status"]:
        state.successes += 1
        state.failures = 0
        if state.alerted and state.successes >= SUCCESS_THRESHOLD:
            await send_slack_alert(f"✅ {url} is back UP")
            state.alerted = False
    else:
        state.failures += 1
        state.successes = 0
        if not state.alerted and state.failures >= FAILURE_THRESHOLD:
            await send_slack_alert(
                f"🚨 {url} is DOWN after {state.failures} failed checks"
            )
            state.alerted = True


async def run_cycle(states: dict) -> None:
    results = await asyncio.gather(
        *(check_url(url) for url in URLS), return_exceptions=True
    )
    for url, result in zip(URLS, results):
        if isinstance(result, BaseException):
            log.error("check raised for %s", url, exc_info=result)
            result = {"url": url, "status": False, "time": None}
        await handle_result(result, states[url])


async def monitor() -> None:
    init_db()
    states = {url: MonitorState() for url in URLS}
    log.info("monitoring %d url(s) every %ds", len(URLS), CHECK_INTERVAL)

    while True:
        started = time.monotonic()
        try:
            await run_cycle(states)
        except Exception:
            log.exception("check cycle failed")
        # Sleep the remainder of the interval so cadence doesn't drift by
        # however long the checks took.
        await asyncio.sleep(max(0.0, CHECK_INTERVAL - (time.monotonic() - started)))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    asyncio.run(monitor())
