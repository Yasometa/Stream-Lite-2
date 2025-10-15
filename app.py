import streamlit as st
from joblib import load
import numpy as np
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Energy Prediction 🚀", page_icon="⚡", layout="centered")

# Custom background image & styling
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1503387762-592deb58ef4e');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
[data-testid="stSidebar"] {
    background-color: rgba(255,255,255,0.8);
}
div.stButton > button {
    background-color: #2e8b57;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}
div.stButton > button:hover {
    background-color: #3cb371;
    color: black;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Load model
model = load("linear_regression_model.joblib")

# App Title
st.title("⚡ Energy Prediction App")
st.write("Enter building characteristics to predict **energy consumption**:")

# Input fields
X1 = st.number_input("Relative Compactness", min_value=0.62, max_value=0.98, value=0.75)
X2 = st.number_input("Surface Area", min_value=514.0, max_value=808.0, value=600.0)
X3 = st.number_input("Wall Area", min_value=294.0, max_value=416.0, value=350.0)
X4 = st.number_input("Roof Area", min_value=110.0, max_value=220.0, value=150.0)
X5 = st.number_input("Overall Height", min_value=3.0, max_value=7.0, value=3.5)
X6 = st.number_input("Orientation", min_value=2, max_value=5, value=3)
X7 = st.number_input("Glazing Area", min_value=0.0, max_value=0.4, value=0.2)
X8 = st.number_input("Glazing Area Distribution", min_value=0, max_value=5, value=3)

# Prediction
if st.button("Predict Energy Consumption ⚙️"):
    features = np.array([[X1, X2, X3, X4, X5, X6, X7, X8]])
    prediction = model.predict(features)
    predicted_value = float(prediction[0][0])

    # Output card with style
    st.markdown(f"""
    <div style="
        background-color: rgba(255,255,255,0.85);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
        ">
        <h2 style="color:#2e8b57;">Predicted Energy Consumption ⚡</h2>
        <h1 style="color:#333;">{predicted_value:.2f} kWh/m²</h1>
    </div>
    """, unsafe_allow_html=True)

    # Create pie chart
    remaining = max(100 - predicted_value, 0)
    labels = ['Predicted Energy Use', 'Remaining Efficiency']
    values = [predicted_value, remaining]
    colors = ['#2e8b57', '#d3d3d3']

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')
    st.pyplot(fig)

    # Energy interpretation
    if predicted_value < 20:
        st.success("✅ Excellent energy efficiency!")
    elif predicted_value < 35:
        st.info("💡 Good efficiency, some improvement possible.")
    else:
        st.warning("⚠️ High energy usage detected — consider insulation or better materials.")

st.markdown("---")
st.caption("🌍 Designed with ❤️ using Streamlit & Machine Learning")

