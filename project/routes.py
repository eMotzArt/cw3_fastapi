# system import
from fastapi import APIRouter, Response, Request
from fastapi.templating import Jinja2Templates
# my import
from project.paths import TEMPLATES_PATH_ABS
from project.classes import UserIDentifier, Repository

main_router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_PATH_ABS)

@main_router.get("/")
def page_index(request: Request):
    all_posts = Repository().get_all_posts()
    bookmarks_count = Repository().get_bookmarsk_count()

    return templates.TemplateResponse("index.html", {"request": request,
                                                     'bookmark_count': bookmarks_count,
                                                     'posts': all_posts,
                                                     'views_counter': 666
                                                     })

@main_router.get("/cookie-and-object/")
@main_router.post("/cookie-and-object/")
def create_cookie(response: Response, request: Request):
    result = UserIDentifier().initiate_user(request, response)

    return {"message": "Come to the dark side, we have cookies",
            "younewid": request.cookies.get('sky-uid')}