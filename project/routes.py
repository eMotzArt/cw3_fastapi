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

    data_for_template = {
        'request': request,
        'bookmarks_count': bookmarks_count,
        'posts': all_posts
    }
    return templates.TemplateResponse("index.html", data_for_template)

@main_router.get("/post/{post_id}")
def page_post_by_id(request: Request, post_id: int):
    post_by_id = Repository().get_post_by_id(post_id)
    comments_by_post_id = Repository().get_comments_by_post_id(post_id)

    data_for_template = {
        "request": request,
        'comments': comments_by_post_id,
        'post': post_by_id
    }

    return templates.TemplateResponse("post.html", data_for_template)

@main_router.get("/search/")
def page_search(request: Request, search_line: str):
    posts_by_search_line = Repository().get_post_by_search_line(search_line)

    data_for_template = {
        "request": request,
        'posts': posts_by_search_line
    }

    return templates.TemplateResponse("search.html", data_for_template)

@main_router.get("/users/{user_name}")
def page_posts_by_user(request: Request, user_name: str):
    posts_by_user_name = Repository().get_post_by_user_name(user_name)

    data_for_template = {
        "request": request,
        'posts': posts_by_user_name
    }
    return templates.TemplateResponse("user-feed.html", data_for_template)

@main_router.get("/tag/{tag_name}")
def page_posts_by_tag(request: Request, tag_name: str):
    posts_by_tag = Repository().get_post_by_tag(tag_name)

    data_for_template = {
        "request": request,
        "tag":  tag_name,
        'posts': posts_by_tag
    }
    return templates.TemplateResponse("tag.html", data_for_template)







@main_router.get("/api/posts")
def page_index_all_json(request: Request):
    all_posts = Repository().get_all_posts()
    return all_posts

@main_router.get("/api/posts/{post_id}")
def page_index_all_json(request: Request, post_id: int):
    post_by_id = Repository().get_post_by_id(post_id)
    return post_by_id
















@main_router.get("/cookie-and-object/")
@main_router.post("/cookie-and-object/")
def create_cookie(response: Response, request: Request):
    result = UserIDentifier().initiate_user(request, response)

    return {"message": "Come to the dark side, we have cookies",
            "younewid": request.cookies.get('sky-uid')}