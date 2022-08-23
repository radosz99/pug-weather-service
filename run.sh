docker stop $(docker ps -q --filter ancestor=pug_weather_service)
docker build -t pug_weather_service .
docker run -d -p 8120:8120 pug_weather_service