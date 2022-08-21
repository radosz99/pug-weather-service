from datetime import datetime
from cachetools import cached, TTLCache
from requests import get

from .. import utils
from core.constants import CACHE_SIZE, CACHE_ALIVE_TIME, API_KEY, HOURLY_API_URL, THREE_HOURS_API_URL
import core.exceptions as exc
from ..dto import Forecast

cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_ALIVE_TIME)


def get_weather_for_localization_and_time(forecast_request):
    lat, lon = forecast_request.lat, forecast_request.lon
    start_date, end_date = utils.round_unix_timestamps_from_request(forecast_request.start, forecast_request.end)
    print(start_date)
    print(end_date)
    hourly_forecast = Forecast(get_hourly_forecast_for_localization(lat, lon), 1)
    every_3_hours_forecast = Forecast(get_every_3_hours_forecast_for_localization(lat, lon), 3)
    validate_dates_from_request(start_date, end_date, every_3_hours_forecast)

    if utils.get_time_difference_in_hours(start_date, end_date) <= 8 and end_date <= hourly_forecast.end:
        pass

    return hourly_forecast.forecast


def get_hourly_forecast_for_localization(lat, lon):
    forecast = get_2_days_forecast_from_api(lat, lon)
    hourly_forecast = forecast.json()['hourly']
    hourly_forecast = get_forecast_with_changed_key_to_unix_timestamp(hourly_forecast)
    return utils.retrieve_data_from_hourly_forecast(hourly_forecast)


def get_every_3_hours_forecast_for_localization(lat, lon):
    forecast = get_5_days_forecast_from_api(lat, lon)
    every_3_hours_forecast = forecast.json()['list']
    every_3_hours_forecast = get_forecast_with_changed_key_to_unix_timestamp(every_3_hours_forecast)
    return utils.retrieve_data_from_every_three_hours_forecast(every_3_hours_forecast)


def get_2_days_forecast_from_api(lat, lon):
    return get_request(HOURLY_API_URL, lat, lon)


def get_5_days_forecast_from_api(lat, lon):
    return get_request(THREE_HOURS_API_URL, lat, lon)



@utils.timer
@cached(cache)
def get_request(url, lat, lon):
    return get(url=url, params={'lat': lat,
                                'lon': lon,
                                'appid': API_KEY,
                                'units': 'metric'
                                })


def validate_dates_from_request(start_date, end_date, every_3_hours_forecast):
    now = datetime.now()
    if start_date > end_date:
        raise exc.StartDateHasToBeEarlierThenEndDate(f"Start date {start_date} is greater than end date {end_date}")
    elif start_date > every_3_hours_forecast.end:
        raise exc.NotEnoughData(f"Start date {start_date} is too late and has exceeded forecast maximum range - "
                                f"{every_3_hours_forecast.end}")
    elif end_date < now:
        raise exc.NotEnoughData(f"End date {end_date} is too early, before current time which is {now}")


def get_forecast_with_changed_key_to_unix_timestamp(forecast):
    return {forecast['dt']: forecast for forecast in forecast}


def save_forecast_to_file(forecast):
    utils.save_json_to_file(forecast, "forecast.json")


def load_forecast_from_file():
    return utils.load_json_from_file("forecast.json")
