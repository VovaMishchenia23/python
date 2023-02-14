import datetime as dt

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
API_TOKEN = "dYVwJm9ZfzS4Qj/Z5Es?coNZXIzEkKfMRttS21t?g?pGVHd4ns/yQ-MEC2nbJkwB"
API_KEY = ""


def get_weather(location, date, name):

    url_base = "http://api.weatherapi.com/v1/history.json"
    url = f"{url_base}?key={API_KEY}&q={location}&dt={date}"

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        return {
            "name": name,
            "timestamp": dt.datetime.utcnow().isoformat() + "Z",
            "location": location,
            "date": date,
            "weather": weather_data
        }
    else:
        return {"error": "Failed to retrieve weather data"}


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p>Weather API</p>"


@app.route(
    "/weather"
)
def weather_endpoint():
    token = request.form.get("token")
    if token is None:
        raise InvalidUsage("token is required", status_code=400)

    if token != API_TOKEN:
        raise InvalidUsage(f"wrong API token {API_TOKEN}", status_code=403)

        exclude = request.form.get("exclude")

    result = get_weather(request.form.get("location"), request.form.get("date"), request.form.get("name"))
    return result
