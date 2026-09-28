from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return "Waterlogging Backend is Working!"


@app.route("/weather")
def weather():

    latitude = 18.5204
    longitude = 73.8567

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "rain,precipitation,relative_humidity_2m"
    }

    response = requests.get(url, params=params)
    data = response.json()

    current = data["current"]

    result = {
        "location": "Pune",
        "latitude": latitude,
        "longitude": longitude,
        "rainfall_mm": current["rain"],
        "precipitation_mm": current["precipitation"],
        "humidity_percent": current["relative_humidity_2m"]
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)