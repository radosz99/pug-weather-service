import requests
from cachetools import cached, TTLCache

from ..utils import timer

cache = TTLCache(maxsize=10000, ttl=7200)
api_url = "https://api.openweathermap.org/data/3.0/onecall?"


def get_weather_for_localization(latitude, longitude, api_key):
    response = get_hourly_weather_for_localization(latitude, longitude, api_key)
    return response


def get_hourly_weather_for_localization(latitude, longitude, api_key):
    return get_weather_from_external_api(latitude, longitude, api_key).json()['hourly']


@timer
@cached(cache)
def get_weather_from_external_api(latitude, longitude, api_key):
    return requests.get(url=api_url, params={'lat': latitude, "lon": longitude, "appid": api_key})
