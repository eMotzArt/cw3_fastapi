# system import

from fastapi import APIRouter, Response, Request, Form, File, UploadFile, Query, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
# my import
from pydantic import BaseModel

from project.paths import TEMPLATES_PATH_ABS
from project.classes import UserIDentifier, Repository

main_router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_PATH_ABS)

#main route
@main_router.get("/")
def page_index(request: Request):
    if not UserIDentifier().is_user_registered(request):
        return RedirectResponse(url=main_router.url_path_for('page_reg'), status_code=302)

    all_posts = Repository().get_all_posts()
    bookmarks_count = Repository().get_bookmarsk_count(UserIDentifier().generate_user_id(request))

    data_for_template = {
        'request': request,
        'bookmarks_count': bookmarks_count,
        'posts': all_posts
    }
    return templates.TemplateResponse("index.html", data_for_template)

#reg_routes
@main_router.get("/reg")
def page_reg(request: Request):
    data_for_template = {'request': request}
    return templates.TemplateResponse("reg.html", data_for_template)

@main_router.post("/reg")
def page_reg_post(request: Request, response: Response, reg_name: str = Form(...), reg_avatar: UploadFile = File(...)):

    UserIDentifier().register_new_user(request, response, reg_name, reg_avatar)

    return RedirectResponse(url=main_router.url_path_for('page_index'), status_code=302)


#post_routes
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

@main_router.get("/add_comment/{post_id}")
def page_test(request: Request, post_id: int):
    comment_content = request.query_params.get('comment_content')
    user_name = UserIDentifier().get_user_name(request)
    Repository().add_comment(post_id,user_name,comment_content)

    return RedirectResponse(url=main_router.url_path_for('page_post_by_id', post_id=post_id), status_code=302)



#api_posts
@main_router.get("/api/posts")
def page_index_all_json():
    all_posts = Repository().get_all_posts()
    return all_posts

@main_router.get("/api/posts/{post_id}")
def page_index_all_json(post_id: int):
    post_by_id = Repository().get_post_by_id(post_id)
    return post_by_id



from pydantic import BaseModel
class Data(BaseModel):
    name: str

@main_router.get("/{post_id}/getlike")
def getlike(request: Request, post_id:int):
    x=2
    ...