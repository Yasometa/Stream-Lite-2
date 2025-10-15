import streamlit as st
from joblib import load
import numpy as np
import matplotlib.pyplot as plt

# Load trained model
model = load("linear_regression_model.joblib")

# --- PAGE CONFIG ---
st.set_page_config(page_title="Energy Prediction", page_icon="⚡", layout="centered")

# --- BACKGROUND IMAGE & STYLES ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1350&q=80");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
[data-testid="stHeader"], [data-testid="stToolbar"] {
    background: rgba(0,0,0,0);
}
h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- HEADER ---
st.title("⚡ Energy Prediction 🚀")
st.markdown("### Estimate building energy consumption (kWh/m²)")
st.caption("Built with Machine Learning — visualize your building's energy efficiency.")

# --- INPUT FIELDS ---
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

# --- PREDICTION ---
if st.button("🔮 Predict Energy Consumption"):
    features = np.array([[X1, X2, X3, X4, X5, X6, X7, X8]])
    prediction = model.predict(features)[0][0]

    # --- OUTPUT CARD (transparent glass-style) ---
    st.markdown(
        f"""
        <div style="background:rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        padding:25px;border-radius:20px;text-align:center;
        box-shadow:0px 4px 20px rgba(0,0,0,0.3);margin-top:25px;">
            <h2 style="color:#ffffff;">Predicted Energy Consumption</h2>
            <h1 style="color:#00eaff;font-size:52px;">{prediction:.2f} kWh/m²</h1>
            <p style="color:#e0e0e0;">Lower values = higher efficiency 🌿</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- PIE CHART ---
    fig, ax = plt.subplots(figsize=(4, 4))
    data = [prediction, 100 - prediction if prediction < 100 else 0]
    labels = ['Predicted Energy', 'Remaining (to 100)']
    colors = ['#00eaff', '#1a1a1a']
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')
    st.pyplot(fig)

    # --- CONDITIONAL MESSAGE ---
    if prediction <= 25:
        st.success("✅ Excellent Efficiency! Your building is very energy-efficient.")
    elif prediction <= 50:
        st.info("ℹ️ Moderate Efficiency. Consider optimizing insulation or glazing.")
    else:
        st.warning("⚠️ High Energy Usage! Consider design changes for better performance.")

# --- FOOTER ---
st.markdown("---")
st.caption("🌍 Designed with ❤️ using Str
