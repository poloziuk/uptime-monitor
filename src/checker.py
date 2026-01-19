import httpx
import time


async def check_url(url: str):
    try:
        start = time.perf_counter()
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=5.0)
        elapsed = int((time.perf_counter() - start) * 1000)
        return {"url": url, "status": resp.status_code == 200, "time": elapsed}
    except Exception:
        return {"url": url, "status": False, "time": None}
