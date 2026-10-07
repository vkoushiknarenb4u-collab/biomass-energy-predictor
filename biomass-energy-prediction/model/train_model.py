"""Train and save the biomass energy prediction model."""

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "biomass_data.csv"
MODEL_PATH = PROJECT_DIR / "model" / "linear_regression_model.joblib"
PREPROCESSING_PATH = PROJECT_DIR / "model" / "preprocessing.json"

FEATURES = [
	"quantity_kg",
	"moisture_percent",
	"calorific_value_mj_kg",
]
TARGET = "energy_kwh"


def load_and_validate_data():
	"""Load the CSV and check that the required columns and rows exist."""
	data = pd.read_csv(DATA_PATH)
	required_columns = ["biomass_type", *FEATURES, TARGET]
	missing_columns = [column for column in required_columns if column not in data]

	if missing_columns:
		raise ValueError(f"Missing required columns: {missing_columns}")
	if data.empty:
		raise ValueError("The dataset is empty.")

	# Biomass type is descriptive only; the model uses the three numeric features.
	numeric_columns = [*FEATURES, TARGET]
	for column in numeric_columns:
		data[column] = pd.to_numeric(data[column], errors="coerce")

	data[numeric_columns] = data[numeric_columns].fillna(
		data[numeric_columns].median()
	)
	return data


def main():
	data = load_and_validate_data()
	features = data[FEATURES]
	target = data[TARGET]

	# Keep a test set separate so the final metrics measure unseen data.
	features_train, features_test, target_train, target_test = train_test_split(
		features,
		target,
		test_size=0.2,
		random_state=42,
	)

	model = LinearRegression()
	model.fit(features_train, target_train)
	predictions = model.predict(features_test)

	mse = mean_squared_error(target_test, predictions)
	print("Model evaluation results:")
	print(f"MAE:  {mean_absolute_error(target_test, predictions):.4f}")
	print(f"MSE:  {mse:.4f}")
	print(f"RMSE: {mse ** 0.5:.4f}")
	print(f"R2:   {r2_score(target_test, predictions):.4f}")

	# Save the model and the feature order so app.py can make matching predictions.
	joblib.dump(model, MODEL_PATH)
	preprocessing = {
		"features": FEATURES,
		"target": TARGET,
		"missing_value_strategy": "median",
		"medians": {
			feature: float(data[feature].median()) for feature in FEATURES
		},
	}
	PREPROCESSING_PATH.write_text(json.dumps(preprocessing, indent=2), encoding="utf-8")
	print(f"Saved model to: {MODEL_PATH}")
	print(f"Saved preprocessing information to: {PREPROCESSING_PATH}")


if __name__ == "__main__":
	main()
