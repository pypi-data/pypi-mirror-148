""" Handles the parsing and printing the feed of RSS URL

This module provided the RSS URL, reads it and parses its content
and prints the news feed. The option of printing the feed in the
json format is also implemented.

Attributes:
    verision (int): version of the current release

Functions:
    get_encoding(soup): Checks the encoding of the html file of
                        the news page
"""

try:
    import argparse
    import xml.etree.ElementTree as ET
    import requests
    import json
    import logging
    from bs4 import BeautifulSoup
    import re
    from datetime import datetime
    from datetime import timedelta
    import dateutil.parser
    import textwrap

except ImportError:
    print('Error: Modules missing!')

# version of the current release
def main():
    version = 1.0

    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("--version", action="store_true", help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided", type=int)
    parser.add_argument("source", default="empty", nargs='?', help="RSS URL")
    args = parser.parse_args()


    # cheking in the verbose flag is set to TRUE
    if(args.verbose):
        logging_level = logging.INFO
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        logging.info("Verbose is set to ON!")
    else:
        # if the verbose flag is not set, then no logging message
        # should be printed, setting the logging level to one more
        # than the highest level will do the job
        logging_level = logging.CRITICAL + 1

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)


    if(args.version):
        print(f"version: {version}")
        logging.info("Version printed, exiting the program.")
        # if the version flag is set, the only required performance of
        # the app is to show the version and exit, hence:
        exit()


    # if the RSS URL is provided by the user, following must be done
    if(args.source != "empty"):
        # requesting and downloading the .XML file from the provided source
        # in the rss.xml file
        URL = args.source

        try:
            logging.info("Requesting the URL webpage")
            response = requests.get(URL)
        except requests.exceptions.RequestException:
            logging.error("Fetching was unsuccessful.")
            raise SystemExit("Error: Please insert the RSS URL again.")
        else:
            logging.info("Webpage retrieved successfully!")

        with open('rss.xml', 'wb') as file:
            file.write(response.content)

        # json news id and dictionary:
        news_id = 0
        json_dit = {}

        # Parses the XML into element tree
        # and extracts the root of the tree
        try:
            tree = ET.parse('rss.xml')
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

        # defining and initializing variables

        # limit variable: if the user does not provide a value for it
        # or the value is larger than feed size then user gets all available news feeds
        if args.limit is None:
            limit = len(items)
        else:
            limit = min(len(items), args.limit)

        # The feed title
        try:
            feed = root.find("channel").find("title").text
        except AttributeError:
            logging.debug("Couldn't find channel tag!")
            logging.error("RSS  info is not in proper shape!")
            raise SystemExit("Error: Please insert the RSS URL again.")

        # iterator to traverse the news items
        element_iterator = iter(items)

        # run_once variable is for logging the info that the feed is
        # being printed
        # the iteration is performed equal to the limit that is assigned above
        run_once = 0
        for count in range(limit):

            # for each news item, title, publication date, news link and
            # image link(if exists) and content is extracted
            element = next(element_iterator)

            def get_encoding(soup):
                """ Checks the encoding of the html file of the news page

                Args:
                    soup (beautifulsoup object): html parsed object with BeautifulSoup
                                                 function of bs4 library

                Retruns:
                    encod (str): the encoding extracted from the html
                """

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


            def date_format(date):
                """ converts the date string into a particular format

                example timestamp in such format:
                Thu, 21 Apr 2022 09:25:02 +0000

                Args:
                    date (str): URL of the news page

                Retruns:
                    date (str): formatted date
                """

                format = "%a, %d %b %Y %H:%M:%S %z"
                # RSS files dates are in iso format, to parse them:
                date = dateutil.parser.isoparse(date)
                date = date.strftime(format)
                return date

            # for each news item, extracting info and save them in a temporary dictionary to add then
            # to the feeds dictionary
            try:
                news_URL = element.find("link").text

                try:
                    date = element.find("pubDate").text
                    date = date_format(date)
                except ValueError:
                    date = date = element.find("pubDate").text
                
                dic_temp = {"title": element.find("title").text, "date": date,
                            "link": news_URL, "content": get_content(news_URL)}
            except AttributeError:
                logging.debug("Tag names were not found!")
                logging.error("RSS  info is not in proper shape!")
                raise SystemExit("Error: Please insert the RSS URL again.")
            except requests.exceptions.RequestException:
                logging.error("Fetching was unsuccessful. Content of the feed is not printed for this news.")


            # assuming initially that an image is available for each item, and fetching its link
            no_image = False
            try:
                dic_temp["image link"] = element.find('{http://search.yahoo.com/mrss/}content').get("url")
            except AttributeError:
                no_image = True

            if not args.json:
                if run_once == 0:
                    logging.info("Printing the RSS feed")
                    run_once += 1

                def wrap_text(text):
                    """ makes sure the line lengths are no more than 120 for the input


                    Args:
                        text (str): text to be formated in the lines of length 120

                    Retruns:
                        (str): formatted text
                    """
                    return '\n'.join(textwrap.wrap(text, 120))


                print("------------------------------------------------------------------------------------")
                print(f"Title: {wrap_text(dic_temp.get('title'))}")
                print(f"Date: {wrap_text(dic_temp.get('date'))}")
                print(f"Link: {wrap_text(dic_temp.get('link'))}\n")
                print(f"[image: {wrap_text(dic_temp.get('title'))}][2]\n{wrap_text(dic_temp.get('content'))}[1]\n\n")
                print(f"[1]: {wrap_text(dic_temp.get('link'))} (link)")

                if not no_image:
                    print(f"[2]: {wrap_text(dic_temp.get('image link'))} (image)\n\n")

            else:
                news_id += 1
                json_dit["News Number " + str(news_id)] = dic_temp


    if args.json:
        # Approach number 1
        # manually prining the feeds dictionary in json format
        logging.info("Printing the feed in json\n")

        def printJsonFromat(dictionary):
            """ Prints the content of the feeds dictionary in json format

            Args:
                dictionary: a dictionary of RSS items including title, date, news content...

            Retruns:
                None
            """

            print("{")
            for item in dictionary.keys():
                print(f'\n\t"{item}": {{')
                for item_item in dictionary[item].keys():
                    if (item_item == "content"):
                        content = '\n\t\t           '.join(textwrap.wrap(dictionary[item].get(item_item), 64))
                        print(f'\t\t"{item_item}": "{content}"')
                    elif (item_item == "image link"):
                        img_link = '\n\t\t              '.join(textwrap.wrap(dictionary[item].get(item_item), 64))
                        print(f'\t\t"{item_item}": "{img_link}"')
                    elif (item_item == "link"):
                        link = '\n\t\t        '.join(textwrap.wrap(dictionary[item].get(item_item), 64))
                        print(f'\t\t"{item_item}": "{link}"')
                    else:
                        print(f'\t\t"{item_item}": "{dictionary[item].get(item_item)}"')

                print("\t},")
            print("}")

        printJsonFromat(json_dit)

        # Approach number 2

        # out_file = open("test2.json", "w")
        # json.dump(json_dit, out_file, indent=4)
        # out_file.close()

        # myfile = open("test2.json")
        # txt = myfile.read()
        # print(txt)
        # myfile.close()

        # import os
        # os.remove("test2.json")


if __name__ == "__main__":
    main()