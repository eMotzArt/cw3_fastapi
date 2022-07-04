from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from project.classes import UserIDentifier
from project.routes import main_router

app = FastAPI()
app.include_router(main_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/cookie-and-object/")
@app.post("/cookie-and-object/")
def create_cookie(response: Response, request: Request):
    result = UserIDentifier().initiate_user(request, response)

    return {"message": "Come to the dark side, we have cookies",
            "younewid": request.cookies.get('sky-uid')}