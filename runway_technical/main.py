import requests
import pandas as pd
from requests_html import HTMLSession
import feedparser


def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.
P
    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_feed(url):
    """Return a Pandas dataframe containing the RSS feed contents.

    Args: 
        url (string): URL of the RSS feed to read.

    Returns:
        df (dataframe): Pandas dataframe containing the RSS feed contents.
    """
    
    response = get_source(url)
    
    df = pd.DataFrame(columns = ['bozo', 'entries', 'feed', 'headers', 'href', 'status', 'encoding', 'bozo_exception', 'version', 'namespaces'])
    print(df)

    with response as r:
        items = r.html.find("item", first=False)

        for item in items:
            print(item)     

    #         title = item.find('title', first=True).text
    #         pubDate = item.find('pubDate', first=True).text
    #         guid = item.find('guid', first=True).text
    #         description = item.find('description', first=True).text

    #         row = {'title': title, 'pubDate': pubDate, 'guid': guid, 'description': description}
    #         df = df.append(row, ignore_index=True)

    # return df


feed_url = "https://itunes.apple.com/us/rss/customerreviews/id=595068606/sortBy=mostRecent/page=1/json"
blog_feed = feedparser.parse(feed_url)
print(blog_feed)
