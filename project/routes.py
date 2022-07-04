from fastapi import APIRouter, Response, Request
from fastapi.templating import Jinja2Templates
from project.paths import TEMPLATES_PATH_ABS

main_router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_PATH_ABS)

@main_router.get("/")
def create_cookie(response: Response, request: Request):

    return templates.TemplateResponse("index.html", {"request": request})
