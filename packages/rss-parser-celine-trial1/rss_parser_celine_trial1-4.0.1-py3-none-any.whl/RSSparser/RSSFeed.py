import logging
import os

import requests

import fetch_data
from fetch_data import get_soup, extract_XML, extract_article
from fetch_data import  download_images as dl_img
from prepare_data import parse_XML, get_content
from date_time import date_print_format
from fetch_data import extract_links as dl_lnk


class RSSFeed:
    def __init__(self,item):
        self.element = item
        self.title = None
        self.date = None
        self.link = None
        self.content = None
        self.image_link = None
        self.cache_directory = self.create_cache_directory()
        self.dictionary = None
        self.cache_tuple = None
        self.get_feed_fields()
        self.soup = self.set_soup()
        self.article = extract_article(self.soup)
        self.create_dict()
        self.create_cache_tuple()
        self.download_article()
        self.download_images()
        self.download_links()



    def set_soup(self):
        return get_soup(self.link)

    def get_feed_fields(self):
        # for each news item, extracting info and save them in a temporary dictionary to add then
        # to the feeds dictionary
        try:
            self.title = self.element.find("title").text
            self.link = self.element.find("link").text
            self.content = get_content(self.link)

            try:
                date = self.element.find("pubDate").text
                self.date = date_print_format(date)
            except ValueError:
                self.date = self.element.find("pubDate").text

            # assuming initially that an image is available for each item, and fetching its link
            try:
                self.image_link = self.element.find('{http://search.yahoo.com/mrss/}content').get("url")
            except AttributeError:
                self.image_link = None

        except AttributeError:
            logging.debug("Tag names were not found!")
            logging.error("RSS  info is not in proper shape!")
            raise SystemExit("Error: Please insert the RSS URL again.")
        except requests.exceptions.RequestException:
            logging.error("Fetching was unsuccessful. Content of the feed is not printed for this news.")

    def create_cache_directory(self):
        cache_id_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'cached_news2', 'cache_id.txt'))
        with open(cache_id_path, 'r') as file:
            cache_id = file.read()
        cache_id = int(cache_id) + 1

        with open(cache_id_path, 'w') as file:
            file.write(str(cache_id))
        directory_name = "feed_" + str(cache_id)
        directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cached_news2', directory_name))
        if (not os.path.isdir(directory_path)):
           os.makedirs(directory_path)
        return os.path.abspath(os.path.join(os.path.dirname(__file__), 'cached_news2', directory_name))

    def create_dict(self):
        if self.image_link is not None:
            self.dictionary = {"title": self.title,
                               "date": self.date,
                               "link": self.link,
                               "content": self.content,
                               "image_link": self.image_link,
                               "cache_directory": self.cache_directory}
        else:
            self.dictionary = {"title": self.title,
                               "date": self.date,
                               "link": self.link,
                               "content": self.content,
                               "cache_directory": self.cache_directory}

    def create_cache_tuple(self):
        self.cache_tuple = (self.date, self.dictionary)

    def download_article(self):
        article_path = os.path.abspath(os.path.join(self.cache_directory, 'article.txt'))
        with open(article_path, 'w') as file:
            file.write(self.article)

    def download_images(self):
        dl_img(self.soup, self.cache_directory)

    def download_links(self):
        dl_lnk(self.soup, self.cache_directory)




# URL = "https://news.yahoo.com/rss/"
# p2 = RSSFeed(URL)

# print(p2.article)