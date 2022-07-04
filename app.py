from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from project.classes import UserIDentifier
from project.routes import main_router
from project.paths import STATIC_PATH

app = FastAPI()
app.include_router(main_router)
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

