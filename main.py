from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
import traceback

from core.services import weather_api_handler
from core.dto import ForecastRequest
from core import constants
from core.logger import get_logger

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/weather")
def get_weather_for_localization(start: str, end: str, lat: float = 0.0, lon: float = 0.0, max_range: Union[int, None] = None):
    weather_request = ForecastRequest(lon=lon, lat=lat, start=start, end=end)
    if max_range:
        constants.MAX_HOURLY_RANGE = max_range
    try:
        response = weather_api_handler.get_weather_for_localization_and_time(weather_request)
        return response
    except Exception as e:
        tb = traceback.format_exc()
        get_logger().debug(tb)
        raise HTTPException(status_code=404, detail=str(e))
