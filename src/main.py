import asyncio
from src.config import URLS, CHECK_INTERVAL
from src.checker import check_url
from src.db import save_result, init_db
from src.alerts import send_slack_alert

async def monitor():
    init_db()
    while True:
        tasks = [check_url(url) for url in URLS]
        results = await asyncio.gather(*tasks)
        for result in results:
            save_result(result)
            if not result["status"]:
                send_slack_alert(f"🚨 {result['url']} is DOWN")
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(monitor())

