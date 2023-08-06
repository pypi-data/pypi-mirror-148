""" Handles the time and date related operations

Functions:
    date_print_format(date): converts the date string into a particular format
    date_object(date): Given a date in string fomrat, returns a datetime object for date operations
"""

from datetime import datetime
import dateutil.parser


def date_print_format(date):
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


# def iso_date_format(date):
#     """ converts the date string into a particular format

#     example timestamp in such format:
#     Thu, 21 Apr 2022 09:25:02 +0000

#     Args:
#         date (str): URL of the news page

#     Retruns:
#         date (str): formatted date
#     """
#     format = "%Y%m%d"
#     date = dateutil.parser.isoparse(date)
#     # date = date.strftime(format)
#     # date = datetime.strptime(date, format)
#     date = date.replace(tzinfo= None)
#     return date

def date_object(date):
    """Given a date in string fomrat, returns a datetime object for date operations

    Args:
        date (str): date in string format

    Retruns:
        datetime.strptime(date, "%Y%m%d")(datetime): date object of the given string
    """

    # conver the string into a date object
    return datetime.strptime(date, "%Y%m%d")