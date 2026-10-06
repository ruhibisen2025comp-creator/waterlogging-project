from flask import Flask, jsonify, request, send_from_directory
import math
import requests
import os

app = Flask(__name__, static_folder=".", static_url_path="")

OPEN_METEO = "https://api.open-meteo.com/v1/forecast"
GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"

# Pune-focused historical records currently stored in event.json.
with open("event.json", "r", encoding="utf-8") as f:
    import json
    EVENTS = json.load(f)

def geocode_pune(query):
    response = requests.get(
        GEOCODING,
        params={"name": f"{query}, Pune, Maharashtra, India", "count": 5, "language": "en", "format": "json"},
        timeout=10,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    if not results:
        raise ValueError("Location not found. Please enter a Pune locality or landmark.")
    # Prefer a result inside the Pune district/city area.
    for item in results:
        country = str(item.get("country", "")).lower()
        admin = str(item.get("admin1", "")).lower()
        if "india" in country and "maharashtra" in admin:
            return item
    return results[0]

def get_weather(latitude, longitude):
    response = requests.get(
        OPEN_METEO,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "rain,precipitation,relative_humidity_2m",
            "timezone": "Asia/Kolkata",
        },
        timeout=10,
    )
    response.raise_for_status()
    current = response.json()["current"]
    return {
        "rain_mm": float(current.get("rain") or 0),
        "precipitation_mm": float(current.get("precipitation") or 0),
        "humidity": float(current.get("relative_humidity_2m") or 0),
    }

def get_elevation(latitude, longitude):
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": latitude, "longitude": longitude, "current": "temperature_2m", "elevation": "true"},
        timeout=10,
    )
    response.raise_for_status()
    return float(response.json().get("elevation") or 0)

def nearby_hotspots(latitude, longitude, radius_km=8):
    found = []
    for item in EVENTS:
        if str(item.get("city", "")).lower() != "pune":
            continue
        lat = float(item["latitude"])
        lon = float(item["longitude"])
        dlat = math.radians(lat - latitude)
        dlon = math.radians(lon - longitude)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(latitude)) * math.cos(math.radians(lat)) * math.sin(dlon / 2) ** 2
        distance = 6371 * 2 * math.asin(math.sqrt(a))
        if distance <= radius_km:
            copy = dict(item)
            copy["distance_km"] = round(distance, 2)
            found.append(copy)
    return sorted(found, key=lambda x: x["distance_km"])

def call_ml(elevation, slope, precipitation, humidity):
    payload = {
        "elevation": elevation,
        "slope": slope,
        "precipitation": precipitation,
        "humidity": humidity,
    }
    try:
        response = requests.post("http://127.0.0.1:5001/predict", json=payload, timeout=8)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        return {"status": "unavailable", "message": str(exc)}

@app.get("/")
def home():
    return send_from_directory(".", "index.html")

@app.get("/api/hotspots")
def hotspots():
    return jsonify([
        item for item in EVENTS
        if str(item.get("city", "")).lower() == "pune"
    ])

@app.get("/api/risk")
def risk():
    query = request.args.get("location", "").strip()
    if not query:
        return jsonify({"error": "Please enter a Pune location."}), 400

    try:
        place = geocode_pune(query)
        latitude = float(place["latitude"])
        longitude = float(place["longitude"])
        weather = get_weather(latitude, longitude)
        elevation = get_elevation(latitude, longitude)

        # The current trained model expects a slope feature. Until a verified
        # slope layer is connected, keep this explicit rather than hiding it.
        slope = 2.0

        prediction = call_ml(
            elevation=elevation,
            slope=slope,
            precipitation=weather["precipitation_mm"],
            humidity=weather["humidity"],
        )

        nearby = nearby_hotspots(latitude, longitude)

        return jsonify({
            "location": {
                "name": place.get("name") or query,
                "latitude": latitude,
                "longitude": longitude,
            },
            "weather": weather,
            "terrain": {
                "elevation": elevation,
                "slope": slope,
                "slope_source": "temporary model input; replace with verified GIS slope layer",
            },
            "nearby_hotspots": len(nearby),
            "historical_hotspots": nearby,
            "prediction": prediction,
        })
    except (requests.RequestException, ValueError, KeyError) as exc:
        return jsonify({"error": str(exc)}), 502

@app.get("/health")
def health():
    return jsonify({"status": "online", "service": "Pune WaterGuard backend"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
