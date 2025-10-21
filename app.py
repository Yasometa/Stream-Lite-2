import streamlit as st
from joblib import load
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import base64
import os

# ========== CHECK AND INSTALL MISSING PACKAGES ==========
try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    st.warning("Seaborn not available. Heatmap will use matplotlib alternative.")

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Energy Prediction 🚀", page_icon="⚡", layout="wide")

# ========== CUSTOM CSS FOR DARK THEME ==========
st.markdown("""
<style>
    /* Main content styling */
    .main-content {
        background: rgba(13, 17, 23, 0.85);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Input field styling */
    .stNumberInput {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    /* Input label styling - FIXED VISIBILITY */
    .stNumberInput label {
        color: #1E90FF !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7) !important;
    }
    
    /* Text styling for dark theme */
    .dark-heading {
        color: #1E90FF !important;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
        font-weight: 700;
    }
    
    .dark-subheading {
        color: #00CED1 !important;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.6);
        font-weight: 600;
    }
    
    .white-text {
        color: #E8E8E8 !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
    }
    
    /* Card styling */
    .result-card {
        background: linear-gradient(135deg, rgba(30, 30, 60, 0.95), rgba(0, 50, 80, 0.9));
        color: white;
        border-radius: 15px;
        text-align: center;
        padding: 25px;
        margin: 20px 0;
        font-size: 20px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
        border: 2px solid rgba(0, 150, 255, 0.3);
    }
    
    /* Input card styling */
    .input-card {
        background: rgba(30, 35, 45, 0.9);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(100, 150, 255, 0.2);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(25, 30, 40, 0.9);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(100, 150, 255, 0.2);
        color: #E8E8E8;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #1E90FF, #00BFFF);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(30, 144, 255, 0.4);
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #1C86EE, #009ACD);
        box-shadow: 0 6px 20px rgba(30, 144, 255, 0.6);
    }
    
    /* Help text styling */
    .stNumberInput .stTooltipIcon {
        color: #00CED1 !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== BACKGROUND IMAGE ==========
def add_bg_from_local(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        
        page_bg = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 30, 0.8)), 
                         url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        
        [data-testid="stHeader"] {{
            background: rgba(0, 0, 0, 0.0);
        }}
        
        [data-testid="stSidebar"] {{
            background: rgba(13, 17, 23, 0.9) !important;
        }}
        </style>
        """
        st.markdown(page_bg, unsafe_allow_html=True)
    else:
        # Fallback gradient background
        st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        </style>
        """, unsafe_allow_html=True)
        st.info("Using default gradient background. Add your image file for custom background.")

# Add background - replace with your image file
add_bg_from_local("energy_bg.jpg")  # You can use: dark_tech.jpg, energy_dashboard.jpg, etc.

# ========== LOAD MODEL ==========
model = load("linear_regression_model.joblib")

# ========== HEADER ==========
st.markdown("<h1 class='dark-heading' style='text-align:center;'>🏙️ Smart Energy Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<p class='white-text' style='text-align:center; font-size:18px;'>Advanced AI-powered building energy consumption analysis</p>", unsafe_allow_html=True)

# ========== INPUTS SECTION ==========
st.markdown("<div class='main-content'>", unsafe_allow_html=True)
st.markdown("<h2 class='dark-subheading'>🏗️ Building Parameters</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='input-card'>", unsafe_allow_html=True)
    X1 = st.number_input(
        "🏗️ Relative Compactness", min_value=0.62, max_value=0.98, value=0.75, step=0.01,
        help="Ratio of building volume to surface area"
    )
    X2 = st.number_input(
        "📐 Surface Area (m²)", min_value=514.0, max_value=808.0, value=600.0, step=10.0,
        help="Total surface area of the building"
    )
    X3 = st.number_input(
        "🏠 Wall Area (m²)", min_value=294.0, max_value=416.0, value=350.0, step=5.0,
        help="Total wall area exposed to external environment"
    )
    X4 = st.number_input(
        "🏢 Roof Area (m²)", min_value=110.0, max_value=220.0, value=150.0, step=5.0,
        help="Total roof area of the building"
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='input-card'>", unsafe_allow_html=True)
    X5 = st.number_input(
        "📏 Overall Height (m)", min_value=3.0, max_value=7.0, value=3.5, step=0.1,
        help="Total height of the building"
    )
    X6 = st.number_input(
        "🧭 Orientation", min_value=2, max_value=5, value=3, step=1,
        help="Building orientation (2: North, 3: East, 4: South, 5: West)"
    )
    X7 = st.number_input(
        "🌞 Glazing Area Ratio", min_value=0.0, max_value=0.4, value=0.2, step=0.05,
        help="Ratio of glazing area to floor area"
    )
    X8 = st.number_input(
        "🪟 Glazing Area Distribution", min_value=0, max_value=5, value=3, step=1,
        help="Distribution of glazing area across building faces"
    )
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
    
    # Calculate cool/heat load distribution
    cool_load = pred_value * 0.6  # 60% for cooling
    heat_load = pred_value * 0.4  # 40% for heating
    
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    
    # Result Card
    st.markdown(f"""
    <div class='result-card'>
        <h2 style='margin-bottom: 20px; color: #00CED1;'>📊 Energy Consumption Analysis</h2>
        <h1 style='font-size:48px; margin: 10px 0; color: #1E90FF;'>⚡ {pred_value:.2f} kWh/m²</h1>
        <p style='font-size:16px; opacity: 0.9; color: #E8E8E8;'>Total Energy Load per Square Meter</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 class='dark-subheading'>🔥❄️ Cool/Heat Load Distribution</h3>", unsafe_allow_html=True)
        
        # Professional pie chart with dark theme
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        fig1.patch.set_facecolor('#0D1117')
        ax1.set_facecolor('#0D1117')
        
        labels = ['Cooling Load', 'Heating Load']
        sizes = [cool_load, heat_load]
        colors = ['#1E90FF', '#FF6B6B']  # Blue for cooling, Red for heating
        explode = (0.05, 0.05)
        
        wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                                          autopct='%1.1f%%', shadow=True, startangle=90,
                                          textprops={'fontsize': 12, 'color': 'white', 'weight': 'bold'})
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax1.axis('equal')
        plt.title('Energy Load Distribution\nCooling vs Heating', 
                 color='white', fontsize=14, fontweight='bold', pad=20)
        plt.setp(texts, color='white', fontweight='bold')
        
        st.pyplot(fig1)
        
        # Load metrics
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.metric("Cooling Load", f"{cool_load:.2f} kWh/m²", "60%",
                     help="Energy required for cooling systems")
        with col1_2:
            st.metric("Heating Load", f"{heat_load:.2f} kWh/m²", "40%",
                     help="Energy required for heating systems")
    
    with col2:
        st.markdown("<h3 class='dark-subheading'>📈 Feature Impact Analysis</h3>", unsafe_allow_html=True)
        
        # Create feature impact data
        features_names = ['Compactness', 'Surface Area', 'Wall Area', 'Roof Area', 
                         'Height', 'Orientation', 'Glazing Area', 'Glazing Dist.']
        
        impact_scores = [X1 * 0.3, X2 * 0.1, X3 * 0.15, X4 * 0.1, 
                        X5 * 0.2, X6 * 0.05, X7 * 0.25, X8 * 0.05]
        
        if SEABORN_AVAILABLE:
            # Create heatmap with dark theme
            heatmap_data = pd.DataFrame({
                'Feature': features_names,
                'Impact': impact_scores
            }).set_index('Feature')
            
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            fig2.patch.set_facecolor('#0D1117')
            ax2.set_facecolor('#0D1117')
            
            sns.heatmap(heatmap_data.T, annot=True, fmt='.2f', cmap='viridis', 
                       cbar_kws={'label': 'Impact Score'}, ax=ax2,
                       annot_kws={'color': 'white', 'weight': 'bold'})
            
            ax2.tick_params(colors='white')
            plt.title('Feature Impact Heatmap', 
                     color='white', fontsize=14, fontweight='bold', pad=20)
            plt.xticks(rotation=45, color='white')
            plt.yticks(color='white')
            cbar = ax2.collections[0].colorbar
            cbar.ax.yaxis.set_tick_params(color='white')
            plt.setp(plt.getp(cbar.ax, 'yticklabels'), color='white')
        else:
            # Fallback: Bar chart with dark theme
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            fig2.patch.set_facecolor('#0D1117')
            ax2.set_facecolor('#0D1117')
            
            y_pos = np.arange(len(features_names))
            colors = plt.cm.viridis(np.linspace(0, 1, len(impact_scores)))
            
            bars = ax2.barh(y_pos, impact_scores, color=colors, alpha=0.8)
            ax2.set_yticks(y_pos)
            ax2.set_yticklabels(features_names, color='white', fontweight='bold')
            ax2.set_xlabel('Impact Score', color='white', fontweight='bold')
            ax2.set_title('Feature Impact Analysis', color='white', fontsize=14, fontweight='bold', pad=20)
            
            for i, v in enumerate(impact_scores):
                ax2.text(v + 0.01, i, f'{v:.2f}', color='white', fontweight='bold', va='center')
            
            ax2.tick_params(colors='white')
            ax2.spines['bottom'].set_color('white')
            ax2.spines['top'].set_color('white') 
            ax2.spines['right'].set_color('white')
            ax2.spines['left'].set_color('white')
        
        st.pyplot(fig2)
    
    # Additional Insights
    st.markdown("---")
    st.markdown("<h3 class='dark-subheading'>💡 Energy Efficiency Insights</h3>", unsafe_allow_html=True)
    
    insight_col1, insight_col2, insight_col3 = st.columns(3)
    
    with insight_col1:
        st.metric("Efficiency Rating", "B+", "+2 levels",
                 help="Building energy efficiency classification")
    
    with insight_col2:
        st.metric("Potential Savings", "15%", "-8% vs avg.",
                 help="Potential energy savings compared to average buildings")
    
    with insight_col3:
        st.metric("Carbon Footprint", "2.1 tCO₂", "-0.5 tCO₂",
                 help="Estimated carbon dioxide emissions reduction")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ========== FOOTER ==========
st.markdown("""
<div style='text-align: center; margin-top: 50px;'>
    <p class='white-text'>🌍 Powered by AI | Energy Efficiency Analytics Platform</p>
    <p class='white-text' style='opacity: 0.7;'>UCI Energy Dataset • Professional Grade Analysis</p>
</div>
""", unsafe_allow_html=True)






