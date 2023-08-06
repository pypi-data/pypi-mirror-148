""" Prepare the data of the news to be printed as the RSS feeds

This modules fetches the XML content of the URL provided by the user,
parses it into XML tree elements, extracts the required data from
this tree structre and prints it in the rquired format provided
by the user



Functions:
    set_verbose_prep(logging_level): set the configuration for loggings
    get_encoding(soup): Checks the encoding of the html file of the news page
    get_content(news_link): Extracts the content summary of the news page
    extract_XML(URL): Given the RSS url, fetches the XML content
    parse_XML(): Parses the XML file
    print_RSS_title(root): Prints the title of the RSS file before the feed
    feeds_number(args_limit, length): Determines number of feeds to be printed
    make_news_dictionary(items, json, root, limit): Parses the XML element tree into a dictionary of feeds
    show_feeds(URL, json, limit): Handles the getching, parsing the XML content and printing the feed
"""
# import xml.etree.ElementTree as ET
# import requests
# import json
# import logging
# from bs4 import BeautifulSoup
# import re
# from datetime import datetime
# from date_time import date_print_format
# from print_news import print_regular_format, print_json_format
# from cache_news import cache_news

import os
try:
    import xml.etree.ElementTree as ET
    import requests
    import json
    import logging
    from bs4 import BeautifulSoup
    import re
    from datetime import datetime
    import os
except ImportError:
    raise SystemExit('Error: Modules missing!')

json_dit = {}
chache_list = []


def set_verbose_prep(logging_level):
    """ set the configuration for loggings

    Args:
        logging_level (str): the level of loggings user is willing to be shown

    Retruns:
        None
    """
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)


def get_encoding(soup):
    """ Checks the encoding of the html file of the news page

    Args:
        soup (beautifulsoup object): html parsed object with BeautifulSoup
                                     function of bs4 library

    Retruns:
        encod (str): the encoding extracted from the html
    """
    # getting the enocing from the soup object (html parsed object)
    if soup and soup.meta:
        encod = soup.meta.get('charset')
        if encod is None:
            encod = soup.meta.get('content-type')
            if encod is None:
                content = soup.meta.get('content')
                match = re.search('charset=(.*)', content)
                if match:
                    encod = match.group(1)
                else:
                    raise ValueError('unable to find encoding')
    else:
        raise ValueError('unable to find encoding')
    return encod


def get_content(news_link):
    """ Extracts the content summary of the news page

    Args:
        news_link (str): URL of the news page

    Retruns:
        content.attrs.get("content") (str): the summary of the content
                                            of the news page
    """

    try:
        logging.info("Getting the content of the news feed.")
        page = requests.get(news_link)
        text = page.content
        # parsing the content of the webpage into
        # html string
        soup = BeautifulSoup(text, "html.parser")
        # parsing the content of the webpage, this time with the
        # recognized encoding
        soup = BeautifulSoup(text, "html.parser", from_encoding=get_encoding(soup))
        content = soup.find("meta", attrs={"name": "description"})
        return content.attrs.get("content")

    except ValueError:
        # if the get_encoding function is unable to provide
        # correct encoding, continue with the defaults of
        # BeautifulSoup function
        logging.warning("The encoding might not be correct!")
        page = requests.get(news_link)
        text = page.content
        soup = BeautifulSoup(text, "html.parser")
        content = soup.find("meta", attrs={"name": "description"})
        return content.attrs.get("content")


# def extract_XML(URL):
#     """Given the RSS url, fetches the XML content
#
#     The content is then stored in a file names rss.xml
#
#     Args:
#         URL (str): RSS URL provided by the user
#
#     Retruns:
#         None
#     """
#     try:
#         logging.info("Requesting the URL webpage")
#         response = requests.get(URL)
#     except requests.exceptions.RequestException:
#         logging.error("Fetching was unsuccessful.")
#         raise SystemExit("Error: Please insert the RSS URL again or Check internet connectivity.")
#     else:
#         logging.info("Webpage retrieved successfully!")
#
#     xml = os.path.abspath(os.path.join(os.path.dirname(__file__), 'rss.xml'))
#     with open(xml, 'wb') as file:
#         file.write(response.content)


def parse_XML():
    """Parses the xml file

    Reads the rss.xml file and parses it into XML elements in tree structure

    Args:
        None
    Retruns:
        root: root node of the XML tree
        items: feed nodes of the XML tree
    """

    # Parses the XML into element tree
    # and extracts the root of the tree
    try:
        xml = os.path.abspath(os.path.join(os.path.dirname(__file__), 'rss.xml'))
        tree = ET.parse(xml)
    except ET.ParseError:
        logging.error("Parsing was unsuccessful.")
        raise SystemExit("Error: Please insert the RSS URL again.")
    else:
        logging.info("RSS file Parsed successfully!")

    root = tree.getroot()

    # creating a list of all items(titles) in the RSS file
    # in the RSS file, the titles are wrapped in elements
    # with the tag: item
    try:
        items = root.find("channel").findall("item")
    except AttributeError:
        logging.debug("Couldn't find channel tag!")
        logging.error("RSS info is not in proper shape!")
        raise SystemExit("Error: Please insert the RSS URL again.")
    return root, items


def print_RSS_title(root):
    """Prints the title of the RSS file before the feed

    Args:
        root: root of the parsed XML tree

    Retruns:
        None
    """
    # The feed title
    try:
        feed = root.find("channel").find("title").text
        print(feed)
    except AttributeError:
        logging.debug("Couldn't find channel tag!")
        logging.error("RSS  info is not in proper shape!")
        raise SystemExit("Error: Please insert the RSS URL again.")


def feeds_number(args_limit, length):
    """Determines number of feeds to be printed

    Based on the limit input by the user, this number is calculated

    Args:
        args_limit (int): the number limit input by the user

    Retruns:
        limit: number of feeds to be printed
    """
    # limit variable: if the user does not provide a value for it
    # or the value is larger than feed size then user gets all available news feeds
    if args_limit is None:
        limit = length
    else:
        limit = min(length, args_limit)
    return limit


def make_news_dictionary(items, json, root, limit):
    """ Parses the XML element tree into a dictionary of feeds

    Takes the XML element tree and extract from it the required elements
    and stores the items for each feed in a dictionary and then all the feed
    dictionaries into one final dictionary.
    Also caching the read news is called from this function.

    Args:
        items: feed nodes of the XML tree
        json: printing mode specified by the user
        root: root node of the XML tree
        limit: number of cached news specified by the user to be shown

    Retruns:
        None
    """
    # iterator to traverse the news items
    element_iterator = iter(items)

    # run_once variable is for logging the info that the feed is
    # being printed
    # the iteration is performed equal to the limit that is assigned above
    run_once = 0
    news_id = 0
    for count in range(limit):

        # for each news item, title, publication date, news link and
        # image link(if exists) and content is extracted
        element = next(element_iterator)

        # for each news item, extracting info and save them in a temporary dictionary to add then
        # to the feeds dictionary
        try:
            news_URL = element.find("link").text

            try:
                date = element.find("pubDate").text
                date = date_print_format(date)
            except ValueError:
                date = element.find("pubDate").text

            dic_temp = {"title": element.find("title").text, "date": date,
                        "link": news_URL, "content": get_content(news_URL)}
        except AttributeError:
            logging.debug("Tag names were not found!")
            logging.error("RSS  info is not in proper shape!")
            raise SystemExit("Error: Please insert the RSS URL again.")
        except requests.exceptions.RequestException:
            logging.error("Fetching was unsuccessful. Content of the feed is not printed for this news.")

        # assuming initially that an image is available for each item, and fetching its link
        try:
            dic_temp["image link"] = element.find('{http://search.yahoo.com/mrss/}content').get("url")
        except AttributeError:
            dic_temp["image link"] = None

        chache_list.append((date, dic_temp))

        if json == False:
            if (run_once == 0):
                print_RSS_title(root)
                run_once += 1
            print_regular_format(dic_temp)
        else:
            news_id += 1
            json_dit["News Number " + str(news_id)] = dic_temp


def show_feeds(URL, json, limit):
    """Handles the getching, parsing the XML content and printing the feed

    Args:
        URL (str): RSS URL provided by the user
        root: root node of the XML tree
        limit: number of cached news specified by the user to be shown

    Retruns:
        date (str): formatted date
    """

    logging.info("retrieving XML file.")
    extract_XML(URL)
    logging.info("parsing XML file")
    root, items = parse_XML()
    limit = feeds_number(limit, len(items))
    logging.info("Extracting feed information.")
    make_news_dictionary(items, json, root, limit)
    logging.info("caching the news.")
    cache_news(chache_list)
    if json:
        print_RSS_title(root)
        print_json_format(json_dit)













