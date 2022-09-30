from fastapi import Form, Request, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Any, Optional
from fastapi.responses import FileResponse
import time
from runway_technical.csv_reader import csv_header

from runway_technical.reviews import fetch_reviews_id, check_url, get_url


app = FastAPI()

templates = Jinja2Templates(directory="runway_technical/templates/")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Root Endpoint"""

    return templates.TemplateResponse("index.html", {'request': request})


@app.post("/submit")
async def submit(app_id: Optional[str] = Form(None), url_string: Optional[str] = Form(None), url_itunes_string: Optional[str] = Form(None)):
    """Submit endpoint. Takes list input and cloud platform choice of AWS or GCP. Downloads csv file"""

    file_path = 'reviews.csv'
    csv_header(file_path)

    try:
        if app_id:
            fetch_reviews_id(str(app_id))
            time.sleep(2.4)

        elif url_itunes_string:
            check_url(str(url_string))
            time.sleep(2.4)
            
        elif url_string:
            get_url(str(url_string))
            time.sleep(2.4)

        else:
            print("Invalid input")
    
    except Exception as e:
        raise print(f"Error: {e}")

    return FileResponse(path=file_path, filename=file_path, media_type=file_path)