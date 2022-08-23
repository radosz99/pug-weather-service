from flask import Flask, request, jsonify
from flask_cors import CORS

from core.exceptions import HttpException
from core.services import weather_api_handler

app = Flask(__name__)
CORS(app)


@app.route("/api/v1/forecast", methods=['GET'])
def get_weather_for_localization():
    args = request.args.to_dict()
    forecast = weather_api_handler.get_forecast_for_given_parameters(args)
    response = jsonify(forecast.to_dict())
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add("Access-Control-Allow-Headers", '*')
    response.headers.add("Access-Control-Allow-Methods", '*')
    return response


@app.errorhandler(HttpException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
