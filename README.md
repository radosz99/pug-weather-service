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


# Run

By activating virtualenv:
```
$ poetry shell
$ uvicorn main:app
 
```

Or via `poetry run`:
```
$ poetry run uvicorn main:app
```
Or via Docker:
```
$ docker build -t pug_weather_service .
$ docker run -d -p 8120:8120 pug_weather_service
```
