from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.db import get_results, get_last_results, init_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    results = get_results()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": results},
    )


@app.get("/status")
def get_status(limit: int = 10):
    return get_last_results(limit)
