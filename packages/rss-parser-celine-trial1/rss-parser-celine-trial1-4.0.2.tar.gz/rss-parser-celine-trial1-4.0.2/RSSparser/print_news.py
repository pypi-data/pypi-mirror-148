""" Handles the printing of the feeds

Functions:
    set_verbose_print(logging_level): set the configuration for loggings
    wrap_text(text): makes sure the line lengths are no more than 120 for the input
    print_json_format(dictionary): Prints the content of the feeds dictionary in json format
    print_regular_format(dic_temp): Prints the content of the feeds dictionary in regular format

"""
import logging
import textwrap

def set_verbose_print(logging_level):
    """ set the configuration for loggings

    Args:
        logging_level (str): the level of loggings user is willing to be shown

    Retruns:
        None
    """
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)

def wrap_text(text):
    """ makes sure the line lengths are no more than 120 for the input


    Args:
        text (str): text to be formated in the lines of length 120

    Retruns:
        (str): formatted text
    """
    return '\n'.join(textwrap.wrap(text, 120))


def print_json_format(dictionary):
    """ Prints the content of the feeds dictionary in json format

    Args:
    dictionary: a dictionary of RSS items including title, date, news content...

    Retruns:
    None
    """

    # Approach number 1
    # manually prining the feeds dictionary in json format
    logging.info("Printing the feed in json\n")
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


run_once = 0
def print_regular_format(dic_temp):
    """ Prints the content of the feeds dictionary in regular format

    Args:
    dictionary: a dictionary of RSS items including title, date, news content...

    Retruns:
    None
    """
    global run_once
    if run_once == 0:
        logging.info("Printing the RSS feed")
        run_once += 1


    print("------------------------------------------------------------------------------------")
    print(f"Title: {wrap_text(dic_temp.get('title'))}")
    print(f"Date: {wrap_text(dic_temp.get('date'))}")
    print(f"Link: {wrap_text(dic_temp.get('link'))}\n")
    print(f"[image: {wrap_text(dic_temp.get('title'))}][2]\n{wrap_text(dic_temp.get('content'))}[1]\n\n")
    print(f"[1]: {wrap_text(dic_temp.get('link'))} (link)")

    if dic_temp.get('image link') is not None:
        print(f"[2]: {wrap_text(dic_temp.get('image link'))} (image)\n\n")
