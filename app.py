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


@app.route("/risk")
def risk():

    # Pune location
    latitude = 18.5204
    longitude = 73.8567

    # Get live weather data
    weather_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "rain,precipitation,relative_humidity_2m"
    }

    weather_response = requests.get(weather_url, params=params)
    weather_data = weather_response.json()
    current = weather_data["current"]

    precipitation = current["precipitation"]
    humidity = current["relative_humidity_2m"]

    # Temporary terrain values for testing
    elevation = 510.5
    slope = 1.2

    # Send data to ML service
    ml_url = "http://127.0.0.1:5001/predict"

    ml_data = {
        "elevation": elevation,
        "slope": slope,
        "precipitation": precipitation,
        "humidity": humidity
    }

    ml_response = requests.post(
        ml_url,
        json=ml_data
    )

    prediction = ml_response.json()

    return jsonify({
        "location": "Pune",
        "weather": {
            "precipitation_mm": precipitation,
            "humidity_percent": humidity
        },
        "terrain": {
            "elevation": elevation,
            "slope": slope
        },
        "prediction": prediction
    })


if __name__ == "__main__":
    app.run(debug=True)