import streamlit as st
from joblib import load
import numpy as np

# Load model
model = load("linear_regression_model.joblib")

st.title("Energy Prediction 🚀")
st.write("Enter environmental features to predict energy consumption (kWh/m²):")

# Inputs with realistic min/max values (from typical energy dataset)
X1 = st.number_input("Relative Compactness", min_value=0.62, max_value=0.98, value=0.75)
X2 = st.number_input("Surface Area", min_value=514.0, max_value=808.0, value=600.0)
X3 = st.number_input("Wall Area", min_value=294.0, max_value=416.0, value=350.0)
X4 = st.number_input("Roof Area", min_value=110.0, max_value=220.0, value=150.0)
X5 = st.number_input("Overall Height", min_value=3.0, max_value=7.0, value=3.5)
X6 = st.number_input("Orientation", min_value=2, max_value=5, value=3)
X7 = st.number_input("Glazing Area", min_value=0.0, max_value=0.4, value=0.2)
X8 = st.number_input("Glazing Area Distribution", min_value=0, max_value=5, value=3)

if st.button("Predict"):
    features = np.array([[X1, X2, X3, X4, X5, X6, X7, X8]])
    prediction = model.predict(features)
    st.success(f"Predicted Energy Consumption: {prediction[0][0]:.2f} kWh/m²")
