import copy
import dateparser
import datetime
from dateutil.relativedelta import relativedelta

def lexical_date_parser(date_to_check):
    """
    Analyzes a string representing a date and returns the normalized date and a datetime object.
    """
    if date_to_check == '':
        return '', None
    date_tmp = copy.copy(date_to_check)
    try:
        date_tmp = date_tmp[date_tmp.rfind('..') + 2:]
        datetime_tmp = dateparser.parse(date_tmp)
    except:
        return date_tmp, None
    if datetime_tmp:
        datetime_tmp = datetime_tmp.replace(tzinfo=None)
    return date_tmp.strip(), datetime_tmp

def define_date(date):
    """
    Returns a datetime object based on a string representing the date.
    Handles formats like "6 hours ago", "yesterday", "1 day ago", and explicit dates.
    """
    try:
        # Handle relative formats like "6 hours ago", "1 day ago", "yesterday"
        if 'ago' in date.lower():
            quantity = int(date.split()[0])
            if 'hour' in date.lower():
                return datetime.datetime.now() - relativedelta(hours=quantity)
            elif 'day' in date.lower():
                return datetime.datetime.now() - relativedelta(days=quantity)
            elif 'week' in date.lower():
                return datetime.datetime.now() - relativedelta(weeks=quantity)
            elif 'month' in date.lower():
                return datetime.datetime.now() - relativedelta(months=quantity)
            elif 'year' in date.lower():
                return datetime.datetime.now() - relativedelta(years=quantity)

        elif 'yesterday' in date.lower():
            return datetime.datetime.now() - relativedelta(days=1)

        else:
            return datetime.datetime.strptime(date, '%d/%m/%Y')

    except ValueError:
        return None
