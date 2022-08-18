import unittest
from datetime import datetime, timedelta

from core.utils import convert_date_to_unix_timestamp
from core.dto import WeatherRequest
from core.services import weather_api_handler as weather_service
import core.exceptions as exc


@unittest.skip
class TestDatesMethods(unittest.TestCase):
    @staticmethod
    def get_weather_request(start, end):
        start = convert_date_to_unix_timestamp(start)
        end = convert_date_to_unix_timestamp(end)
        return WeatherRequest(lon=10, lat=10, start=start, end=end)

    def test_1(self):
        start = datetime(2022, 8, 19, 18, 30, 00)
        end = datetime(2022, 8, 19, 19, 00, 00)
        data = TestDatesMethods.get_weather_request(start, end)
        start_date, hours = weather_service.parse_dates_from_request(data)
        start_date = datetime.strptime(start_date, "%m/%d/%Y, %H:%M")
        self.assertEqual(start_date.hour, 18, "Incorrect start hour")
        self.assertEqual(start_date.minute, 0, "Incorrect start minutes")
        self.assertEqual(hours, 1, "Incorrect hours amount")

    def test_2(self):
        start = datetime(2022, 8, 19, 18, 30, 00)
        end = datetime(2022, 8, 19, 19, 30, 00)
        data = TestDatesMethods.get_weather_request(start, end)
        start_date, hours = weather_service.parse_dates_from_request(data)
        start_date = datetime.strptime(start_date, "%m/%d/%Y, %H:%M")
        self.assertEqual(start_date.hour, 18, "Incorrect start hour")
        self.assertEqual(start_date.minute, 0, "Incorrect start minutes")
        self.assertEqual(hours, 2, "Incorrect hours amount")

    def test_3(self):
        start = datetime(2022, 8, 19, 18, 30, 00)
        end = datetime(2022, 8, 19, 20, 0, 00)
        data = TestDatesMethods.get_weather_request(start, end)
        start_date, hours = weather_service.parse_dates_from_request(data)
        start_date = datetime.strptime(start_date, "%m/%d/%Y, %H:%M")
        self.assertEqual(start_date.hour, 18, "Incorrect start hour")
        self.assertEqual(start_date.minute, 0, "Incorrect start minutes")
        self.assertEqual(hours, 2, "Incorrect hours amount")

    def test_4(self):
        start = datetime(2022, 8, 19, 18, 0, 00)
        end = datetime(2022, 8, 19, 18, 30, 00)
        data = TestDatesMethods.get_weather_request(start, end)
        start_date, hours = weather_service.parse_dates_from_request(data)
        start_date = datetime.strptime(start_date, "%m/%d/%Y, %H:%M")
        self.assertEqual(start_date.hour, 18, "Incorrect start hour")
        self.assertEqual(start_date.minute, 0, "Incorrect start minutes")
        self.assertEqual(hours, 1, "Incorrect hours amount")

    def test_5(self):
        start = datetime(2022, 8, 19, 18, 0, 00)
        end = datetime(2022, 8, 19, 19, 0, 00)
        data = TestDatesMethods.get_weather_request(start, end)
        start_date, hours = weather_service.parse_dates_from_request(data)
        start_date = datetime.strptime(start_date, "%m/%d/%Y, %H:%M")
        self.assertEqual(start_date.hour, 18, "Incorrect start hour")
        self.assertEqual(start_date.minute, 0, "Incorrect start minutes")
        self.assertEqual(hours, 1, "Incorrect hours amount")

    def test_6(self):
        start = datetime(2022, 8, 19, 18, 0, 00)
        end = datetime(2022, 8, 19, 19, 30, 00)
        data = TestDatesMethods.get_weather_request(start, end)
        start_date, hours = weather_service.parse_dates_from_request(data)
        start_date = datetime.strptime(start_date, "%m/%d/%Y, %H:%M")
        self.assertEqual(start_date.hour, 18, "Incorrect start hour")
        self.assertEqual(start_date.minute, 0, "Incorrect start minutes")
        self.assertEqual(hours, 2, "Incorrect hours amount")

    def test_exception_when_start_date_is_greater(self):
        start = datetime(2022, 8, 19, 20, 30, 00)
        end = datetime(2022, 8, 19, 19, 30, 00)
        data = TestDatesMethods.get_weather_request(start, end)
        self.assertRaises(exc.StartDateHasToBeEarlierThenEndDate, weather_service.parse_dates_from_request, data)

    def test_exception_when_start_date_is_from_past(self):
        now = datetime.now()
        start = now - timedelta(days=1)
        end = now + timedelta(hours=2)
        data = TestDatesMethods.get_weather_request(start, end)
        self.assertRaises(exc.DatesShouldNotBeFromPast, weather_service.parse_dates_from_request, data)


@unittest.skip
class TestWeatherMethods(unittest.TestCase):
    @staticmethod
    def get_current_date_with_shift(shift):
        date = datetime.now()
        date = date.replace(minute=0, second=0, microsecond=0)
        return convert_date_to_unix_timestamp(date + timedelta(hours=shift))

    def test_exception_when_start_date_too_late(self):
        start = TestWeatherMethods.get_current_date_with_shift(80)
        end = TestWeatherMethods.get_current_date_with_shift(90)
        weather_request = WeatherRequest(lon=10, lat=10, start=start, end=end)
        self.assertRaises(exc.NotEnoughData, weather_service.get_weather_for_localization_and_time, weather_request)

    def test_forecast_range(self):
        start = TestWeatherMethods.get_current_date_with_shift(3)
        end = TestWeatherMethods.get_current_date_with_shift(7)
        weather_request = WeatherRequest(lon=10, lat=10, start=start, end=end)
        forecast = weather_service.get_weather_for_localization_and_time(weather_request)
        self.assertEqual(len(forecast), 5)

    def test_exception_when_end_date_is_too_late(self):
        start = TestWeatherMethods.get_current_date_with_shift(3)
        end = TestWeatherMethods.get_current_date_with_shift(80)
        weather_request = WeatherRequest(lon=10, lat=10, start=start, end=end)
        self.assertRaises(exc.NotEnoughData, weather_service.get_weather_for_localization_and_time, weather_request)


class TestChartCreationMethods(unittest.TestCase):
    @staticmethod
    def get_current_date_with_shift(shift):
        date = datetime.now()
        date = date.replace(minute=0, second=0, microsecond=0)
        return convert_date_to_unix_timestamp(date + timedelta(hours=shift))

    def test_forecast_range(self):
        start = TestChartCreationMethods.get_current_date_with_shift(3)
        end = TestChartCreationMethods.get_current_date_with_shift(7)
        weather_request = WeatherRequest(lon=10, lat=10, start=start, end=end)
        forecast = weather_service.get_weather_for_localization_and_time(weather_request)
        print(forecast)
        self.assertEqual(len(forecast), 4)

