from flask import Flask, jsonify, render_template
import requests

from ml.predict import predict_waterlogging_risk

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


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

    latitude = 18.5204
    longitude = 73.8567
    location_name = "Pune"

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
    is_basin = 1

    # Connect directly to ML model
    prediction = predict_waterlogging_risk(
        location_name=location_name,
        latitude=latitude,
        longitude=longitude,
        elevation_m=elevation,
        slope_pct=slope,
        is_basin=is_basin,
        precip_mm=precipitation,
        humidity_pct=humidity
    )

    return jsonify({
        "location": location_name,

        "weather": {
            "precipitation_mm": precipitation,
            "humidity_percent": humidity
        },

        "terrain": {
            "elevation_m": elevation,
            "slope_percentage": slope,
            "is_low_lying_basin": is_basin
        },

        "prediction": prediction
    })


if __name__ == "__main__":
    app.run(debug=True)