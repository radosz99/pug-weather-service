from flask import Flask, request, jsonify
from flask_cors import CORS

from core.exceptions import HttpException
from core.services import weather_api_handler

app = Flask(__name__)
CORS(app)


@app.route("/weather", methods=['GET'])
def get_weather_for_localization():
    args = request.args.to_dict()
    forecast = weather_api_handler.get_forecast_for_given_parameters(args)
    # return forecast.__dict__
    return jsonify(forecast.to_dict())


@app.errorhandler(HttpException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
