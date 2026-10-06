# Pune WaterGuard

Pune WaterGuard is a Flask-based urban waterlogging risk awareness website.

## Connected architecture

Browser
-> Flask /api/risk
-> Open-Meteo geocoding
-> Open-Meteo current weather
-> Open-Meteo elevation
-> Random Forest ML model
-> historical hotspot dataset
-> JSON response
-> frontend result + Leaflet map

## Run locally

1. Install Python 3.10+.
2. Open a terminal in the repository folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the complete website:

```bash
python app.py
```

5. Open http://127.0.0.1:5000

Only the main Flask server is required. The ML model is loaded directly by app.py, so a separate ML server is not needed.

## Main files

- index.html — website structure
- style.css — website styling
- script.js — frontend API calls and interactive Leaflet map
- app.py — backend, external data integration and ML inference
- event.json — historical hotspot records
- ml/waterlogging_model.pkl — trained Random Forest model
- ml/predict.py — standalone ML inference reference
- ml/train_model.py — model-training code

## API endpoints

- GET / — website
- GET /api/risk?location=Kothrud — complete risk analysis
- GET /api/hotspots — Pune historical hotspots
- GET /health — backend and model health status

## Important limitation

The project does not yet contain a verified GIS slope layer. The backend therefore uses an explicit fallback slope estimate and marks it in the API response. Replace estimate_slope() with a verified GIS/elevation-derived slope calculation when that dataset is available.

The prediction is an awareness/decision-support estimate and should not be treated as guaranteed live road-condition information.
