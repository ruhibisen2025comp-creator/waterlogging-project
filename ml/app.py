from flask import Flask, request, jsonify
import joblib
import os

app = Flask(__name__)

# Load model safely
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'waterlogging_model.pkl')
model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Warning: Could not load model file ({e}). Using heuristic fallback.")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json() or {}
    
    # Extract the 7 parameters
    lat = float(data.get('latitude', 18.5204))
    lng = float(data.get('longitude', 73.8567))
    elev = float(data.get('elevation', 560))
    slope = float(data.get('slope', 2.0))
    basin = int(data.get('is_basin', 0))
    precip = float(data.get('precipitation', 0.0))
    humidity = float(data.get('humidity', 50.0))

    risk_level = "Low"
    probability = 0.20
    pmc_alert = False

    # ML Inference using pure Python list (No pandas needed)
    if model is not None:
        try:
            feature_vector = [[lat, lng, elev, slope, basin, precip, humidity]]
            pred = model.predict(feature_vector)[0]
            
            if hasattr(model, 'predict_proba'):
                probs = model.predict_proba(feature_vector)[0]
                probability = float(probs[1]) if len(probs) > 1 else float(pred)
            else:
                probability = float(pred)

            if probability >= 0.7 or pred == 2 or (basin == 1 and precip > 15):
                risk_level = "High"
                pmc_alert = True
            elif probability >= 0.4 or pred == 1 or precip > 8:
                risk_level = "Medium"
                pmc_alert = False
            else:
                risk_level = "Low"
                pmc_alert = False
        except Exception as err:
            print(f"Model prediction error: {err}")
            # Fallback heuristic logic if ML model execution hits an array shape issue
            if precip > 15 or (basin == 1 and precip > 5):
                risk_level, probability, pmc_alert = "High", 0.85, True
            elif precip > 5:
                risk_level, probability, pmc_alert = "Medium", 0.50, False
            else:
                risk_level, probability, pmc_alert = "Low", 0.15, False
    else:
        # Fallback if pickle model isn't found
        if precip > 15 or (basin == 1 and precip > 5):
            risk_level, probability, pmc_alert = "High", 0.85, True
        elif precip > 5:
            risk_level, probability, pmc_alert = "Medium", 0.50, False

    return jsonify({
        "status": "success",
        "risk_level": risk_level,
        "probability": round(probability, 2),
        "pmc_authority_alert": pmc_alert,
        "features_received": {
            "latitude": lat,
            "longitude": lng,
            "elevation": elev,
            "slope": slope,
            "is_basin": basin,
            "precipitation": precip,
            "humidity": humidity
        }
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)