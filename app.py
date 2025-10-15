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
    background-image: url('https://images.unsplash.com/photo-1509395176047-4a66953fd231');
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
X2 = st.number_input("Surface Area", min_
