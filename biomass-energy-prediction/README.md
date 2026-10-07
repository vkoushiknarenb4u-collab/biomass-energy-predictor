# Biomass Energy Prediction for Sustainable Energy

## Project Overview

This beginner-friendly B.Tech AIML mini-project predicts the energy that can be generated from a user-provided quantity of biomass. It is completely software-based and uses a simple Linear Regression model with a Streamlit web interface.

## Problem Statement

Biomass waste such as crop residues, food waste, and wood waste can be used as an energy resource. Estimating its possible energy output can help explain how waste may support renewable energy planning.

## Objectives

- Train a machine learning model to estimate energy generation in kWh.
- Use basic biomass characteristics as model inputs.
- Provide a simple web application for user predictions.
- Explain possible sustainability links to SDG 7, SDG 12, and SDG 13.
- Demonstrate an estimated, assumption-based CO2 reduction calculation.

## Technologies Used

- Python
- pandas
- scikit-learn
- Linear Regression
- joblib
- Flask
- Streamlit

## System Architecture

```text
User
	|
	v
Streamlit Web Application
	|
	v
Input Validation
	|
	v
ML Model
	|
	v
Energy Prediction
	|
	v
Sustainability Calculation
	|
	v
SDG Impact
```

## Dataset Description

The file `data/biomass_data.csv` contains 120 sample records. It includes six biomass types:

- Rice Husk
- Sugarcane Bagasse
- Coconut Shell
- Corn Stalk
- Wood Waste
- Food Waste

The dataset is a realistic educational sample, not a live measurement database. Each row contains biomass characteristics and an energy output value used as the prediction target.

## Input Features

- `quantity_kg`: quantity of biomass in kilograms
- `moisture_percent`: moisture content from 0 to 100 percent
- `calorific_value_mj_kg`: energy content in MJ/kg

`biomass_type` is shown to the user but is not used directly as a numerical model feature.

## ML Algorithm

The project uses Linear Regression from scikit-learn. The model learns the relationship between the three numeric input features and `energy_kwh`.

## How the Model Works

1. Load and validate the CSV data.
2. Convert numeric columns to numeric values and fill missing numeric values with their medians.
3. Split the data into training and testing sets.
4. Train a Linear Regression model on the training data.
5. Evaluate predictions on the test data.
6. Save the model as `model/linear_regression_model.joblib`.
7. Save feature and preprocessing information as `model/preprocessing.json`.

## Model Evaluation

The training script prints four test-set metrics:

- MAE: Mean Absolute Error
- MSE: Mean Squared Error
- RMSE: Root Mean Squared Error
- R2: R-squared score

With the included sample dataset and fixed random seed, the current evaluation is approximately:

- MAE: 29.17 kWh
- MSE: 1781.10
- RMSE: 42.20 kWh
- R2: 0.91

These results are for an educational sample dataset and should not be treated as a real engineering performance guarantee.

## Web Application Features

- Select one of six biomass types.
- Enter quantity, moisture percentage, and calorific value.
- Validate user input before prediction.
- Display predicted energy generation in kWh.
- Show the entered biomass information.
- Display a simple predicted-energy chart.
- Calculate an estimated CO2 reduction.
- Explain SDG 7, SDG 12, and SDG 13 connections.

## Sustainability and SDG Connections

### SDG 7 - Affordable and Clean Energy

Biomass waste can be converted into a useful renewable energy resource. This project demonstrates a simple way to estimate that possible energy output.

### SDG 12 - Responsible Consumption and Production

Using agricultural, food, and wood waste for energy can support better resource use and reduce waste sent for disposal.

### SDG 13 - Climate Action

Replacing some higher-emission energy with biomass-based energy may support climate action. The application presents this as an educational estimate.

## Estimated CO2 Reduction

The application uses this simple, configurable assumption:

```text
Estimated CO2 reduction = predicted energy in kWh x 0.7 kg CO2/kWh
```

The factor `0.7 kg CO2/kWh` is an assumed educational emission factor. The result is not measured by a sensor and is not a verified carbon credit or emissions report.

## Advantages

- Simple and easy to explain in a viva.
- Completely software-based and usable offline.
- Uses a common machine learning algorithm.
- Includes input validation and clear results.
- Connects the technical output to sustainability goals.

## Limitations

- The dataset is a small educational sample rather than a field dataset.
- Linear Regression may not represent all real biomass processes.
- The CO2 result is based on an assumption, not direct measurement.
- The application does not account for plant efficiency, transport, or operating conditions.
- It does not use sensors, IoT devices, or real-time data.

## Future Enhancement

- Add a larger, validated real-world dataset.
- Compare Linear Regression with other explainable models.
- Add more evaluation plots and cross-validation.
- Allow users to upload a compatible dataset.
- Refine the emission factor using a documented regional energy baseline.

## Installation Steps

1. Install Python 3.10 or newer.
2. Open a terminal in the `biomass-energy-prediction` folder.
3. Install the required packages:

```bash
pip install -r requirements.txt
```

No API keys, databases, hardware, or internet connection are required after the packages have been installed.

## How to Run the Project

From the project folder, train the model:

```bash
python model/train_model.py
```

Then start the Streamlit application:

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit, usually `http://localhost:8501`.

## How to Run the React Frontend

The separate React frontend is in `../biopredict-frontend`. To connect it to the trained model, start the local prediction API from this project folder:

```bash
python api.py
```

The API runs at `http://127.0.0.1:5000`. In another terminal, start the frontend:

```bash
cd ../biopredict-frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`. The frontend sends biomass inputs to the Flask `/predict` endpoint, which loads the saved Linear Regression model and returns energy and estimated CO2 reduction values.

## Sample Input and Output

Sample input:

- Biomass type: Rice Husk
- Quantity: 100 kg
- Moisture: 12 percent
- Calorific value: 14.5 MJ/kg

The application returns a predicted energy value in kWh, an estimated CO2 reduction in kg, the biomass quantity used, a chart, and the related SDG explanations. The exact prediction depends on the trained model artifact.

## Offline and Hardware Note

This project runs locally after Python packages are installed. It does not require sensors, Arduino, ESP32, Raspberry Pi, cameras, IoT devices, external APIs, authentication, or a database.
