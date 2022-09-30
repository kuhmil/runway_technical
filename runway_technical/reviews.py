import urllib.request, json, time, csv, sys
from datetime import datetime, timezone, timedelta
from requests_html import HTMLSession
import requests
import logging
import pytz as pytz
import dateutil.parser
from dateutil.parser import parse
from dateutil.tz import UTC
import pandas as pd
from runway_technical.csv_reader import csv_reader
import re


ITUNES_RSS_URL: str = "https://itunes.apple.com/rss/customerreviews/id={id}/page={page}/sortby=mostrecent/json"


def url_link(app_id, page_number):
    url = ITUNES_RSS_URL.format(id=app_id, page=page_number)
    return url


def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response.status_code

    except Exception as e:
        logging.error(f"URL does not exist: {e}")



def time_check(entry_time_stamp):

    time_one_day = (datetime.utcnow()- timedelta(hours = 24)).replace(microsecond=0)
    entry_time_stamp = dateutil.parser.isoparse(entry_time_stamp).astimezone(UTC).replace(tzinfo=None)
    time_delta = ((time_one_day-entry_time_stamp).total_seconds())/ 60

    return float(time_delta)

def fetch_reviews_id(app_id, page_number=1):

    url = url_link(app_id, page_number)

    try:
        page_count = 0

        with urllib.request.urlopen(url) as f:
            data = json.loads(f.read().decode()).get('feed')

                  
        if data.get('entry') == None:
            fetch_reviews_id(app_id, page_number+1)


        for entry in data.get('entry'):
            title = entry.get('title').get('label')
            author = entry.get('author').get('name').get('label')
            time_stamp = entry.get('updated').get('label')      
            version = entry.get('im:version').get('label')
            rating = entry.get('im:rating').get('label')
            review = entry.get('content').get('label')
            vote_count = entry.get('im:voteCount').get('label')
        
            if time_check(time_stamp) <= 1440.00:
                data = [title,  author, time_stamp ,version, rating, review, vote_count]
                print(data)
                csv_reader(data)

            else:
                page_count += 1

        if page_count == 0:            
            fetch_reviews_id(app_id, page_number+1)


    except Exception as e:
        logging.error(f"fetch_reviews: {e}")


def fetch_reviews_url(url):

    try:
        with urllib.request.urlopen(url) as f:
            data = json.loads(f.read().decode()).get('feed')


        for entry in data.get('entry'):
            title = entry.get('title').get('label')
            author = entry.get('author').get('name').get('label')
            time_stamp = entry.get('updated').get('label')      
            version = entry.get('im:version').get('label')
            rating = entry.get('im:rating').get('label')
            review = entry.get('content').get('label')
            vote_count = entry.get('im:voteCount').get('label')
            
            if time_check(time_stamp) <= 1440.00:
                data = [title,  author, time_stamp ,version, rating, review, vote_count]
                csv_reader(data)

    except Exception as e:
        logging.error(f"fetch_reviews: {e}")


def check_url(user_input):
    try:
        if get_source(user_input) == 200:
            fetch_reviews_url(user_input)
            
    except Exception as e:
        logging.error(f"URL does not exist: {e}")

def get_url(user_input):
    get_id = re.findall('\d+', user_input)
    app_id = str(get_id[0])
    fetch_reviews_id(app_id, page_number=1)