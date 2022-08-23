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
