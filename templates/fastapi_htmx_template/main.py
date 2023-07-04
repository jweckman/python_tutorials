from time import sleep

from fastapi import FastAPI, Depends, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlmodel import select, Session

from fastapi_htmx_template.db import get_session, create_db_and_tables, populate_test_data
from fastapi_htmx_template.models import User

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
        session: Session = Depends(get_session),
    ):
    users = session.exec(select(User)).all()
    user_cols = ['id', 'name','birth_year','join_date']
    html_table_rows = []
    html_table_rows.append("<tr><th>{}</th><th>{}</th><th>{}</th><th>{}</th></tr>".format(*user_cols))
    for u in users:
        tr = ''.join([f"<td>{getattr(u, col)}</td>" for col in user_cols])
        tr = f"<tr>{tr}</tr>"
        html_table_rows.append(tr)
    html = f"<html><head></head><body><table>{''.join(html_table_rows) or '<td>empty</td>'}</table></body></html>"
    sleep(1)
    return HTMLResponse(content=html, status_code=200)

if __name__ == "__main__":
    create_db_and_tables()
    populate_test_data()
