from functools import wraps
from time import time, mktime
from datetime import datetime, timedelta
import json

from .dto import HourForecast


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
    return int(mktime(date.timetuple()))


def round_unix_timestamps_from_request(start_date, end_date):
    start_date = convert_unix_timestamp_to_date(start_date)
    end_date = convert_unix_timestamp_to_date(end_date)
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


def convert_unix_timestamp_to_date_string(timestamp):
    date = convert_unix_timestamp_to_date(timestamp)
    return convert_date_to_string(date)


def convert_date_to_string(date):
    return date.strftime("%m/%d/%Y, %H:%M")


def convert_string_to_date(str_date):
    return datetime.strptime(str_date, "%m/%d/%Y, %H:%M")


def get_index_of_key_in_dictionary(dic, item):
    return list(dic.keys()).index(item)


def verify_index_in_dictionary(list_to_verify, index):
    try:
        _ = list(list_to_verify.items())[index]
    except IndexError:
        raise IndexError(f"Index {index} exceeded dictionary length")


def get_time_difference_in_hours(date_1, date_2):
    time_difference = date_2 - date_1
    return int(time_difference.total_seconds() / 3600)


def convert_string_to_json(str_json):
    str_json = str_json.replace("\'", "\"")
    return json.loads(str_json)


def retrieve_data_from_hourly_forecast(dict_forecast):
    forecast = {}
    for key, value in dict_forecast.items():
        temp = value.get('temp', 0)
        clouds = value.get('clouds', 0)
        wind_speed = value.get('wind_speed', 0)
        try:
            rain = value['rain']['1h']
        except KeyError:
            rain = 0
        weather = str(value['weather'][0])
        weather = convert_string_to_json(weather)
        desc_1 = weather['main']
        desc_2 = weather['description']
        icon = weather['icon']
        uvi = value.get('uvi', 0)
        humidity = value.get('humidity', 0)
        try:
            snow = value['snow']['1h']
        except KeyError:
            snow = 0
        pop = value.get('pop', 0)
        unix_timestamp = value.get('dt', 0)
        date = convert_unix_timestamp_to_date_string(unix_timestamp)
        hour_forecast = HourForecast(temp, clouds, wind_speed, rain, desc_1, desc_2, uvi, humidity, icon, snow, pop, date)
        forecast[unix_timestamp] = hour_forecast.__dict__
    return forecast


def retrieve_data_from_every_three_hours_forecast(dict_forecast):
    forecast = {}
    for key, value in dict_forecast.items():
        main = value['main']
        temp = main.get('temp', 0)
        clouds = value['clouds']['all']
        wind_speed = value['wind']['speed']
        try:
            rain = value['rain']['3h']
        except KeyError:
            rain = 0
        weather = str(value['weather'][0])
        weather = convert_string_to_json(weather)
        desc_1 = weather['main']
        desc_2 = weather['description']
        icon = weather['icon']
        uvi = value.get('uvi', 0)
        humidity = main .get('humidity', 0)
        try:
            snow = value['snow']['3h']
        except KeyError:
            snow = 0
        pop = value.get('pop', 0)
        unix_timestamp = value.get('dt', 0)
        date = convert_unix_timestamp_to_date_string(unix_timestamp)
        hour_forecast = HourForecast(temp, clouds, wind_speed, rain, desc_1, desc_2, uvi, humidity, icon, snow, pop, date)
        forecast[unix_timestamp] = hour_forecast.__dict__
    return forecast


