import os
import json
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Pune locality coordinates & terrain lookup table matching 7 dataset parameters
PUNE_LOCALITIES = {
    "kothrud": {"name": "Kothrud", "lat": 18.5074, "lng": 73.8077, "elevation": 560.0, "slope": 2.5, "is_basin": 0},
    "karve nagar": {"name": "Karve Nagar", "lat": 18.4890, "lng": 73.8203, "elevation": 540.0, "slope": 1.8, "is_basin": 0},
    "swargate": {"name": "Swargate", "lat": 18.5000, "lng": 73.8500, "elevation": 510.2, "slope": 1.1, "is_basin": 1},
    "shivajinagar": {"name": "Shivajinagar", "lat": 18.5314, "lng": 73.8446, "elevation": 558.0, "slope": 1.5, "is_basin": 0},
    "viman nagar": {"name": "Viman Nagar", "lat": 18.5679, "lng": 73.9143, "elevation": 570.0, "slope": 1.0, "is_basin": 0},
    "hadapsar": {"name": "Hadapsar", "lat": 18.5089, "lng": 73.9260, "elevation": 540.0, "slope": 0.8, "is_basin": 1},
    "baner": {"name": "Baner", "lat": 18.5590, "lng": 73.7868, "elevation": 575.0, "slope": 2.1, "is_basin": 0},
    "aundh": {"name": "Aundh", "lat": 18.5580, "lng": 73.8075, "elevation": 565.0, "slope": 1.4, "is_basin": 0},
    "katraj": {"name": "Katraj", "lat": 18.4575, "lng": 73.8508, "elevation": 610.0, "slope": 3.8, "is_basin": 0},
    "deccan": {"name": "Deccan Gymkhana", "lat": 18.5167, "lng": 73.8417, "elevation": 552.0, "slope": 1.1, "is_basin": 1},
    "pune": {"name": "Pune Central", "lat": 18.5204, "lng": 73.8567, "elevation": 550.0, "slope": 1.5, "is_basin": 0}
}

# Historical flood hotspots for Leaflet map fallback
HISTORICAL_HOTSPOTS = [
    {"location": "Swargate Underpass", "latitude": 18.5000, "longitude": 73.8500},
    {"location": "Deccan Gymkhana / Goodluck Chowk", "latitude": 18.5167, "longitude": 73.8417},
    {"location": "Kothrud Bus Stand", "latitude": 18.5074, "longitude": 73.8077},
    {"location": "Katraj Lake Area", "latitude": 18.4575, "longitude": 73.8508},
    {"location": "Hadapsar Flyover Junction", "latitude": 18.5089, "longitude": 73.9260}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/hotspots")
def hotspots():
    return jsonify(HISTORICAL_HOTSPOTS)

@app.route("/api/events")
def get_events():
    json_path = os.path.join(app.root_path, "event.json")
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
        return jsonify(data)
    return jsonify([])

@app.route("/api/risk")
def risk():
    location_query = request.args.get("location", "pune").strip().lower()
    
    loc_data = PUNE_LOCALITIES.get(location_query, PUNE_LOCALITIES["pune"])
    loc_name = request.args.get("location", "Pune").strip() if location_query not in PUNE_LOCALITIES else loc_data["name"]

    latitude = loc_data["lat"]
    longitude = loc_data["lng"]
    elevation = loc_data["elevation"]
    slope = loc_data["slope"]
    is_basin = loc_data["is_basin"]

    # Fetch live weather data from Open-Meteo
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "rain,precipitation,relative_humidity_2m"
    }

    try:
        weather_response = requests.get(weather_url, params=params, timeout=5)
        weather_data = weather_response.json()
        current = weather_data.get("current", {})
        rain = current.get("rain", 0.0)
        precipitation = current.get("precipitation", 0.0)
        humidity = current.get("relative_humidity_2m", 60.0)
    except Exception:
        rain, precipitation, humidity = 0.0, 0.0, 60.0

    # Request prediction from ML Microservice running on port 5001 with ALL 7 features
    ml_url = "http://127.0.0.1:5001/predict"
    ml_payload = {
        "location": loc_name,
        "latitude": latitude,
        "longitude": longitude,
        "elevation": elevation,
        "slope": slope,
        "is_basin": is_basin,
        "precipitation": precipitation,
        "humidity": humidity
    }

    try:
        ml_response = requests.post(ml_url, json=ml_payload, timeout=5)
        prediction = ml_response.json()
    except Exception:
        prediction = {
            "risk_level": "Moderate",
            "probability": 50.0,
            "message": "ML service offline"
        }

    return jsonify({
        "location": {
            "name": loc_name,
            "latitude": latitude,
            "longitude": longitude
        },
        "weather": {
            "rain": rain,
            "precipitation": precipitation,
            "humidity": humidity
        },
        "terrain": {
            "elevation": elevation,
            "slope": slope,
            "is_basin": is_basin
        },
        "prediction": prediction
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True) 