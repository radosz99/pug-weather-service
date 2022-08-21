import unittest
from datetime import datetime, timedelta

from core.utils import convert_date_to_unix_timestamp
from core.dto import ForecastRequest
from core.services import weather_api_handler as weather_service
import core.exceptions as exc


class TestChartCreationMethods(unittest.TestCase):
    @staticmethod
    def get_current_date_with_shift(shift):
        date = datetime.now()
        date = date.replace(minute=0, second=0, microsecond=0)
        return convert_date_to_unix_timestamp(date + timedelta(hours=shift))

    def test_forecast_range(self):
        start = TestChartCreationMethods.get_current_date_with_shift(0)
        end = TestChartCreationMethods.get_current_date_with_shift(6)
        weather_request = ForecastRequest(lon=44.50, lat=15.04, start=start, end=end)
        forecast = weather_service.get_weather_for_localization_and_time(weather_request)
        # self.assertEqual(len(forecast), 5)
        # print(forecast)

    def test_5_hours_request(self):
        forecast = weather_service.get_every_3_hours_forecast_for_localization(15.04, 44.50)
        print(forecast)