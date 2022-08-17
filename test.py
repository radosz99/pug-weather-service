import requests

api_url = "https://api.openweathermap.org/data/3.0/onecall?"
api_key = "bff3552459e4f2133cee5085ac8f466c"

response = requests.get(url=api_url, params={'lat': 51.7, "lon": 17.4, "appid": api_key})
print(response.json())