# Biomass Energy Predictor

A local educational project that estimates energy output from biomass characteristics with a trained Linear Regression model. It includes a Streamlit interface and a React frontend connected to a Flask API.

## Features

- Predict estimated energy output in kWh from biomass quantity, moisture, and calorific value.
- Show an educational estimated CO2 reduction using an assumed factor of 0.7 kg CO2/kWh.
- Run the app through Streamlit or through the React frontend and Flask API.

The model uses a small sample dataset for demonstration. Predictions and CO2 estimates are educational and are not engineering guarantees or verified emissions measurements.

## Requirements

- Python 3.10 or newer
- Node.js and npm for the React frontend

Run these PowerShell commands from the repository root to prepare the Python environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\biomass-energy-prediction\requirements.txt
```

## Run the Streamlit app

```powershell
.\.venv\Scripts\python.exe -m streamlit run .\biomass-energy-prediction\app.py
```

Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Run the React frontend and Flask API

Start the API in one PowerShell terminal:

```powershell
.\.venv\Scripts\python.exe .\biomass-energy-prediction\api.py
```

In a second terminal, install and start the frontend:

```powershell
cd .\biopredict-frontend
npm install
npm run dev -- --host 127.0.0.1
```

Open `http://127.0.0.1:5173`. Keep both terminals running while using the app.

## Retrain the model (optional)

The trained model is included under `biomass-energy-prediction/model`. To retrain it from the included CSV dataset:

```powershell
.\.venv\Scripts\python.exe .\biomass-energy-prediction\model\train_model.py
```

See [the backend README](biomass-energy-prediction/README.md) for dataset details, model evaluation, limitations, and additional project information.
