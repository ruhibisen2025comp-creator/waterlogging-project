from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "waterlogging_rf_model.joblib")
model = None

try:
    model = joblib.load(MODEL_PATH)
except Exception as exc:
    print("Model load error:", exc)

@app.get("/health")
def health():
    return jsonify({
        "status": "online",
        "service": "Pune WaterGuard ML",
        "model_loaded": model is not None
    })

@app.post("/predict")
def predict():
    if model is None:
        return jsonify({"status": "error", "message": "ML model is not available."}), 503

    data = request.get_json(silent=True) or {}
    required = ["elevation", "slope", "precipitation", "humidity"]
    missing = [key for key in required if key not in data]
    if missing:
        return jsonify({"status": "error", "message": "Missing: " + ", ".join(missing)}), 400

    try:
        values = {key: float(data[key]) for key in required}
        frame = pd.DataFrame([values], columns=required)

        predicted = int(model.predict(frame)[0])
        probability = float(model.predict_proba(frame)[0][1]) * 100

        if probability >= 70:
            level = "HIGH"
        elif probability >= 30:
            level = "MODERATE"
        else:
            level = "LOW"

        return jsonify({
            "status": "success",
            "waterlogging_risk": predicted,
            "risk_probability": round(probability, 2),
            "risk_level": level
        })
    except (ValueError, TypeError) as exc:
        return jsonify({"status": "error", "message": str(exc)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
