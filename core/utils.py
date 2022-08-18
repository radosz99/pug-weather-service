from functools import wraps
from time import time, mktime
from datetime import datetime, timedelta
import json


def timer(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f"func: {f.__name__} args:[{args}, {kw}] took: {te-ts} sec")
        return result
    return wrap


def convert_unix_timestamp_to_date(unix_timestamp):
    try:
        date = int(unix_timestamp)
        return datetime.fromtimestamp(date).replace(second=0)
    except ValueError:
        raise ValueError(f"Cannot convert {unix_timestamp} to date, invalid format")


def convert_date_to_unix_timestamp(date):
    return mktime(date.timetuple())


def round_dates_from_request(start_date, end_date):
    start_date = start_date.replace(minute=0)
    if end_date.minute >= 30:
        end_date = end_date + timedelta(hours=1)
    end_date = end_date.replace(minute=0)
    return start_date, end_date


def save_json_to_file(json_to_save, filename):
    json_object = json.dumps(json_to_save, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_object)


def load_json_from_file(filename):
    with open(filename, 'r') as openfile:
        json_object = json.load(openfile)
    return json_object


def unix_timestamp_to_date_string(timestamp):
    date = convert_unix_timestamp_to_date(timestamp)
    return date_to_string(date)


def date_to_string(date):
    return date.strftime("%m/%d/%Y, %H:%M")


def get_index_of_key_in_dictionary(dic, item):
    return list(dic.keys()).index(item)


def verify_index_in_dictionary(list_to_verify, index):
    try:
        _ = list(list_to_verify.items())[index]
    except IndexError:
        raise IndexError(f"Index {index} exceeded dictionary length")