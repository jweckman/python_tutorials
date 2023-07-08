from time import sleep

from fastapi import FastAPI, Depends, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlmodel import select, Session

from fastapi_htmx_template.db import get_session, create_db_and_tables, populate_test_data
from fastapi_htmx_template.models import User

import leather

templates = Jinja2Templates(directory="templates")

app = FastAPI(default_response_class=HTMLResponse)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index(
        *,
        session: Session = Depends(get_session),
        request: Request,
    ):
    context = {
        "request": request,
        "content": 'Hello World!',
    }
    return templates.TemplateResponse("index.html", context)

@app.get("/users/")
async def read_users(
        *,
        session: Session = Depends(get_session),
        request: Request,
    ):
    context = {
        "request": request,
        "users": session.exec(select(User)).all(),
    }
    sleep(1)
    return templates.TemplateResponse("table_users.html", context)

@app.get("/svg_chart")
async def read_svg_chart(
        session: Session = Depends(get_session),
    ):
    users = session.exec(select(User)).all()
    data = [(u.id, u.id) for u in users]

    chart = leather.Chart('Line')
    chart.add_line(data)
    return HTMLResponse(content=chart.to_svg(), status_code=200)

if __name__ == "__main__":
    create_db_and_tables()
    populate_test_data()
