import os
from bs4.element import NavigableString
import requests
from bs4 import BeautifulSoup
import shutil
import logging
import json

from RSSparser.prepare_data import get_encoding
def get_soup(news_link):
    """ Extracts the content summary of the news page

    Args:
        news_link (str): URL of the news page

    Retruns:
        content.attrs.get("content") (str): the summary of the content
                                            of the news page
    """

    try:
        page = requests.get(news_link)
        text = page.content
        # parsing the content of the webpage into
        # html string
        soup = BeautifulSoup(text, "html.parser")
        # parsing the content of the webpage, this time with the
        # recognized encoding
        soup = BeautifulSoup(text, "html.parser", from_encoding=get_encoding(soup))
        soup.prettify()
        return soup

    except ValueError:
        # if the get_encoding function is unable to provide
        # correct encoding, continue with the defaults of
        # BeautifulSoup function
        page = requests.get(news_link)
        text = page.content
        soup = BeautifulSoup(text, "html.parser")
        return soup


def extract_XML(URL):
    """Given the RSS url, fetches the XML content

    The content is then stored in a file names rss.xml

    Args:
        URL (str): RSS URL provided by the user

    Retruns:
        None
    """
    try:
        logging.info("Requesting the URL webpage")
        response = requests.get(URL)
    except requests.exceptions.RequestException:
        logging.error("Fetching was unsuccessful.")
        raise SystemExit("Error: Please insert the RSS URL again or Check internet connectivity.")
    else:
        logging.info("Webpage retrieved successfully!")

    xml = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'rss.xml'))
    with open(xml, 'wb') as file:
        file.write(response.content)

def extract_images(soup):
    images = []
    string_type = NavigableString
    for image in soup.find("article").find_all("img"):
        images.append(image.attrs.get("src"))
    return images


def download_images(soup, feed_cache_directory):
    images_URL_list = extract_images(soup)
    image_id = 0
    images_dir = os.path.abspath(os.path.join(feed_cache_directory, 'images'))
    for url in images_URL_list:
        if (not os.path.isdir(images_dir)):
            os.makedirs(images_dir)
        if(url is not None):
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                image_id += 1
                image_name = "image_" + str(image_id) + ".jpg"
                with open(os.path.abspath(os.path.join(images_dir, image_name)), 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)


def extract_links(soup, feed_cache_directory):
    links = []
    for item in soup.find("article").find_all("a"):
        link = item.attrs.get("href")
        if(link.startswith("https") or link.startswith("http")):
            links.append(link)

    with open(os.path.abspath(os.path.join(feed_cache_directory, 'links.txt')), 'w') as f:
        f.write(json.dumps(links))




def extract_article(soup):
    article = ""
    string_type = NavigableString
    for paragraph in soup.find("article").find_all("p"):
        if(isinstance(paragraph.next_element, string_type)):
            article = article + "\n" + paragraph.next_element

    return article

def get_news(dic_temp):
    article = extract_article()