from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from forum_app import routes

app = FastAPI()

app.mount("/static", StaticFiles(directory="/opt/forum_app/static"), name="static")
app.mount("/icons", StaticFiles(directory="/opt/forum_app/icons"), name="icons")

templates = Jinja2Templates(directory="/opt/forum_app/templates")
