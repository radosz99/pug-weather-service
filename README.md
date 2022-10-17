# Info
Python application for getting weather for specific coordinates and time.

https://api.matcher.pl/v1/forecast?lat=51&lon=17&start=1663912800&end=1663941600  

Query parameters:
- `lat` - latitude of the place,
- `lon` - longitude of the place,
- `start` - start time of the forecast in unix timestamp,
- `end` - end time of the forecast in unix timestamp,

# Install
Clone repository:

```
$ git clone https://github.com/radosz99/pug-weather-service.git
```

Install `poetry` package:
```
$ pip install poetry
```
Install Python dependencies via poetry:
```
$ poetry install
```
After pulling new repository you can update packages viay:
```
$ poetry update
```


# Run

By activating virtualenv:
```
$ poetry shell
$ gunicorn main:app
 
```

Or via `poetry run`:
```
$ poetry run gunicorn main:app
```
Or via Docker:
```
$ docker build -t pug_weather_service .
$ docker run -d -p 8120:8120 pug_weather_service
```
