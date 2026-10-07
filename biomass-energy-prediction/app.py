"""Streamlit interface for the biomass energy prediction model."""

import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "model" / "linear_regression_model.joblib"
PREPROCESSING_PATH = PROJECT_DIR / "model" / "preprocessing.json"
BIOMASS_TYPES = [
	"Rice Husk",
	"Sugarcane Bagasse",
	"Coconut Shell",
	"Corn Stalk",
	"Wood Waste",
	"Food Waste",
]
# Simple educational assumption, not a sensor measurement or verified offset.
EMISSION_FACTOR_KG_CO2_PER_KWH = 0.7


st.set_page_config(
	page_title="Biomass Energy Predictor",
	page_icon="⚡",
	layout="centered",
)


@st.cache_resource
def load_prediction_artifacts():
	"""Load the trained model and its saved feature information once."""
	model = joblib.load(MODEL_PATH)
	preprocessing = json.loads(PREPROCESSING_PATH.read_text(encoding="utf-8"))
	return model, preprocessing


st.title("Biomass Energy Predictor")
st.write("Estimate energy generation from user-provided biomass characteristics.")
st.info(
	"This system provides an ML-based estimate using user-provided biomass "
	"characteristics. It does not directly measure biomass properties."
)

with st.form("prediction_form"):
	st.subheader("Biomass Information")
	biomass_type = st.selectbox("Biomass Type", BIOMASS_TYPES)
	quantity_kg = st.number_input(
		"Quantity of Biomass (kg)", min_value=0.0, value=100.0, step=1.0
	)
	moisture_percent = st.number_input(
		"Moisture Percentage", min_value=0.0, max_value=100.0, value=15.0, step=0.1
	)
	calorific_value = st.number_input(
		"Calorific Value (MJ/kg)", min_value=0.0, value=15.0, step=0.1
	)
	predict_clicked = st.form_submit_button(
		"PREDICT ENERGY", type="primary", use_container_width=True
	)

if predict_clicked:
	if quantity_kg <= 0:
		st.error("Quantity must be greater than 0 kg.")
	elif not 0 <= moisture_percent <= 100:
		st.error("Moisture must be between 0 and 100 percent.")
	elif calorific_value <= 0:
		st.error("Calorific value must be greater than 0 MJ/kg.")
	else:
		model, preprocessing = load_prediction_artifacts()
		input_data = pd.DataFrame(
			[[quantity_kg, moisture_percent, calorific_value]],
			columns=preprocessing["features"],
		)
		prediction = float(model.predict(input_data)[0])
		emission_reduction = prediction * EMISSION_FACTOR_KG_CO2_PER_KWH

		st.divider()
		st.subheader("Predicted Energy Generation")
		energy_column, co2_column, quantity_column = st.columns(3)
		energy_column.metric("Energy Prediction", f"{prediction:,.2f} kWh")
		co2_column.metric("Estimated CO₂ Reduction", f"{emission_reduction:,.2f} kg")
		quantity_column.metric("Biomass Quantity Used", f"{quantity_kg:,.2f} kg")

		st.subheader("Energy Generation Chart")
		chart_data = pd.DataFrame(
			{"Predicted Energy (kWh)": [prediction]}, index=[biomass_type]
		)
		st.bar_chart(chart_data)

		st.subheader("Entered Biomass Information")
		st.write(f"**Biomass Type:** {biomass_type}")
		st.write(f"**Quantity:** {quantity_kg:,.2f} kg")
		st.write(f"**Moisture:** {moisture_percent:,.2f}%")
		st.write(f"**Calorific Value:** {calorific_value:,.2f} MJ/kg")

		st.subheader("Sustainability Impact")
		st.write(
			"Converting biomass waste into useful energy can reduce waste sent to "
			"landfill and provide a renewable alternative to some fossil-fuel energy."
		)
		st.info(
			f"Estimated CO₂ Reduction = predicted energy × emission factor "
			f"({EMISSION_FACTOR_KG_CO2_PER_KWH} kg CO₂/kWh). This is an estimate "
			"based on an assumed emission factor, not a direct measurement."
		)

		sdg_7, sdg_12, sdg_13 = st.columns(3)
		sdg_7.markdown(
			"**SDG 7 – Affordable and Clean Energy**\n\n"
			"The project shows how biomass waste can be converted into a useful "
			"renewable energy estimate."
		)
		sdg_12.markdown(
			"**SDG 12 – Responsible Consumption and Production**\n\n"
			"Using agricultural and food waste for energy supports better use of "
			"resources and less waste."
		)
		sdg_13.markdown(
			"**SDG 13 – Climate Action**\n\n"
			"The estimated reduction helps explain the possible climate benefit of "
			"replacing higher-emission energy sources."
		)
