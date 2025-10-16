import streamlit as st
from joblib import load
import numpy as np
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Smart Energy Prediction ⚡", page_icon="🏙️", layout="centered")

# --- Background: modern smart city & energy buildings ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1581091870633-1eea1c90a6f0');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
div.stButton > button {
    background: linear-gradient(90deg, #007bff, #00c6ff);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #00c6ff, #007bff);
    color: black;
}
.css-1cpxqw2, .stNumberInput input {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 8px;
    padding: 8px;
    color: #000;
    font-weight: 500;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Load model
model = load("linear_regression_model.joblib")

# Title and subtitle
st.markdown("<h1 style='text-align:center;color:#00c6ff;'>🏙️ Smart Building Energy Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:white;'>Estimate your building's energy performance using AI-powered modeling ⚡</p>", unsafe_allow_html=True)

# Input section with columns
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🏗️ Enter Building Parameters")

col1, col2 = st.columns(2)
with col1:
    X1 = st.number_input("Relative Compactness", min_value=0.62, max_value=0.98, value=0.75)
    X2 = st.number_input("Surface Area", min_value=514.0, max_value=808.0, value=600.0)
    X3 = st.number_input("Wall Area", min_value=294.0, max_value=416.0, value=350.0)
    X4 = st.number_input("Roof Area", min_value=110.0, max_value=220.0, value=150.0)
with col2:
    X5 = st.number_input("Overall Height", min_value=3.0, max_value=7.0, value=3.5)
    X6 = st.number_input("Orientation", min_value=2, max_value=5, value=3)
    X7 = st.number_input("Glazing Area", min_value=0.0, max_value=0.4, value=0.2)
    X8 = st.number_input("Glazing Area Distribution", min_value=0, max_value=5, value=3)

# Predict button
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔍 Predict Energy Consumption"):
    features = np.array([[X1, X2, X3, X4, X5, X6, X7, X8]])
    prediction = model.predict(features)
    predicted_value = float(prediction[0][0])

    # --- Output card (blue electric glow) ---
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, rgba(0,40,80,0.9), rgba(0,80,160,0.85));
        color: #00eaff;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 25px rgba(0,0,0,0.5);
        ">
        <h2>Predicted Energy Consumption ⚡</h2>
        <h1 style="font-size:48px;">{predicted_value:.2f} kWh/m²</h1>
        <p style="color:#b3e5ff;">AI estimation based on building structure parameters</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Pie chart (energy blue) ---
    remaining = max(100 - predicted_value, 0)
    labels = ['Predicted Energy Use', 'Potential Efficiency']
    values = [predicted_value, remaining]
    colors = ['#00c6ff', '#002f5e']

    fig, ax = plt.subplots()
    fig.patch.set_facecolor("none")
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'color': 'white'})
    ax.set_facecolor("none")
    st.pyplot(fig)

    # --- Energy efficiency message ---
    if predicted_value < 20:
        st.success("🌱 Excellent! Your building is highly energy-efficient.")
    elif predicted_value < 35:
        st.info("💡 Good performance — optimization could improve efficiency further.")
    else:
        st.warning("⚠️ High consumption — review insulation and glazing parameters.")

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("💠 Powered by Streamlit | Smart Energy Modeling System")
