import streamlit as st
from joblib import load
import numpy as np
import matplotlib.pyplot as plt

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="Smart Energy Prediction ⚡", page_icon="🏙️", layout="centered")

# --- Background: futuristic smart-energy theme ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1603791440384-56cd371ee9a7?auto=format&fit=crop&w=1600&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    backdrop-filter: blur(3px);
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
div.stButton > button {
    background: linear-gradient(90deg, #00c6ff, #007bff);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #007bff, #00c6ff);
    color: black;
}
.card {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.3);
}
.stNumberInput input {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 8px;
    padding: 8px;
    color: #000;
    font-weight: 500;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ----------------- MODEL LOAD -----------------
model = load("linear_regression_model.joblib")

# ----------------- TITLE -----------------
st.markdown("<h1 style='text-align:center;color:#00eaff;'>🏙️ Smart Energy Consumption Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:white;'>AI-powered analysis for sustainable building design ⚡</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ----------------- INPUT FORM (Glass Card) -----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
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
st.markdown("</div>", unsafe_allow_html=True)

# ----------------- PREDICTION -----------------
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔍 Predict Energy Consumption"):
    features = np.array([[X1, X2, X3, X4, X5, X6, X7, X8]])
    prediction = model.predict(features)
    predicted_value = float(prediction[0][0])

    # --- Output (Glass card with glow) ---
    st.markdown(f"""
    <div class="card" style="text-align:center; color:#00eaff;">
        <h2>Predicted Energy Consumption ⚡</h2>
        <h1 style="font-size:48px; color:#66d9ff;">{predicted_value:.2f} kWh/m²</h1>
        <p style="color:#b3e5ff;">AI estimation based on structural design parameters</p>
    </div>
    """, unsafe_allow_html=True)

    # --- PIE CHART ---
    remaining = max(100 - predicted_value, 0)
    labels = ['Predicted Energy Use', 'Potential Efficiency']
    values = [predicted_value, remaining]
    colors = ['#00c6ff', '#004477']

    fig, ax = plt.subplots()
    fig.patch.set_facecolor("none")
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'color': 'white'})
    ax.set_facecolor("none")
    st.pyplot(fig)

    # --- Status message ---
    if predicted_value < 20:
        st.success("🌱 Excellent! Your building is highly energy-efficient.")
    elif predicted_value < 35:
        st.info("💡 Good performance — minor optimization possible.")
    else:
        st.warning("⚠️ High energy use detected — review insulation and glazing design.")

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("💠 Powered by Streamlit | Smart Energy Modeling System")


