import streamlit as st
from joblib import load
import numpy as np
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Energy Prediction ⚡", page_icon="💡", layout="centered")

# --- Custom CSS for blue energy styling ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1504384308090-c894fdcc538d');
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
    color: #000;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Load model
model = load("linear_regression_model.joblib")

# Title
st.title("💡 Energy Consumption Prediction")
st.write("Enter building parameters below to estimate **energy consumption (kWh/m²)**:")

# Inputs
X1 = st.number_input("Relative Compactness", min_value=0.62, max_value=0.98, value=0.75)
X2 = st.number_input("Surface Area", min_value=514.0, max_value=808.0, value=600.0)
X3 = st.number_input("Wall Area", min_value=294.0, max_value=416.0, value=350.0)
X4 = st.number_input("Roof Area", min_value=110.0, max_value=220.0, value=150.0)
X5 = st.number_input("Overall Height", min_value=3.0, max_value=7.0, value=3.5)
X6 = st.number_input("Orientation", min_value=2, max_value=5, value=3)
X7 = st.number_input("Glazing Area", min_value=0.0, max_value=0.4, value=0.2)
X8 = st.number_input("Glazing Area Distribution", min_value=0, max_value=5, value=3)

# Prediction
if st.button("Predict Energy Usage ⚙️"):
    features = np.array([[X1, X2, X3, X4, X5, X6, X7, X8]])
    prediction = model.predict(features)
    predicted_value = float(prediction[0][0])

    # --- Output card (electric blue styling) ---
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #001f3f, #004080);
        color: #00c6ff;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.6);
        ">
        <h2>Predicted Energy Consumption ⚡</h2>
        <h1 style="font-size:48px;">{predicted_value:.2f} kWh/m²</h1>
        <p style="color:#b3e5ff;">(Based on input parameters)</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Pie chart (blue energy feel) ---
    remaining = max(100 - predicted_value, 0)
    labels = ['Predicted Energy Use', 'Efficiency Reserve']
    values = [predicted_value, remaining]
    colors = ['#00c6ff', '#001f3f']

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'color':'white'})
    ax.set_facecolor("#0a0a0a")
    st.pyplot(fig)

    # --- Efficiency message ---
    if predicted_value < 20:
        st.success("🌱 *Excellent efficiency!* Your building design is highly energy-saving.")
    elif predicted_value < 35:
        st.info("💡 *Good efficiency.* A few improvements can reduce energy demand further.")
    else:
        st.warning("⚠️ *High energy usage detected.* Consider insulation and passive cooling.")

st.markdown("---")
st.caption("⚡ Designed with precision using Streamlit & Machine Learning")


