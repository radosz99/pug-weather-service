from datetime import datetime
from cachetools import cached, TTLCache
from requests import get
import json

from core.utils import convert_unix_timestamp_to_date
import core.exceptions as exc
from .. import utils
from core.constants import CACHE_SIZE, CACHE_ALIVE_TIME, API_KEY, API_URL

cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_ALIVE_TIME)


def get_weather_for_localization_and_time(weather_request):
    # hourly_forecast = get_hourly_weather_for_localization(weather_request)
    # short_forecast = cut_forecast_to_given_hours(hourly_forecast, weather_request)
    # save_forecast_to_file(short_forecast)
    short_forecast = load_forecast_from_file()
    return short_forecast


def get_hourly_weather_for_localization(weather_request):
    hourly_forecast = get_weather_from_external_api(weather_request).json()['hourly']
    return get_hourly_forecast_with_changed_key_to_date(hourly_forecast)


@utils.timer
@cached(cache)
def get_weather_from_external_api(weather_request):
    return get(url=API_URL, params={'lat': weather_request.lat,
                                    'lon': weather_request.lon,
                                    'appid': API_KEY,
                                    'units': 'metric'
                                    })


def cut_forecast_to_given_hours(hourly_forecast, weather_request):
    start_date, hours = parse_dates_from_request(weather_request)
    try:
        start_index = utils.get_index_of_key_in_dictionary(hourly_forecast, start_date)
        end_index = start_index + hours + 1
        utils.verify_index_in_dictionary(hourly_forecast, end_index)
        return dict(list(hourly_forecast.items())[start_index: end_index])
    except ValueError:
        raise exc.NotEnoughData("Lack of data, start date is not in next 2 days range")
    except IndexError:
        raise exc.NotEnoughData("Lack of data, end date is not in next 2 days range")


def parse_dates_from_request(weather_request):
    start_date = convert_unix_timestamp_to_date(weather_request.start)
    end_date = convert_unix_timestamp_to_date(weather_request.end)
    validate_given_dates(start_date, end_date)
    start_date, end_date = utils.round_dates_from_request(start_date, end_date)
    return utils.date_to_string(start_date), get_time_difference_in_hours(start_date, end_date)


def validate_given_dates(start_date, end_date):
    if start_date > end_date:
        raise exc.StartDateHasToBeEarlierThenEndDate(f"Start date {start_date} is greater than end date {end_date}")
    if start_date < datetime.now():
        raise exc.DatesShouldNotBeFromPast(f"Start date {start_date} is from the past, "
                                           f"current time - {datetime.now()}")


def get_time_difference_in_hours(date_1, date_2):
    time_difference = date_2 - date_1
    return int(time_difference.total_seconds() / 3600)


def get_hourly_forecast_with_changed_key_to_date(hourly_forecast):
    return {utils.unix_timestamp_to_date_string(hour_forecast['dt']): hour_forecast for hour_forecast in hourly_forecast}


def save_forecast_to_file(forecast):
    utils.save_json_to_file(forecast, "forecast.json")


def load_forecast_from_file():
    return utils.load_json_from_file("forecast.json")
