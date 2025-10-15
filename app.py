import streamlit as st
from joblib import load
import numpy as np
import pandas as pd

# Load trained model
model = load("linear_regression_model.joblib")

# --- PAGE CONFIG ---
st.set_page_config(page_title="Energy Prediction Dashboard", page_icon="⚡", layout="centered")

# --- HEADER ---
st.title("🏠 Building Energy Prediction Dashboard")
st.markdown("### Predict Energy Consumption (kWh/m²)")
st.write("Adjust the sliders below to simulate different building conditions and estimate the energy load.")

# --- LAYOUT: Input columns ---
col1, col2 = st.columns(2)

with col1:
    X1 = st.slider("Relative Compactness", 0.62, 0.98, 0.75)
    X2 = st.slider("Surface Area", 514.0, 808.0, 600.0)
    X3 = st.slider("Wall Area", 294.0, 416.0, 350.0)
    X4 = st.slider("Roof Area", 110.0, 220.0, 150.0)

with col2:
    X5 = st.slider("Overall Height", 3.0, 7.0, 3.5)
    X6 = st.slider("Orientation", 2, 5, 3)
    X7 = st.slider("Glazing Area", 0.0, 0.4, 0.2)
    X8 = st.slider("Glazing Area Distribution", 0, 5, 3)

# --- PREDICTION ---
if st.button("🔮 Predict Energy Consumption"):
    features = np.array([[X1, X2, X3, X4, X5, X6, X7, X8]])
    prediction = model.predict(features)[0][0]

    st.success(f"### Predicted Energy Consumption: **{prediction:.2f} kWh/m²**")

    # --- Visualization ---
    chart_data = pd.DataFrame({
        'Feature': ['Predicted Energy (kWh/m²)'],
        'Value': [prediction]
    })

    st.markdown("#### 📊 Prediction Visualization")
    st.bar_chart(chart_data.set_index('Feature'))

    st.info("Lower values indicate better energy efficiency. Typical residential buildings range from 10–50 kWh/m².")

# --- FOOTER ---
st.markdown("---")
st.caption("Developed with ❤️ using Streamlit and Machine Learning")
