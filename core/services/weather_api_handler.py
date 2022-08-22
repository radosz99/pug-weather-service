from datetime import datetime
from cachetools import cached, TTLCache
from requests import get
import logging

from .. import utils
from core.constants import CACHE_SIZE, CACHE_ALIVE_TIME, API_KEY, HOURLY_API_URL, THREE_HOURS_API_URL
import core.exceptions as exc
from ..dto import Forecast


cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_ALIVE_TIME)


def get_weather_for_localization_and_time(forecast_request):
    lat, lon = forecast_request.lat, forecast_request.lon
    start, end = utils.round_unix_timestamps_from_request(forecast_request.start, forecast_request.end)
    logging.info(f"Looking for forecast withing the range {start} - {end} for latitude = {lat}, longitude = {lon}")

    hourly_forecast = Forecast(get_hourly_forecast_for_localization(lat, lon), 1)
    every_3_hours_forecast = Forecast(get_every_3_hours_forecast_for_localization(lat, lon), 3)

    validate_dates_from_request(start, end, every_3_hours_forecast.end)

    forecast = hourly_forecast if check_if_apply_for_hourly(start, end, hourly_forecast) else every_3_hours_forecast
    cut_forecast_to_specific_range(start, end, forecast)
    return forecast


def check_if_apply_for_hourly(start_date, end_date, hourly_forecast):
    from core.constants import MAX_HOURLY_RANGE
    if utils.get_time_difference_in_hours(start_date, end_date) <= MAX_HOURLY_RANGE and end_date <= hourly_forecast.end:
        return True
    else:
        return False


def get_hourly_forecast_for_localization(lat, lon):
    forecast = get_2_days_forecast_from_api(lat, lon)
    hourly_forecast = forecast.json()['hourly']
    return utils.retrieve_data_from_hourly_forecast(hourly_forecast)


def get_every_3_hours_forecast_for_localization(lat, lon):
    forecast = get_5_days_forecast_from_api(lat, lon)
    every_3_hours_forecast = forecast.json()['list']
    return utils.retrieve_data_from_every_three_hours_forecast(every_3_hours_forecast)


def get_2_days_forecast_from_api(lat, lon):
    return get_request(HOURLY_API_URL, lat, lon)


def get_5_days_forecast_from_api(lat, lon):
    return get_request(THREE_HOURS_API_URL, lat, lon)


def cut_forecast_to_specific_range(start, end, forecast):
    end_index = len(forecast.single_forecasts) - 1 if forecast.end <= end else find_index_of_last_suitable_single_forecast(end, forecast)
    start_index = 0 if forecast.start >= start else find_index_of_first_suitable_single_forecast(start, forecast)
    logging.info(f"Forecast = {forecast} cut withing the range - {start} to {end} from index {start_index} "
                 f"({forecast.single_forecasts[start_index].unix_timestamp}) to index {end_index} "
                 f"({forecast.single_forecasts[end_index].unix_timestamp})")
    forecast.single_forecasts = forecast.single_forecasts[start_index:end_index + 1]
    forecast.start = forecast.single_forecasts[0].unix_timestamp
    forecast.end = forecast.single_forecasts[-1].unix_timestamp


def find_index_of_last_suitable_single_forecast(date, forecast):
    difference_in_hours = utils.get_time_difference_in_hours(date, forecast.start)
    quotient, remainder = int(difference_in_hours / forecast.step_in_hours), difference_in_hours % forecast.step_in_hours
    single_forecast_index = quotient + 1 if remainder != 0 else quotient
    logging.info(f"Difference between date and start of forecast = {difference_in_hours}, next single forecast index = {single_forecast_index}")
    return single_forecast_index


def find_index_of_first_suitable_single_forecast(date, forecast):
    difference_in_hours = utils.get_time_difference_in_hours(date, forecast.start)
    single_forecast_index = int(difference_in_hours / forecast.step_in_hours)
    logging.info(f"Difference between date and start of forecast = {difference_in_hours}, previous single forecast index = {single_forecast_index}")
    return single_forecast_index


@utils.timer
@cached(cache)
def get_request(url, lat, lon):
    return get(url=url, params={'lat': lat,
                                'lon': lon,
                                'appid': API_KEY,
                                'units': 'metric'
                                })


def validate_dates_from_request(start_date, end_date, last_forecast_date):
    now = datetime.now()
    if start_date > end_date:
        raise exc.StartDateHasToBeEarlierThenEndDate(f"Start date {start_date} is greater than end date {end_date}")
    elif start_date > last_forecast_date:
        raise exc.NotEnoughData(f"Start date {start_date} is too late and has exceeded forecast maximum range - "
                                f"{last_forecast_date}")
    elif end_date < now:
        raise exc.NotEnoughData(f"End date {end_date} is too early, before current time which is {now}")


def save_forecast_to_file(forecast):
    utils.save_json_to_file(forecast, "forecast.json")


def load_forecast_from_file():
    return utils.load_json_from_file("forecast.json")
