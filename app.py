from flask import Flask, jsonify, request, send_from_directory
import json
import math
import os

import joblib
import pandas as pd
import requests

app = Flask(__name__, static_folder=".", static_url_path="")

OPEN_METEO = "https://api.open-meteo.com/v1/forecast"
GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "ml",
    "waterlogging_rf_model.joblib",
)

with open(os.path.join(os.path.dirname(__file__), "event.json"), "r", encoding="utf-8") as f:
    EVENTS = json.load(f)

try:
    MODEL = joblib.load(MODEL_PATH)
    MODEL_ERROR = None
except Exception as exc:
    MODEL = None
    MODEL_ERROR = str(exc)


def geocode_pune(query):
    # Open-Meteo is useful for cities, but some Pune localities are not
    # present in its GeoNames index. Try Open-Meteo first.
    search_names = [
        f"{query}, Pune, Maharashtra",
        f"{query}, Pune",
        query,
    ]

    for search_name in search_names:
        response = requests.get(
            GEOCODING,
            params={
                "name": search_name,
                "count": 10,
                "language": "en",
                "format": "json",
                "countryCode": "IN",
            },
            timeout=10,
        )
        response.raise_for_status()
        results = response.json().get("results", [])

        for item in results:
            country = str(item.get("country", "")).lower()
            admin = str(item.get("admin1", "")).lower()
            if "india" in country and "maharashtra" in admin:
                return item

    # Fallback to OpenStreetMap Nominatim, which has better coverage
    # for neighbourhoods/localities such as Kothrud, Wakad and Hadapsar.
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={
            "q": f"{query}, Pune, Maharashtra, India",
            "format": "jsonv2",
            "limit": 10,
            "addressdetails": 1,
        },
        headers={
            "User-Agent": "Pune-WaterGuard/1.0",
        },
        timeout=10,
    )
    response.raise_for_status()
    results = response.json()

    for item in results:
        address = item.get("address", {})
        country = str(address.get("country", "")).lower()
        state = str(address.get("state", "")).lower()
        city = " ".join([
            str(address.get("city", "")),
            str(address.get("town", "")),
            str(address.get("municipality", "")),
            str(address.get("county", "")),
        ]).lower()

        if (
            "india" in country
            and "maharashtra" in state
            and "pune" in city
        ):
            return {
                "name": item.get("display_name", query).split(",")[0],
                "latitude": float(item["lat"]),
                "longitude": float(item["lon"]),
            }

    raise ValueError(
        "Location not found. Please enter a Pune locality or landmark."
    )


def get_weather(latitude, longitude):
    response = requests.get(
        OPEN_METEO,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "precipitation,rain,relative_humidity_2m",
            "timezone": "Asia/Kolkata",
        },
        timeout=10,
    )
    response.raise_for_status()
    current = response.json().get("current", {})

    return {
        "rain_mm": float(current.get("rain") or 0),
        "precipitation_mm": float(current.get("precipitation") or 0),
        "humidity": float(current.get("relative_humidity_2m") or 0),
    }


def get_elevation(latitude, longitude):
    response = requests.get(
        OPEN_METEO,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m",
            "elevation": "true",
            "timezone": "Asia/Kolkata",
        },
        timeout=10,
    )
    response.raise_for_status()
    return float(response.json().get("elevation") or 0)


def estimate_slope(latitude, longitude):
    # The current project does not contain a verified GIS slope layer.
    return 2.0


def estimate_low_lying_basin(elevation, slope):
    return 1 if elevation < 560 and slope < 2.5 else 0


def nearby_hotspots(latitude, longitude, radius_km=8):
    found = []

    for item in EVENTS:
        if str(item.get("city", "")).lower() != "pune":
            continue

        lat = float(item["latitude"])
        lon = float(item["longitude"])

        dlat = math.radians(lat - latitude)
        dlon = math.radians(lon - longitude)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(latitude))
            * math.cos(math.radians(lat))
            * math.sin(dlon / 2) ** 2
        )
        distance = 6371 * 2 * math.asin(math.sqrt(a))

        if distance <= radius_km:
            copy = dict(item)
            copy["distance_km"] = round(distance, 2)
            found.append(copy)

    return sorted(found, key=lambda x: x["distance_km"])


def predict_risk(elevation, slope, precipitation, humidity):
    if MODEL is None:
        raise RuntimeError(f"ML model could not be loaded: {MODEL_ERROR}")

    # These four feature names match the trained Random Forest model.
    features = pd.DataFrame([{
        "elevation": elevation,
        "slope": slope,
        "precipitation": precipitation,
        "humidity": humidity,
    }])

    prediction = int(MODEL.predict(features)[0])
    probability = float(MODEL.predict_proba(features)[0][1]) * 100

    if probability >= 70:
        level = "HIGH"
    elif probability >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "status": "SUCCESS",
        "waterlogging_risk": prediction,
        "risk_probability": round(probability, 2),
        "risk_level": level,
    }


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
        slope = estimate_slope(latitude, longitude)
        is_basin = estimate_low_lying_basin(elevation, slope)

        prediction = predict_risk(
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
                "is_low_lying_basin": is_basin,
                "slope_source": "project fallback estimate; replace with verified GIS layer",
            },
            "nearby_hotspots": len(nearby),
            "historical_hotspots": nearby,
            "prediction": prediction,
        })

    except requests.RequestException as exc:
        return jsonify({"error": f"External data service unavailable: {exc}"}), 502
    except (ValueError, KeyError, TypeError, RuntimeError) as exc:
        return jsonify({"error": str(exc)}), 500


@app.get("/health")
def health():
    return jsonify({
        "status": "online",
        "service": "Pune WaterGuard",
        "ml_model_loaded": MODEL is not None,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
