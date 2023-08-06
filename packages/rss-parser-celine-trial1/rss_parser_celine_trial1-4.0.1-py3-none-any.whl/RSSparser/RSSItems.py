import logging
import os

import requests
from fetch_data import get_soup, extract_XML, extract_article
from prepare_data import parse_XML, get_content
from RSSFeed import RSSFeed
from print_news import print_json_format, print_regular_format
from cache_news import cache_news as cache
from date_time import date_print_format


class RSSItems:
    cached_news_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cached_news2'))

    def __init__(self,rss_url, json, limit):
        self.title = None
        # self.date = None
        self.URL = rss_url
        self.json = json

        self.root = None
        self.items = None
        self.cache_list = []
        # self.dictionary = None

        extract_XML(rss_url)
        self.parse_XML()
        self.length = len(self.items)
        self.limit = self.feeds_number(limit)
        self.rss_items = []
        self.json_dictionary = {}
        # self.cached_news_directory()
        self.create_cache_directory()
        self.set_rss_elements()
        self.creat_json_dictionary()
        self.create_cache_list()
        self.cache_news()


    def parse_XML(self):
        self.root, self.items = parse_XML()
        self.length = len(self.items)

    def set_rss_elements(self):
        element_iterator = iter(self.items)
        # for count in range(self.limit):
        for count in range(self.limit):
            element = next(element_iterator)
            self.rss_items.append(RSSFeed(element))

    def feeds_number(self, limit):
        """Determines number of feeds to be printed

        Based on the limit input by the user, this number is calculated

        Args:
            args_limit (int): the number limit input by the user

        Retruns:
            limit: number of feeds to be printed
        """
        # limit variable: if the user does not provide a value for it
        # or the value is larger than feed size then user gets all available news feeds
        if limit is None:
            limit = self.length
        else:
            limit = min(self.length, limit)
        return limit

    def create_cache_directory(self):
        if not os.path.isdir(self.cached_news_directory):
            os.makedirs(self.cached_news_directory)
            cache_id = "0"
            cache_id_path =  os.path.abspath(os.path.join(self.cached_news_directory, "cache_id.txt"))
            with open(cache_id_path, 'w') as file:
                file.write(cache_id)

    def creat_json_dictionary(self):
        news_id = 0
        for items in self.rss_items:
            news_id += 1
            news_key = "News Number: " + str(news_id)
            self.json_dictionary[news_key] = items.dictionary


    def print_feed(self):
        if self.json:
            print_json_format(self.json_dictionary)
        else:
            for item in self.rss_items:
                print_regular_format(item.dictionary)

    def create_cache_list(self):
        for item in self.rss_items:
            self.cache_list.append(item.cache_tuple)

    def cache_news(self):
        cache(self.cache_list, self.cached_news_directory)



