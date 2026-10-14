from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.db import get_last_results, init_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")

HOME_PAGE_LIMIT = 100


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    results = get_last_results(HOME_PAGE_LIMIT)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"results": results},
    )


@app.get("/status")
def get_status(limit: int = Query(10, ge=1, le=1000)):
    return get_last_results(limit)
