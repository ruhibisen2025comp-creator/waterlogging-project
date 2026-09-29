"""
ML Inference & Alert Payload Engine
Module: Pune Urban Waterlogging Risk Analyzer
"""

import joblib
import pandas as pd
import json

# Path to serialized model artifact
MODEL_PATH = "ml/waterlogging_model.pkl"

def load_inference_model():
    """Loads the trained Random Forest model from disk."""
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Run train_model.py first.")

def predict_waterlogging_risk(location_name, latitude, longitude, elevation_m, slope_pct, is_basin, precip_mm, humidity_pct):
    """
    Executes ML inference on terrain & weather parameters.
    
    Returns:
        dict: Standardized payload with classification, risk percentage, 
              risk category, and conditional PMC authority alert.
    """
    model = load_inference_model()

    # Format input features matching training data columns
    input_features = pd.DataFrame([{
        'latitude': latitude,
        'longitude': longitude,
        'ground_elevation_m': elevation_m,
        'slope_percentage': slope_pct,
        'is_low_lying_basin': is_basin,
        'precipMM': precip_mm,
        'humidity': humidity_pct
    }])

    # Model inference: raw class & risk probability
    prediction = int(model.predict(input_features)[0])
    risk_prob = float(model.predict_proba(input_features)[0][1])
    risk_percentage = round(risk_prob * 100, 2)

    # Risk categorization logic
    if risk_percentage >= 70:
        risk_category = "HIGH"
    elif risk_percentage >= 30:
        risk_category = "MEDIUM"
    else:
        risk_category = "LOW"

    # Base response payload for frontend/maps integration
    response_payload = {
        "status": "SUCCESS",
        "location": location_name,
        "coordinates": {"latitude": latitude, "longitude": longitude},
        "is_waterlogged": bool(prediction),
        "risk_percentage": f"{risk_percentage}%",
        "risk_category": risk_category,
        "pmc_authority_alert": None
    }

    # Construct Municipal Authority Alert Payload if High Risk (>70%)
    if risk_category == "HIGH":
        response_payload["pmc_authority_alert"] = {
            "alert_id": f"PMC-ALERT-{int(latitude*1000)}-{int(longitude*1000)}",
            "alert_level": "CRITICAL",
            "location": location_name,
            "coordinates": {"lat": latitude, "lng": longitude},
            "risk_score": f"{risk_percentage}%",
            "action_required": "Dispatch de-watering pump unit & signal traffic diversion",
            "department": "Pune Municipal Corporation (PMC) Drainage & Traffic Control"
        }

    return response_payload


# --- Local Module Verification Test ---
if __name__ == "__main__":
    # Test sample: High-risk scenario in Swargate low-lying area
    sample_output = predict_waterlogging_risk(
        location_name="Swargate Underpass",
        latitude=18.5000,
        longitude=73.8500,
        elevation_m=10.2,
        slope_pct=1.1,
        is_basin=1,
        precip_mm=82.5,
        humidity_pct=94.0
    )
    
    print("\n=== INFERENCE RESULT ===")
    print(json.dumps(sample_output, indent=2))