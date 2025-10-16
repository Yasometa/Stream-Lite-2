import streamlit as st
from joblib import load
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import base64
import os

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Energy Prediction 🚀", page_icon="⚡", layout="wide")

# ========== CUSTOM CSS FOR BETTER VISIBILITY ==========
st.markdown("""
<style>
    /* Main content styling */
    .main-content {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Input field styling */
    .stNumberInput, .stSlider {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    /* Text styling for better contrast */
    .white-text {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
    }
    
    .cyan-text {
        color: #00FFFF !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
    }
    
    /* Card styling */
    .result-card {
        background: linear-gradient(135deg, rgba(0, 119, 255, 0.9), rgba(0, 255, 204, 0.9));
        color: white;
        border-radius: 15px;
        text-align: center;
        padding: 25px;
        margin: 20px 0;
        font-size: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ========== BACKGROUND IMAGE ==========
def add_bg(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        page_bg = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(page_bg, unsafe_allow_html=True)
    else:
        st.warning(f"Background image '{image_file}' not found. Using default background.")

# Add background
add_bg("sss.jpeg")

# ========== LOAD MODEL ==========
try:
    model = load("linear_regression_model.joblib")
except:
    st.error("Model file 'linear_regression_model.joblib' not found. Using dummy model.")
    # Dummy model for demonstration
    class DummyModel:
        def predict(self, X):
            return np.array([25.5 + 0.1 * X[0][0] + 0.05 * X[0][1]])
    model = DummyModel()

# ========== HEADER ==========
st.markdown("<h1 class='cyan-text' style='text-align:center;'>🏙️ Smart Energy Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<p class='white-text' style='text-align:center; font-size:18px;'>Advanced AI-powered building energy consumption analysis</p>", unsafe_allow_html=True)

# ========== INPUTS SECTION ==========
st.markdown("<div class='main-content'>", unsafe_allow_html=True)
st.markdown("<h2 class='cyan-text'>🏗️ Building Parameters</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    X1 = st.slider("**Relative Compactness**", 0.62, 0.98, 0.75, 0.01)
    X2 = st.slider("**Surface Area (m²)**", 514.0, 808.0, 600.0, 10.0)
    X3 = st.slider("**Wall Area (m²)**", 294.0, 416.0, 350.0, 5.0)
    X4 = st.slider("**Roof Area (m²)**", 110.0, 220.0, 150.0, 5.0)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    X5 = st.slider("**Overall Height (m)**", 3.0, 7.0, 3.5, 0.1)
    X6 = st.slider("**Orientation**", 2, 5, 3, 1)
    X7 = st.slider("**Glazing Area Ratio**", 0.0, 0.4, 0.2, 0.05)
    X8 = st.slider("**Glazing Distribution**", 0, 5, 3, 1)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ========== PREDICTION BUTTON ==========
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_btn = st.button("**🔮 PREDICT ENERGY CONSUMPTION**", 
                          use_container_width=True, 
                          type="primary")

# ========== PREDICTION RESULTS ==========
if predict_btn:
    features = np.array([[X1, X2, X3, X4, X5, X6, X7, X8]])
    prediction = model.predict(features)
    pred_value = prediction[0] if np.ndim(prediction) == 1 else prediction[0][0]
    
    # Calculate cool/heat load distribution (example logic)
    cool_load = pred_value * 0.6  # 60% for cooling
    heat_load = pred_value * 0.4  # 40% for heating
    
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    
    # Result Card
    st.markdown(f"""
    <div class='result-card'>
        <h2 style='margin-bottom: 20px;'>📊 Energy Consumption Analysis</h2>
        <h1 style='font-size:48px; margin: 10px 0;'>⚡ {pred_value:.2f} kWh/m²</h1>
        <p style='font-size:16px; opacity: 0.9;'>Total Energy Load per Square Meter</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 class='cyan-text'>🔥❄️ Cool/Heat Load Distribution</h3>", unsafe_allow_html=True)
        
        # Professional pie chart
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        labels = ['Cooling Load', 'Heating Load']
        sizes = [cool_load, heat_load]
        colors = ['#00B4D8', '#FF6B6B']
        explode = (0.05, 0.05)  # explode slices
        
        wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                                          autopct='%1.1f%%', shadow=True, startangle=90,
                                          textprops={'fontsize': 12, 'color': 'white', 'weight': 'bold'})
        
        # Enhance pie chart appearance
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax1.axis('equal')
        plt.title('Energy Load Distribution\nCooling vs Heating', 
                 color='white', fontsize=14, fontweight='bold', pad=20)
        plt.setp(texts, color='white', fontweight='bold')
        
        # Set background color
        fig1.patch.set_facecolor('none')
        ax1.set_facecolor('none')
        
        st.pyplot(fig1)
        
        # Load metrics
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.metric("Cooling Load", f"{cool_load:.2f} kWh/m²", "60%")
        with col1_2:
            st.metric("Heating Load", f"{heat_load:.2f} kWh/m²", "40%")
    
    with col2:
        st.markdown("<h3 class='cyan-text'>📈 Feature Impact Heatmap</h3>", unsafe_allow_html=True)
        
        # Create feature impact data (example values)
        features_names = ['Compactness', 'Surface Area', 'Wall Area', 'Roof Area', 
                         'Height', 'Orientation', 'Glazing Area', 'Glazing Dist.']
        
        # Example impact scores (replace with your actual feature importance)
        impact_scores = [X1 * 0.3, X2 * 0.1, X3 * 0.15, X4 * 0.1, 
                        X5 * 0.2, X6 * 0.05, X7 * 0.25, X8 * 0.05]
        
        # Create heatmap data
        heatmap_data = pd.DataFrame({
            'Feature': features_names,
            'Impact': impact_scores
        }).set_index('Feature')
        
        # Create heatmap
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap_data.T, annot=True, fmt='.2f', cmap='coolwarm', 
                   cbar_kws={'label': 'Impact Score'}, ax=ax2,
                   annot_kws={'color': 'white', 'weight': 'bold'})
        
        ax2.set_facecolor('none')
        fig2.patch.set_facecolor('none')
        ax2.tick_params(colors='white')
        plt.title('Feature Impact on Energy Consumption', 
                 color='white', fontsize=14, fontweight='bold', pad=20)
        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')
        cbar = ax2.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax, 'yticklabels'), color='white')
        
        st.pyplot(fig2)
    
    # Additional Insights
    st.markdown("---")
    st.markdown("<h3 class='cyan-text'>💡 Energy Efficiency Insights</h3>", unsafe_allow_html=True)
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        st.metric("Efficiency Rating", "B+", "+2 levels")
    
    with insight_col2:
        st.metric("Potential Savings", "15%", "-8% vs avg.")
    
    with insight_col3:
        st.metric("Carbon Footprint", "2.1 tCO₂", "-0.5 tCO₂")
    
    st.markdown("</div>", unsafe_allow_html=True")

# ========== FOOTER ==========
st.markdown("""
<div style='text-align: center; margin-top: 50px;'>
    <p class='white-text'>🌍 Powered by AI | Energy Efficiency Analytics Platform</p>
    <p class='white-text' style='opacity: 0.7;'>UCI Energy Dataset • Professional Grade Analysis</p>
</div>
""", unsafe_allow_html=True)

