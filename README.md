# UrbanFlow

UrbanFlow is a Flask-based urban waterlogging and transit risk analysis web platform designed for Pune. It evaluates environmental and topographical conditions along specific commuter corridors to predict flood risks and provide safe navigation options.

## Connected Architecture

Browser -> Flask `/api/risk` -> Open-Meteo geocoding -> Open-Meteo current weather -> Open-Meteo elevation -> Random Forest ML model -> historical hotspot dataset -> JSON response -> frontend result + Leaflet map + high-risk navigation hand-off

## Tech Stack
* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3, JavaScript
* **Mapping:** Leaflet.js, Open-Meteo Geocoding & Elevation APIs
* **Machine Learning:** Scikit-learn (Random Forest Model)

## Run Locally

1. Open the repository folder in VS Code or your terminal.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
Run the application:

Bash
python app.py
Open http://127.0.0.1:5000 in your browser.

Note: Only the main Flask server is required. The ML model is loaded directly by app.py.

Main Files
index.html — Website structure and UI layout

style.css — Custom styling and gradient themes

script.js — Frontend API calls, interactive Leaflet map, and navigation triggers

app.py — Backend routing, external data integration, and ML inference

event.json — Historical Pune flood hotspot records

ml/waterlogging_model.pkl — Trained Random Forest model

ml/predict.py — Standalone ML inference reference

ml/train_model.py — Model-training script

API Endpoints
GET / — Renders the main web interface

GET /api/risk?source=...&destination=... — Executes route-based risk analysis

GET /api/hotspots — Fetches Pune historical flood hotspots

GET /health — Backend and model health status check

## System Limitations & Disclaimer
The platform utilizes a fallback slope estimate when detailed GIS slope layers are pending, and flags this dynamically in the API response. UrbanFlow serves as an intelligent decision-support and hazard awareness system; predictions should be used alongside official municipal advisories during extreme weather events.
