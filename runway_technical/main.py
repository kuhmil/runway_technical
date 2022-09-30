from fastapi import Form, Request, FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every
from runway_technical.csv_reader import csv_header, csv_check
from runway_technical.reviews import get_url, store_app_id
from typing import Optional
import time


app = FastAPI()

templates = Jinja2Templates(directory="runway_technical/templates/")

file_path = 'reviews.csv'
csv_header(file_path)


def user_input(app_id, url_string):
    """Evaluates if there is a value for either one. If there are two inputs the url_string is taken into account over the app ID input"""

    if app_id:
        app_input = app_id

    if url_string:
        app_input = url_string
    
    return app_input



@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Root Endpoint"""

    return templates.TemplateResponse("index.html", {'request': request})


@app.post("/submit")
async def submit(app_id: Optional[str] = Form(None), url_string: Optional[str] = Form(None)):
    """Submit endpoint. Takes user input and uses the app ID to find reviews on the app. Outputs a csv with the reviews if there has been any in the last 24 hours"""

    try:
        app_id_input = user_input(app_id, url_string)

        if app_id_input:
            get_url(app_id_input)
            time.sleep(2.4)

        else:
            print("Invalid input")
    
    except Exception as e:
        csv_check(file_path, ["An exception was raised"])
        raise print(f"Error: {e}")

    csv_check(file_path, ["There are no reviews in the last 24 hours"])

    return FileResponse(path=file_path, filename=file_path, media_type=file_path)


@app.on_event("startup")
@repeat_every(seconds=24 * 60 * 60) # Currently set to every 24 hours
async def csv_refresh():
    """Updates csv if run locally or through docker. The seconds can be adjusted to the timing preference"""

    if store_app_id["app_id"]:
        get_url(store_app_id["app_id"])