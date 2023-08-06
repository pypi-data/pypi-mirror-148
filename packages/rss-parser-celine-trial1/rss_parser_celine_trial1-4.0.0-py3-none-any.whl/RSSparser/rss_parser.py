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
# import argparse
# from prepare_data import show_feeds, set_verbose_prep
# from print_news import set_verbose_print
# import logging
# from cache_news import show_chache_bydate, set_verbose_cache



try:
    import argparse
    from prepare_data import show_feeds, set_verbose_prep
    from print_news import set_verbose_print
    import logging
    from cache_news import show_chache_bydate, set_verbose_cache, clear_cache, retrieve_by_number
    from RSSItems import RSSItems
    from convert_format import convert_html
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
    parser.add_argument("--date", help="Show cached news published after date")
    parser.add_argument("--clear",action="store_true", help="Clears cache.")
    parser.add_argument("--to-html", help="Converts and stores in HTML at the user-provided path.")
    parser.add_argument("--to-pdf", help="Converts and stores in PDF at the user-provided path.")
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

    # based on the set/unset verbose flag, set the logging level for other
    # moodles too
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)
    set_verbose_prep(logging_level)
    set_verbose_print(logging_level)
    set_verbose_cache(logging_level)

    # additional feature
    if (args.clear):
        clear_cache()

    # if the version flag is set, print the version and exit the program
    if(args.version):
        print(f"version: {version}")
        logging.info("Version printed, exiting the program.")
        # if the version flag is set, the only required performance of
        # the app is to show the version and exit, hence:
        exit()

    # if the date option is provided with an argument, only the
    # cached news will be shown
    if(args.date is not None):
        logging.info("Date is set!")
        if(args.to_html is not None):
            html = True
            show_chache_bydate(args.date, args.json, args.limit, args.to_html, html)
        else:
            html = False
            show_chache_bydate(args.date, args.json, args.limit, args.to_pdf, html)

        exit()

    # if the RSS URL is provided by the user, following must be done
    if(args.source != "empty"):
        RSS = RSSItems(args.source, args.json, args.limit)
        if(args.to_html is not None):
            convert_html(RSS.cache_list, args.to_html)
        if (args.to_pdf is not None):
            convert_html(RSS.cache_list, args.to_pdf)
        logging.info("program finished successfully")

    if(args.to_html is None and args.date):
        convert_html(retrieve_by_number(args.limit), args.to_html)




if __name__ == "__main__":
    main()