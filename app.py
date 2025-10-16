import streamlit as st
from joblib import load
import numpy as np
import matplotlib.pyplot as plt

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Energy Prediction 🚀", page_icon="⚡", layout="wide")

# ========== BACKGROUND IMAGE ==========
def add_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = f"data:image/jpg;base64,{data.encode('base64') if hasattr(data, 'encode') else st.image(data)}"
    page_bg = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/jpg;base64,{data.encode('base64') if hasattr(data, 'encode') else ''}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"], [data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0);
    }}
    .glass {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }}
    .result-card {{
        background: linear-gradient(135deg, rgba(0, 119, 255, 0.85), rgba(0, 255, 204, 0.8));
        color: white;
        border-radius: 15px;
        text-align: center;
        padding: 20px;
        margin-top: 30px;
        font-size: 20px;
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

add_bg("sss.jpg")

# ========== LOAD MODEL ==========
model = load("linear_regression_model.joblib")

# ========== HEADER ==========
st.markdown("<h1 style='text-align:center;color:#00FFD1;'>🏙️ Energy Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:white;'>Estimate building energy consumption based on environmental parameters.</p>", unsafe_allow_html=True)
st.write("")

# ========== INPUTS ==========
with st.container():
    st.markdown("<div class='glass'>", unsafe_allow_html=True)

    st.subheader("Enter Building Parameters:")
    X1 = st.number_input("🏗️ Relative Compactness", min_value=0.62, max_value=0.98, value=0.75)
    X2 = st.number_input("📐 Surface Area", min_value=514.0, max_value=808.0, value=600.0)
    X3 = st.number_input("🏠 Wall Area", min_value=294.0, max_value=416.0, value=350.0)
    X4 = st.number_input("🏢 Roof Area", min_value=110.0, max_value=220.0, value=150.0)
    X5 = st.number_input("📏 Overall Height", min_value=3.0, max_value=7.0, value=3.5)
    X6 = st.number_input("🧭 Orientation", min_value=2, max_value=5, value=3)
    X7 = st.number_input("🌞 Glazing Area", min_value=0.0, max_value=0.4, value=0.2)
    X8 = st.number_input("🪟 Glazing Area Distribution", min_value=0, max_value=5, value=3)

    st.markdown("</div>", unsafe_allow_html=True)

# ========== PREDICTION ==========
if st.button("🔮 Predict Energy Consumption"):
    features = np.array([[X1, X2, X3, X4, X5, X6, X7, X8]])
    prediction = model.predict(features)

    st.markdown(f"""
    <div class='result-card'>
        <h2>Predicted Energy Consumption</h2>
        <h1 style='font-size:45px;'>⚡ {prediction[0][0]:.2f} kWh</h1>
        <p>Estimated energy use per unit area based on input parameters.</p>
    </div>
    """, unsafe_allow_html=True)

    # Pie chart visualization
    fig, ax = plt.subplots()
    ax.pie([prediction[0][0], 100 - prediction[0][0] if prediction[0][0] <= 100 else 0],
           labels=['Predicted Energy', 'Remaining Capacity'],
           autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

st.caption("🌍 Designed with ❤️ using Streamlit | Energy Efficiency Dataset (UCI)")




