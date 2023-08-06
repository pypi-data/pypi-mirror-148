""" Caches the news and retrieves the cached news

This modules implements functions to cache the previously
seen feeds, and retrieve them when user enters the date
argument

Functions:
    get_encoding(soup): Checks the encoding of the html file of
                        the news page

    cache_news(news_list): saves the news list in a file
    retrieve_cache(): reades the file that contents the chached news
    find_item(selected_date, json, limit): based on the given date,
                selects the news that are published after the date
                and picks the number of news specified by the limit
                argument (if the argument is not present, all chached
                news) also prints the feed if it is in the regular format
    clear_cache(): deletes the file of the cached news
    show_chache_bydate(selected_date, json, limit): prints
                the selected number of cached news feed with
                calling find_item function

"""
import pickle
from RSSparser.date_time import  date_object
from datetime import datetime
from RSSparser.print_news import print_json_format, print_regular_format
import logging
import os
import shutil
import dateutil.parser
from RSSparser.convert_format import convert_html, convert_pdf


# try:
#     import pickle
#     from date_time import iso_date_format, date_object
#     from datetime import datetime
#     from print_news import print_json_format, print_regular_format
#     import os
#     import logging
# except ImportError:
#     raise SystemExit('Error: Modules missing!')


def set_verbose_cache(logging_level):
    """ set the configuration for loggings

    Args:
        logging_level (str): the level of loggings user is willing to be shown

    Retruns:
        None
    """
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)



# def cache_news(news_list):
#     """ caches the news feeds stored in a list

#     Args:
#         news_list (list): a list of feed dictionaries

#     Retruns:
#         None
#     """

#     # if already a file exists with cached news, read,
#     #otherwise create a new file and write into it
#     try:
#         a_file = open("cached_news.pkl", "rb")
#         saved_news = pickle.load(a_file)
#         cache_list = [*news_list, *saved_news]
#         cache_file = open("cached_news.pkl", "wb")
#         # pickle module used for serializing the data
#         pickle.dump(cache_list, cache_file)
#         cache_file.close()

#     except FileNotFoundError:
#         logging.info("Appending the feeds cache to existing cached news")
#         a_file = open("cached_news.pkl", "wb")
#         pickle.dump(news_list, a_file)
#         a_file.close()

def cache_news(news_list, cache_directory):
    cache_directory = cache_directory
    # cache_directory = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'cached_news2'))
    cache = os.path.join(cache_directory, "cached_news.pkl")
    # try:
    #     try:
    #         a_file = open(cache, "rb")
    #     except FileNotFoundError:
    #         logging.info("creating the cache directory.")
    #         os.makedirs(cache_directory, exist_ok=False)
    #         a_file = open(cache, "rb")
    #
    #     saved_news = pickle.load(a_file)
    #     cache_list = [*news_list, *saved_news]
    #     cache_file = open(cache, "wb")
    #     # pickle module used for serializing the data
    #     logging.info("Appending the feeds cache to existing cached news")
    #     pickle.dump(cache_list, cache_file)
    #     cache_file.close()
    #
    # except FileNotFoundError:
    #     logging.info("Creating a new cache file.")
    #     a_file = open(cache, "wb")
    #     pickle.dump(cache, a_file)
    #     a_file.close()


    if(os.path.isdir(cache_directory)):
        if(os.path.isfile(cache)):
            a_file = open(cache, "rb")
            saved_news = pickle.load(a_file)
            cache_list = [*news_list, *saved_news]
            cache_file = open(cache, "wb")
            logging.info("Appending the feeds cache to existing cached news")
            pickle.dump(cache_list, cache_file)
            cache_file.close()
        else:
            a_file = open(cache, "wb")
            pickle.dump(news_list, a_file)
            a_file.close()

    else:
        logging.info("Creating a new cache file.")
        os.makedirs(cache_directory)
        a_file = open(cache, "wb")
        pickle.dump(news_list, a_file)
        a_file.close()


# os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'cache', cached_news.pkl))


def retrieve_cache():
    """ retrievs the cached news in a file

    Args:
        None

    Retruns:
        pickle.load(a_file) (list): the loaded list of feeds
    """
    logging.info("retrieving cache")
    cache = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'cached_news2', "cached_news.pkl"))
    try:
        a_file = open(cache, "rb")
        return pickle.load(a_file)
    except FileNotFoundError:
        logging.warning("There is no cached news feed!")
        raise SystemExit()


def find_item(selected_date, json, limit, date):
    """ Selects the news after the specified date

    This function selects the news from the retirieved list that satisfy
    the date condition, and if the selected mode is not json, then prints it
    in the regular format

    Args:
        selected_date(str): date chosen by user for the news to be shown after that
        json: printing mode specified by the user
        limit: number of cached news specified by the user to be shown

    Retruns:
        selected_news (dict): a dictionary of cached news created based on the number limit
                              and date
    """

    news_id = 0
    # the news items from the cached news is stored in the selected news
    # dictionary after picked by the specified date by the user
    logging.info("Finding news.")
    selected_news = {}
    cached_news = retrieve_cache()

    # setting the number of cached news to be printed based on the limit input
    if limit is None:
        limit = len(cached_news)
    else:
        limit = min(limit, len(cached_news))


    selected_date = date_object(selected_date)
    element_iterator = iter(cached_news)
    news_list = []
    for count in range(limit):
        item = next(element_iterator)
        # news_date = item[0]
        # converting to datetime object for comparison
        # news_date = datetime.strptime(item[0], "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo= None)
        news_date = dateutil.parser.parse(item[0]).replace(tzinfo= None)
        if news_date > selected_date:
            # if(json):
            #     news_id += 1
            #     selected_news["News Number " + str(news_id)] = item[1]
            news_id += 1
            selected_news["News Number " + str(news_id)] = item[1]
            news_list.append(item)

            # if the format is not set to json, each selected feed will be
            # printed after be chosen
            if(not json and (date is None)): print_regular_format(item[1])
    return selected_news, news_list

def clear_cache():
    """ deletes the cache file

    Args:
        None

    Retruns:
        None
    """
    # cache diretory path
    cache = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'cached_news'))
    # clear cache by deleting the file


    try:
        shutil.rmtree(cache)
        logging.info("cache cleared!")
    except:
        logging.error("No cached news exist!")
        raise SystemExit()

def show_chache_bydate(selected_date, json, limit, convert, html):
    """ prints the cached news based on the number limit and date

    with the specified printing format and numbe of news and selected date
    prints the cached news feed

    Args:
        selected_date(str): date chosen by user for the news to be shown after that
        json: printing mode specified by the user
        limit: number of cached news specified by the user to be shown

    Retruns:
        None
    """
    selected_news, list = find_item(selected_date, json, limit, convert)
    if(convert is None):
        if(json):
            print_json_format(selected_news)
        else:
            for item in selected_news:
                print_regular_format(item)
    else:
        if(html):
            convert_html(list, convert)
            if (json):
                print_json_format(selected_news)
        else:
            convert_pdf(list, convert)
            if (json):
                print_json_format(selected_news)



def retrieve_by_number(limit):
    cached_list = retrieve_cache()
    if(limit is not None):
        limit = min(len(cached_list), limit)
    else:
        limit = len(cached_list)
    cached_list = iter(cached_list)
    numbered_cache = []
    for number in range(limit):
        numbered_cache.append(next(cached_list))
    return cached_list
