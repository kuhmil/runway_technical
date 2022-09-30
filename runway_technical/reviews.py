import urllib.request, json
from datetime import datetime, timedelta
from requests_html import HTMLSession
import logging
import dateutil.parser
from dateutil.tz import UTC
from runway_technical.csv_reader import csv_reader
import re


ITUNES_RSS_URL: str = "https://itunes.apple.com/rss/customerreviews/id={id}/page={page}/sortby=mostrecent/json"
store_app_id = {}

def url_link(app_id, page_number):
    """Create URL for feed"""

    url = ITUNES_RSS_URL.format(id=app_id, page=page_number)
    return url


def get_source(url):
    """Check if URL is valid"""

    try:
        session = HTMLSession()
        response = session.get(url)
        return response.status_code

    except Exception as e:
        logging.error(f"URL does not exist: {e}")


def time_iso_utc(time_stamp):
    """Convert to UTC time"""

    time_stamp = dateutil.parser.isoparse(time_stamp).astimezone(UTC).replace(tzinfo=None)
    return time_stamp

def time_check(entry_time_stamp):
    """Check time difference between now and the review. All in UTC time"""

    time_limit = (datetime.utcnow()- timedelta(hours = 24)).replace(microsecond=0)
    entry_time_stamp = time_iso_utc(entry_time_stamp)
    time_delta = ((time_limit-entry_time_stamp).total_seconds())/ 60

    return float(time_delta)


def fetch_reviews_id(app_id, page_number=1):
    """Fetch app reviews within the 24 hour limit. Pagination stops when the time limit has been reached"""
    
    url = url_link(app_id, page_number)

    if get_source(url) == 200:
        try:
            page_count = 0

            with urllib.request.urlopen(url) as f:
                data = json.loads(f.read().decode()).get('feed')

            if data.get('entry') == None:
                fetch_reviews_id(app_id, page_number+1)


            for entry in data.get('entry'):
                title = entry.get('title').get('label')
                time_stamp = entry.get('updated').get('label')
                rating = entry.get('im:rating').get('label')
                review = entry.get('content').get('label')
                vote_count = entry.get('im:voteCount').get('label')
                
                if time_check(time_stamp) <= 1440.00: #1440 minutes = 24 hours
                    data = [title, time_iso_utc(time_stamp), rating, review, vote_count]
                    csv_reader(data)

                else:
                    page_count += 1

            if page_count == 0:            
                fetch_reviews_id(app_id, page_number+1)

        except Exception as e:
                logging.error(f"fetch_reviews_id: {e}")


def get_url(user_input):
    """Parses user input into a readable value. Stores app id in a dictionary"""
    get_id = re.findall('\d+', user_input)
    app_id = str(get_id[0])
    store_app_id["app_id"] = app_id
    fetch_reviews_id(app_id)