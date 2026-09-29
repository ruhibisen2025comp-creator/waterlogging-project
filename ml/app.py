from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load pre-trained Random Forest Binary
MODEL_PATH = 'ml/waterlogging_rf_model.joblib'
try:
    model = joblib.load(MODEL_PATH)
    print("✓ Model successfully loaded into memory.")
except Exception as e:
    print(f"✗ Failed to load model binary: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for the main backend to verify ML service status."""
    return jsonify({
        "status": "online",
        "service": "Pune Waterlogging Risk ML Microservice",
        "model_loaded": model is not None
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Main Inference Endpoint.
    Expects JSON payload from Backend:
    {"elevation": 510.5, "slope": 1.2, "precipitation": 85.0, "humidity": 90.0}
    """
    try:
        data = request.get_json()
        
        # Validate required input features
        required_features = ['elevation', 'slope', 'precipitation', 'humidity']
        for feature in required_features:
            if feature not in data:
                return jsonify({"error": f"Missing required feature: '{feature}'"}), 400
        
        # Format incoming payload into DataFrame matching training schema
        input_df = pd.DataFrame([{
            'elevation': float(data['elevation']),
            'slope': float(data['slope']),
            'precipitation': float(data['precipitation']),
            'humidity': float(data['humidity'])
        }])
        
        # Execute model inference
        prediction_class = int(model.predict(input_df)[0])
        probability = float(model.predict_proba(input_df)[0][1])
        
        # Return structured JSON prediction response
        return jsonify({
            'waterlogging_risk': prediction_class,
            'risk_probability': round(probability, 4),
            'risk_level': 'HIGH' if prediction_class == 1 else 'LOW',
            'status': 'success'
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 