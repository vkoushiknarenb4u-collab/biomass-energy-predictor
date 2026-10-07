"""Small local API that connects the React frontend to the trained model."""

import json
from pathlib import Path

import joblib
from flask import Flask, jsonify, request


PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "model" / "linear_regression_model.joblib"
PREPROCESSING_PATH = PROJECT_DIR / "model" / "preprocessing.json"
EMISSION_FACTOR_KG_CO2_PER_KWH = 0.7

app = Flask(__name__)
model = joblib.load(MODEL_PATH)
preprocessing = json.loads(PREPROCESSING_PATH.read_text(encoding="utf-8"))


@app.after_request
def add_cors_headers(response):
    """Allow the local Vite development server to call this local API."""
    response.headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:5173"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.get("/health")
def health_check():
    return jsonify({"status": "ok", "model": "LinearRegression"})


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    required_fields = ["biomass_type", "quantity_kg", "moisture_percent", "calorific_value_mj_kg"]
    missing_fields = [field for field in required_fields if field not in payload]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        quantity = float(payload["quantity_kg"])
        moisture = float(payload["moisture_percent"])
        calorific_value = float(payload["calorific_value_mj_kg"])
    except (TypeError, ValueError):
        return jsonify({"error": "Numeric inputs must be valid numbers."}), 400

    if quantity <= 0:
        return jsonify({"error": "Quantity must be greater than 0 kg."}), 400
    if not 0 <= moisture <= 100:
        return jsonify({"error": "Moisture must be between 0 and 100 percent."}), 400
    if calorific_value <= 0:
        return jsonify({"error": "Calorific value must be greater than 0 MJ/kg."}), 400

    features = [[quantity, moisture, calorific_value]]
    prediction = float(model.predict(features)[0])
    co2_reduction = prediction * EMISSION_FACTOR_KG_CO2_PER_KWH

    return jsonify({
        "biomass_type": payload["biomass_type"],
        "quantity_kg": quantity,
        "moisture_percent": moisture,
        "calorific_value_mj_kg": calorific_value,
        "predicted_energy_kwh": prediction,
        "estimated_co2_reduction_kg": co2_reduction,
        "emission_factor_kg_co2_per_kwh": EMISSION_FACTOR_KG_CO2_PER_KWH,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
