from fastapi import FastAPI
from src.db import get_last_results, init_db

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/status")
def get_status(limit: int = 10):
    results = get_last_results(limit=limit)
    return [
        {
            "url": r.url,
            "status": r.status,
            "response_time": r.response_time,
            "timestamp": r.timestamp.isoformat()
        }
        for r in results
    ]

