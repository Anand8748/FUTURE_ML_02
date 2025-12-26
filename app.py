"""
Spotify Churn Prediction System - Streamlit Web Application
Modern, interactive web app for churn prediction and analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Spotify Churn Prediction System",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern design
st.markdown("""
    <style>
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Hide sidebar toggle button */
    [data-testid="stHeader"] [data-testid="stDecoration"] {
        display: none;
    }
    
    /* Navigation Bar Styles */
    .navbar {
        background: linear-gradient(90deg, #1DB954 0%, #1ed760 100%);
        padding: 1rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .navbar-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .navbar-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        text-decoration: none;
    }
    .spotify-logo {
        height: 60px;
        width: 60px;
        object-fit: contain;
        flex-shrink: 0;
    }
    .navbar-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 1.8rem;
        font-weight: 700;
        color: white;
        text-decoration: none;
    }
    .navbar-nav {
        display: flex;
        gap: 1.5rem;
        list-style: none;
        margin: 0;
        padding: 0;
    }
    .nav-item {
        display: inline-block;
    }
    .nav-link {
        color: white;
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: all 0.3s;
    }
    .nav-link:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .navbar-container {
            flex-direction: column;
            gap: 1rem;
        }
        .navbar-brand {
            font-size: 1.5rem;
        }
        .navbar-nav {
            flex-wrap: wrap;
            justify-content: center;
            gap: 0.5rem;
        }
        .hero-title {
            font-size: 2rem;
        }
        .hero-subtitle {
            font-size: 1rem;
        }
        .hero-section {
            height: 400px;
        }
        .section-title {
            font-size: 1.8rem !important;
        }
        .section-subtitle {
            font-size: 1rem !important;
        }
        .feature-card {
            padding: 1.5rem !important;
            margin-bottom: 1rem;
        }
        .feature-title {
            font-size: 1.2rem !important;
        }
        .stat-card {
            padding: 1.5rem !important;
        }
        .stat-number {
            font-size: 2rem !important;
        }
        .video-container {
            height: 300px !important;
        }
        .video-container video {
            height: 300px !important;
        }
        .sub-header {
            font-size: 1.2rem !important;
        }
        .prediction-box {
            padding: 1.5rem !important;
        }
        .prediction-box h1 {
            font-size: 2rem !important;
        }
    }
    
    @media (max-width: 480px) {
        .section-title {
            font-size: 1.5rem !important;
        }
        .feature-card {
            padding: 1rem !important;
        }
        .stat-card {
            padding: 1rem !important;
        }
        .stat-number {
            font-size: 1.5rem !important;
        }
        .video-container {
            height: 250px !important;
        }
        .video-container video {
            height: 250px !important;
        }
        .prediction-box h1 {
            font-size: 1.5rem !important;
        }
    }
    
    /* Ensure Streamlit columns are responsive */
    @media (max-width: 768px) {
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    
    /* Video Section Styles */
    .video-container {
        width: 100%;
        height: 650px;
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    .video-container video {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 15px;
    }
    /* Hide ALL video controls - no progress bar, time, menu, or any controls */
    .video-container video::-webkit-media-controls {
        display: none !important;
    }
    .video-container video::-webkit-media-controls-enclosure {
        display: none !important;
    }
    .video-container video::-webkit-media-controls-panel {
        display: none !important;
    }
    .video-container video::-webkit-media-controls-play-button {
        display: none !important;
    }
    .video-container video::-webkit-media-controls-timeline {
        display: none !important;
    }
    .video-container video::-webkit-media-controls-current-time-display {
        display: none !important;
    }
    .video-container video::-webkit-media-controls-time-remaining-display {
        display: none !important;
    }
    .video-container video::-webkit-media-controls-mute-button {
        display: none !important;
    }
    .video-container video::-webkit-media-controls-volume-slider {
        display: none !important;
    }
    .video-container video::-webkit-media-controls-fullscreen-button {
        display: none !important;
    }
    .video-container video::-webkit-media-controls-overlay-play-button {
        display: none !important;
    }
    
    /* Professional Home Page Styles */
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 3rem 0 1.5rem 0;
        color: #1a1a1a;
    }
    .section-subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s, box-shadow 0.3s;
        height: 100%;
        border: 1px solid #f0f0f0;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(29, 185, 84, 0.15);
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    .feature-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }
    .feature-description {
        color: #666;
        line-height: 1.6;
        font-size: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 20px rgba(29, 185, 84, 0.2);
        transition: transform 0.3s;
    }
    .stat-card:hover {
        transform: scale(1.05);
    }
    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    .cta-button {
        background: linear-gradient(90deg, #1DB954, #1ed760);
        color: white;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
        text-decoration: none;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(29, 185, 84, 0.3);
    }
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(29, 185, 84, 0.4);
    }
    .benefit-item {
        display: flex;
        align-items: start;
        gap: 1rem;
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1DB954;
    }
    .benefit-icon {
        font-size: 2rem;
        flex-shrink: 0;
    }
    .benefit-content h4 {
        margin: 0 0 0.5rem 0;
        color: #1a1a1a;
        font-size: 1.2rem;
    }
    .benefit-content p {
        margin: 0;
        color: #666;
        line-height: 1.6;
    }
    .how-it-works-step {
        text-align: center;
        padding: 2rem;
    }
    .step-number {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #1DB954, #1ed760);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 auto 1rem;
    }
    .step-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .step-description {
        color: #666;
        line-height: 1.6;
    }
    
    /* Professional Footer Styles - Icons Only */
    .footer {
        background: rgba(0, 0, 0, 0.05);
        color: #333;
        padding: 2rem 2rem 1.5rem;
        margin-top: 4rem;
        border-top: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
        width: 100%;
        position: relative;
    }
    .footer-icons-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1.5rem;
        max-width: 1200px;
        margin: 0 auto 1rem;
    }
    .footer-copyright-text {
        text-align: center;
        font-size: 0.85rem;
        color: #666;
        margin-top: 1rem;
        padding-top: 0;
        border-top: none;
    }
    .footer-copyright-text strong {
        color: #1DB954;
        font-weight: 600;
    }
    .social-link-item {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(255, 255, 255, 0.1);
        color: #e0e0e0;
        text-decoration: none;
        transition: all 0.3s ease;
        cursor: pointer;
        pointer-events: auto;
        position: relative;
        z-index: 10;
    }
    .social-link-item:hover {
        background: rgba(29, 185, 84, 0.2);
        border-color: #1DB954;
        transform: translateY(-3px);
        color: #1DB954;
        box-shadow: 0 5px 20px rgba(29, 185, 84, 0.4);
    }
    .social-icon {
        width: 24px;
        height: 24px;
        fill: currentColor;
        transition: transform 0.3s ease;
    }
    .social-link-item:hover .social-icon {
        transform: scale(1.15);
    }
    @media (max-width: 768px) {
        .footer {
            padding: 1.5rem 1rem;
        }
        .footer-icons-container {
            gap: 1rem;
        }
        .social-link-item {
            width: 45px;
            height: 45px;
        }
        .social-icon {
            width: 22px;
            height: 22px;
        }
        /* Navigation buttons responsive */
        div[data-testid="column"] button[kind="secondary"] {
            font-size: 0.85rem !important;
            padding: 0.4rem 0.8rem !important;
        }
        /* Form columns stack on mobile */
        [data-testid="column"] {
            width: 100% !important;
        }
    }
    
    @media (max-width: 480px) {
        div[data-testid="column"] button[kind="secondary"] {
            font-size: 0.75rem !important;
            padding: 0.3rem 0.6rem !important;
        }
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1DB954, #1ed760);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1DB954;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(90deg, #1DB954, #1ed760);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(29, 185, 84, 0.4);
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    .high-risk {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .low-risk {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load the original dataset"""
    try:
        df = pd.read_excel('Spotify_data.xlsx')
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        return None

@st.cache_resource
def load_model():
    """Load the trained model"""
    try:
        with open('best_churn_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

@st.cache_resource
def load_preprocessor():
    """Load the preprocessor"""
    try:
        with open('preprocessor.pkl', 'rb') as f:
            preprocessor = pickle.load(f)
        return preprocessor
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading preprocessor: {str(e)}")
        return None

def preprocess_user_input(user_input, preprocessor, feature_names):
    """Preprocess user input for prediction"""
    from sklearn.preprocessing import LabelEncoder
    import numpy as np
    
    try:
        # Create a DataFrame from user input
        df_input = pd.DataFrame([user_input])
        
        # Create a new DataFrame with all features initialized to 0
        processed_input = pd.DataFrame(0, index=[0], columns=feature_names)
        
        # Process each column from user input
        for col in df_input.columns:
            if col in feature_names:
                if col in preprocessor['label_encoders']:
                    # Categorical feature - encode it
                    le = preprocessor['label_encoders'][col]
                    input_value = str(df_input[col].iloc[0])
                    le_classes_str = [str(c) for c in le.classes_]
                    
                    # Handle unseen categories
                    if input_value in le_classes_str:
                        # Find the original class value
                        original_value = le.classes_[le_classes_str.index(input_value)]
                        processed_input[col] = le.transform([original_value])[0]
                    else:
                        # Use first class (most common) as default
                        processed_input[col] = le.transform([le.classes_[0]])[0]
                else:
                    # Numeric feature - convert to numeric
                    try:
                        numeric_value = pd.to_numeric(df_input[col].iloc[0], errors='coerce')
                        if pd.notna(numeric_value):
                            processed_input[col] = numeric_value
                        else:
                            processed_input[col] = 0
                    except (ValueError, TypeError, IndexError):
                        processed_input[col] = 0
        
        # Ensure all values are numeric
        processed_input = processed_input.apply(pd.to_numeric, errors='coerce').fillna(0)
        
        # Verify feature count matches
        if len(processed_input.columns) != len(feature_names):
            raise ValueError(f"Feature count mismatch: expected {len(feature_names)}, got {len(processed_input.columns)}")
        
        # Scale features
        df_input_scaled = preprocessor['scaler'].transform(processed_input)
        
        return df_input_scaled
    
    except Exception as e:
        # Log error for debugging
        import traceback
        print(f"Preprocessing error: {str(e)}")
        print(traceback.format_exc())
        # Return zeros if preprocessing fails
        return np.zeros((1, len(feature_names)))

def create_navbar():
    """Create navigation bar in header"""
    import os
    import base64
    
    # Try to load Spotify logo - prioritize spotify_image.png
    logo_paths = ['spotify_image.png', 'spotify.png', 'spotify_logo.png', 'spotify-logo.png', 'logo.png']
    logo_path = None
    
    for path in logo_paths:
        if os.path.exists(path):
            logo_path = path
            break
    
    # Create logo HTML - Spotify icon
    if logo_path:
        try:
            with open(logo_path, "rb") as img_file:
                logo_base64 = base64.b64encode(img_file.read()).decode()
            img_ext = logo_path.split('.')[-1].lower()
            mime_type = f"image/{img_ext}" if img_ext in ['png', 'jpg', 'jpeg', 'svg'] else "image/png"
            logo_html = f'<img src="data:{mime_type};base64,{logo_base64}" style="height: 60px; width: 60px; object-fit: contain; background: transparent; background-color: transparent;" alt="Spotify Logo">'
        except Exception as e:
            # Fallback to Spotify SVG icon
            logo_html = '<svg style="height: 60px; width: 60px; fill: white;" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.1 5.16 9.141c-.6.18-1.2-.18-1.38-.72-.18-.6.18-1.2.72-1.38 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.42 1.56-.299.421-1.02.599-1.559.3z"/></svg>'
    else:
        # Use Spotify SVG icon if no image file found
        logo_html = '<svg style="height: 60px; width: 60px; fill: white;" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.1 5.16 9.141c-.6.18-1.2-.18-1.38-.72-.18-.6.18-1.2.72-1.38 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.42 1.56-.299.421-1.02.599-1.559.3z"/></svg>'
    
    # Create visible navbar header with logo, brand, and navigation (responsive)
    st.markdown(f"""
    <div class="header-container" style="background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%); padding: 1rem 2rem; border-radius: 10px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <div style="display: flex; align-items: center; justify-content: center; gap: 1.5rem; flex-wrap: wrap;">
            {logo_html}
            <span class="header-title" style="font-size: 2.5rem; font-weight: 700; color: white; text-align: center;">Spotify Churn Prediction</span>
        </div>
    </div>
    <style>
    @media (max-width: 768px) {{
        .header-container {{
            padding: 0.75rem 1rem !important;
        }}
        .header-title {{
            font-size: 1.5rem !important;
        }}
        .header-container img, .header-container svg {{
            height: 80px !important;
            width: 80px !important;
        }}
    }}
    @media (max-width: 480px) {{
        .header-title {{
            font-size: 1.2rem !important;
        }}
        .header-container img, .header-container svg {{
            height: 60px !important;
            width: 60px !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # Create navigation buttons using Streamlit (for functionality)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Home", key="nav_home", use_container_width=True):
            st.session_state.nav_page = "Home"
            st.rerun()
    
    with col2:
        if st.button("Predict Churn", key="nav_predict", use_container_width=True):
            st.session_state.nav_page = "Predict Churn"
            st.rerun()
    
    with col3:
        if st.button("Analytics Dashboard", key="nav_analytics", use_container_width=True):
            st.session_state.nav_page = "Analytics Dashboard"
            st.rerun()
    
    with col4:
        if st.button("Model Performance", key="nav_performance", use_container_width=True):
            st.session_state.nav_page = "Model Performance"
            st.rerun()
    
    # Style the navigation buttons with different colors using JavaScript
    st.markdown("""
    <style>
    /* Base styles for all navigation buttons - Professional Design */
    div[data-testid="column"] button[kind="secondary"] {
        border-radius: 8px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.3px !important;
        text-transform: none !important;
    }
    </style>
    <script>
    // Function to style navigation buttons by text content with professional colors
    function styleNavButtons() {
        const buttons = document.querySelectorAll('button[kind="secondary"]');
        buttons.forEach(function(btn) {
            const text = btn.textContent.trim();
            if (text === 'Home') {
                // Professional Sky Blue - welcoming and modern
                btn.style.background = 'linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%)';
                btn.style.color = '#0ea5e9';
                btn.style.border = '2px solid #0ea5e9';
                btn.style.boxShadow = '0 2px 8px rgba(14, 165, 233, 0.2)';
                btn.addEventListener('mouseenter', function() {
                    this.style.background = 'linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%)';
                    this.style.color = 'white';
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 4px 12px rgba(14, 165, 233, 0.4)';
                });
                btn.addEventListener('mouseleave', function() {
                    this.style.background = 'linear-gradient(135deg, rgba(14, 165, 233, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%)';
                    this.style.color = '#0ea5e9';
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = '0 2px 8px rgba(14, 165, 233, 0.2)';
                });
            } else if (text === 'Predict Churn') {
                // Professional Amber/Orange - attention-grabbing but sophisticated
                btn.style.background = 'linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(251, 146, 60, 0.15) 100%)';
                btn.style.color = '#f59e0b';
                btn.style.border = '2px solid #f59e0b';
                btn.style.boxShadow = '0 2px 8px rgba(245, 158, 11, 0.2)';
                btn.addEventListener('mouseenter', function() {
                    this.style.background = 'linear-gradient(135deg, #f59e0b 0%, #fb923c 100%)';
                    this.style.color = 'white';
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 4px 12px rgba(245, 158, 11, 0.4)';
                });
                btn.addEventListener('mouseleave', function() {
                    this.style.background = 'linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(251, 146, 60, 0.15) 100%)';
                    this.style.color = '#f59e0b';
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = '0 2px 8px rgba(245, 158, 11, 0.2)';
                });
            } else if (text === 'Analytics Dashboard') {
                // Professional Indigo - analytical and trustworthy
                btn.style.background = 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%)';
                btn.style.color = '#6366f1';
                btn.style.border = '2px solid #6366f1';
                btn.style.boxShadow = '0 2px 8px rgba(99, 102, 241, 0.2)';
                btn.addEventListener('mouseenter', function() {
                    this.style.background = 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)';
                    this.style.color = 'white';
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 4px 12px rgba(99, 102, 241, 0.4)';
                });
                btn.addEventListener('mouseleave', function() {
                    this.style.background = 'linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%)';
                    this.style.color = '#6366f1';
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = '0 2px 8px rgba(99, 102, 241, 0.2)';
                });
            } else if (text === 'Model Performance') {
                // Professional Emerald - success-oriented and modern
                btn.style.background = 'linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.15) 100%)';
                btn.style.color = '#10b981';
                btn.style.border = '2px solid #10b981';
                btn.style.boxShadow = '0 2px 8px rgba(16, 185, 129, 0.2)';
                btn.addEventListener('mouseenter', function() {
                    this.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
                    this.style.color = 'white';
                    this.style.transform = 'translateY(-2px)';
                    this.style.boxShadow = '0 4px 12px rgba(16, 185, 129, 0.4)';
                });
                btn.addEventListener('mouseleave', function() {
                    this.style.background = 'linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(5, 150, 105, 0.15) 100%)';
                    this.style.color = '#10b981';
                    this.style.transform = 'translateY(0)';
                    this.style.boxShadow = '0 2px 8px rgba(16, 185, 129, 0.2)';
                });
            }
        });
    }
    
    // Apply styles when page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(styleNavButtons, 100);
        });
    } else {
        setTimeout(styleNavButtons, 100);
    }
    
    // Re-apply styles after Streamlit reruns
    const observer = new MutationObserver(function(mutations) {
        setTimeout(styleNavButtons, 100);
    });
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)

def main():
    """Main application"""
    
    # Initialize session state for page navigation
    if 'nav_page' not in st.session_state:
        st.session_state.nav_page = "Home"
    
    # Create navigation bar
    create_navbar()
    
    # Load data and models
    df = load_data()
    model = load_model()
    preprocessor = load_preprocessor()
    
    # Display content based on selected page from header navigation
    if st.session_state.nav_page == "Home":
        show_home_page(df)
    
    elif st.session_state.nav_page == "Predict Churn":
        if model is None or preprocessor is None:
            st.error("⚠️ Model or preprocessor not found. Please run the training scripts first.")
            st.info("Run: `python data_preprocessing.py` then `python model_training.py`")
        else:
            show_prediction_page(model, preprocessor, df)
    
    elif st.session_state.nav_page == "Analytics Dashboard":
        if df is None:
            st.error("⚠️ Dataset not found. Please ensure Spotify_data.xlsx is in the directory.")
        else:
            show_analytics_dashboard(df)
    
    elif st.session_state.nav_page == "Model Performance":
        show_model_performance()
    
    # Add professional footer to all pages
    create_footer()

def create_footer():
    """Create footer section with social media icons only"""
    # LinkedIn SVG Icon (single line)
    linkedin_icon = '<svg class="social-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'
    
    # GitHub SVG Icon (single line)
    github_icon = '<svg class="social-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>'
    
    # Gmail SVG Icon (single line)
    gmail_icon = '<svg class="social-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.309-3.178 3.927-1.964L5.455 4.64 12 9.548l6.545-4.91 1.528-1.145C21.69 2.28 24 3.434 24 5.457z"/></svg>'
    
    # Footer HTML with icons and copyright
    footer_html = f'<div class="footer"><div class="footer-icons-container"><a href="https://www.linkedin.com/in/mt-anand" target="_blank" rel="noopener noreferrer" class="social-link-item" title="LinkedIn">{linkedin_icon}</a><a href="https://github.com/Anand8748" target="_blank" rel="noopener noreferrer" class="social-link-item" title="GitHub">{github_icon}</a><a href="mailto:anandhatti8748@gmail.com" class="social-link-item" title="Email">{gmail_icon}</a></div><div class="footer-copyright-text">© 2025 Churn Prediction System by <strong>Anand Hatti</strong></div></div>'
    
    st.markdown(footer_html, unsafe_allow_html=True)

def show_home_page(df):
    """Display professional home page"""
    import os
    import base64
    
    # Video Section - Replace hero section with video
    video_path = '237248_medium.mp4'
    
    if os.path.exists(video_path):
        # Display video with autoplay, loop, muted, and NO controls (no progress bar, time, or menu)
        try:
            with open(video_path, "rb") as video_file:
                video_bytes = video_file.read()
                video_base64 = base64.b64encode(video_bytes).decode()
            
            video_html = f"""
            <div class="video-container">
                <video autoplay loop muted playsinline style="width: 100%; height: 650px; object-fit: cover; border-radius: 15px;" oncontextmenu="return false;" disablePictureInPicture>
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            """
            st.markdown(video_html, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading video: {str(e)}")
            st.info("Please ensure 237248_medium.mp4 is in the project directory.")
    else:
        # Fallback message if video not found
        st.warning(f"Video file '{video_path}' not found. Please ensure the video file is in the project directory.")
        st.info("Expected video file: 237248_medium.mp4")
    
    # Features Section
    st.markdown('<h2 class="section-title">Key Features</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Powerful AI-driven tools to help you understand and prevent customer churn</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🔮</span>
            <h3 class="feature-title">Predict Churn</h3>
            <p class="feature-description">Get real-time churn probability predictions for individual customers using advanced machine learning models.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📈</span>
            <h3 class="feature-title">Analytics Dashboard</h3>
            <p class="feature-description">Explore customer data with interactive visualizations and discover patterns that drive churn.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📊</span>
            <h3 class="feature-title">Model Performance</h3>
            <p class="feature-description">View comprehensive metrics and evaluation results from multiple ML models.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Statistics Section
    if df is not None:
        st.markdown('<h2 class="section-title">Dataset Statistics</h2>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Comprehensive data insights at a glance</p>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(df):,}</div>
                <div class="stat-label">Total Users</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(df.columns)}</div>
                <div class="stat-label">Features</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            age_groups = df['Age'].nunique() if 'Age' in df.columns else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{age_groups}</div>
                <div class="stat-label">Age Groups</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            plans = df['spotify_subscription_plan'].nunique() if 'spotify_subscription_plan' in df.columns else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{plans}</div>
                <div class="stat-label">Subscription Plans</div>
            </div>
            """, unsafe_allow_html=True)
    
    # How It Works Section
    st.markdown('<h2 class="section-title">How It Works</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Simple steps to predict and prevent customer churn</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="how-it-works-step">
            <div class="step-number">1</div>
            <h3 class="step-title">Input Customer Data</h3>
            <p class="step-description">Enter customer details including demographics, preferences, and usage patterns.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="how-it-works-step">
            <div class="step-number">2</div>
            <h3 class="step-title">AI Analysis</h3>
            <p class="step-description">Our machine learning models analyze the data and calculate churn probability.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="how-it-works-step">
            <div class="step-number">3</div>
            <h3 class="step-title">Get Insights</h3>
            <p class="step-description">Receive actionable recommendations to prevent churn and retain customers.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Benefits Section
    st.markdown('<h2 class="section-title">Why Choose Our System?</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Key benefits that help you make better business decisions</p>', unsafe_allow_html=True)
    
    benefits = [
        {"icon": "🎯", "title": "Accurate Predictions", "desc": "State-of-the-art ML models with 99%+ accuracy in churn prediction."},
        {"icon": "⚡", "title": "Real-Time Analysis", "desc": "Get instant predictions and insights without waiting for batch processing."},
        {"icon": "📊", "title": "Comprehensive Analytics", "desc": "Deep dive into customer behavior with interactive dashboards and visualizations."},
        {"icon": "💡", "title": "Actionable Insights", "desc": "Receive personalized recommendations to reduce churn and improve retention."},
        {"icon": "🔒", "title": "Data-Driven Decisions", "desc": "Make informed business decisions based on comprehensive data analysis."},
        {"icon": "🚀", "title": "Easy to Use", "desc": "Intuitive interface that requires no technical expertise to operate."}
    ]
    
    col1, col2 = st.columns(2)
    
    for i, benefit in enumerate(benefits):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div class="benefit-item">
                <span class="benefit-icon">{benefit['icon']}</span>
                <div class="benefit-content">
                    <h4>{benefit['title']}</h4>
                    <p>{benefit['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Call to Action
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h2 style="font-size: 2rem; margin-bottom: 1rem; color: #1a1a1a;">Ready to Get Started?</h2>
            <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Start predicting customer churn and take action today!</p>
        </div>
        """, unsafe_allow_html=True)

def get_image_base64(image_path):
    """Convert image to base64 for embedding"""
    import base64
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

def show_prediction_page(model, preprocessor, df):
    """Display prediction page"""
    st.markdown('<div class="sub-header">🔮 Customer Churn Prediction</div>', unsafe_allow_html=True)
    
    # Get unique values from dataset for dropdowns
    if df is not None:
        age_options = sorted(df['Age'].unique().tolist()) if 'Age' in df.columns else []
        gender_options = sorted(df['Gender'].unique().tolist()) if 'Gender' in df.columns else []
        usage_period_options = sorted(df['spotify_usage_period'].unique().tolist()) if 'spotify_usage_period' in df.columns else []
        device_options = sorted(df['spotify_listening_device'].unique().tolist()) if 'spotify_listening_device' in df.columns else []
        plan_options = sorted(df['spotify_subscription_plan'].unique().tolist()) if 'spotify_subscription_plan' in df.columns else []
        willingness_options = sorted(df['premium_sub_willingness'].unique().tolist()) if 'premium_sub_willingness' in df.columns else []
        premium_plan_options = sorted([x for x in df['preffered_premium_plan'].unique().tolist() if pd.notna(x)]) if 'preffered_premium_plan' in df.columns else []
        content_options = sorted(df['preferred_listening_content'].unique().tolist()) if 'preferred_listening_content' in df.columns else []
        genre_options = sorted(df['fav_music_genre'].unique().tolist()) if 'fav_music_genre' in df.columns else []
        time_slot_options = sorted(df['music_time_slot'].unique().tolist()) if 'music_time_slot' in df.columns else []
        mood_options = sorted(df['music_Influencial_mood'].unique().tolist()) if 'music_Influencial_mood' in df.columns else []
        frequency_options = sorted(df['music_lis_frequency'].unique().tolist()) if 'music_lis_frequency' in df.columns else []
        expl_method_options = sorted(df['music_expl_method'].unique().tolist()) if 'music_expl_method' in df.columns else []
        rating_options = sorted(df['music_recc_rating'].unique().tolist()) if 'music_recc_rating' in df.columns else []
        pod_freq_options = sorted(df['pod_lis_frequency'].unique().tolist()) if 'pod_lis_frequency' in df.columns else []
        pod_genre_options = sorted([x for x in df['fav_pod_genre'].unique().tolist() if pd.notna(x)]) if 'fav_pod_genre' in df.columns else []
        pod_format_options = sorted([x for x in df['preffered_pod_format'].unique().tolist() if pd.notna(x)]) if 'preffered_pod_format' in df.columns else []
        pod_host_options = sorted([x for x in df['pod_host_preference'].unique().tolist() if pd.notna(x)]) if 'pod_host_preference' in df.columns else []
        pod_duration_options = sorted([x for x in df['preffered_pod_duration'].unique().tolist() if pd.notna(x)]) if 'preffered_pod_duration' in df.columns else []
        pod_satisfaction_options = sorted(df['pod_variety_satisfaction'].unique().tolist()) if 'pod_variety_satisfaction' in df.columns else []
    else:
        # Default options if dataset not available
        age_options = ['12-20', '20-35', '35-60', '60+']
        gender_options = ['Male', 'Female', 'Others']
        usage_period_options = ['Less than 3 months', '3-6 months', '6-12 months', '1-2 years', 'More than 2 years']
        device_options = ['Smartphone', 'Computer', 'Tablet', 'Smart Speaker']
        plan_options = ['Free', 'Premium Individual', 'Premium Family', 'Premium Student']
        willingness_options = ['Yes', 'No', 'Maybe']
        premium_plan_options = ['Not Applicable', 'Individual', 'Family', 'Student']
        content_options = ['Music', 'Podcasts', 'Both']
        genre_options = ['Pop', 'Rock', 'Hip-Hop', 'Jazz', 'Classical']
        time_slot_options = ['Morning', 'Afternoon', 'Evening', 'Night']
        mood_options = ['Happy', 'Sad', 'Energetic', 'Relaxed']
        frequency_options = ['Daily', 'Weekly', 'Monthly', 'Rarely']
        expl_method_options = ['Discover Weekly', 'Browse', 'Search', 'Recommendations']
        rating_options = [1, 2, 3, 4, 5]
        pod_freq_options = ['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never']
        pod_genre_options = ['Technology', 'Business', 'Entertainment', 'Education']
        pod_format_options = ['Interview', 'Solo', 'Panel Discussion']
        pod_host_options = ['Well-known', 'Unknown', 'No Preference']
        pod_duration_options = ['Short (<30 min)', 'Long (>30 min)', 'Both']
        pod_satisfaction_options = ['Satisfied', 'Ok', 'Not Satisfied']
    
    # Create input form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Customer Demographics")
            age = st.selectbox("Age Group", age_options, key='age')
            gender = st.selectbox("Gender", gender_options, key='gender')
            usage_period = st.selectbox("Spotify Usage Period", usage_period_options, key='usage')
            device = st.selectbox("Primary Listening Device", device_options, key='device')
            subscription_plan = st.selectbox("Subscription Plan", plan_options, key='plan')
            premium_willingness = st.selectbox("Premium Subscription Willingness", willingness_options, key='willingness')
            premium_plan = st.selectbox("Preferred Premium Plan", premium_plan_options, key='premium_plan')
        
        with col2:
            st.subheader("🎵 Music Preferences")
            listening_content = st.selectbox("Preferred Listening Content", content_options, key='content')
            music_genre = st.selectbox("Favorite Music Genre", genre_options, key='genre')
            time_slot = st.selectbox("Favorite Time Slot", time_slot_options, key='time')
            mood = st.selectbox("Music Influential Mood", mood_options, key='mood')
            listening_frequency = st.selectbox("Music Listening Frequency", frequency_options, key='freq')
            expl_method = st.selectbox("Music Discovery Method", expl_method_options, key='expl')
            rec_rating = st.slider("Music Recommendation Rating", 1, 5, 3, key='rating')
        
        st.subheader("🎙️ Podcast Preferences")
        col3, col4 = st.columns(2)
        with col3:
            pod_frequency = st.selectbox("Podcast Listening Frequency", pod_freq_options, key='pod_freq')
            pod_genre = st.selectbox("Favorite Podcast Genre", pod_genre_options, key='pod_genre')
            pod_format = st.selectbox("Preferred Podcast Format", pod_format_options, key='pod_format')
        with col4:
            pod_host = st.selectbox("Podcast Host Preference", pod_host_options, key='pod_host')
            pod_duration = st.selectbox("Preferred Podcast Duration", pod_duration_options, key='pod_duration')
            pod_satisfaction = st.selectbox("Podcast Variety Satisfaction", pod_satisfaction_options, key='pod_sat')
        
        submitted = st.form_submit_button("🔮 Predict Churn Risk", use_container_width=True, key="predict_submit")
        
        # Add styling for submit button
        st.markdown("""
        <style>
        button[data-testid="baseButton-primary"][aria-label*="Predict Churn Risk"],
        button:has-text("Predict Churn Risk"),
        form button[type="submit"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        }
        button[data-testid="baseButton-primary"][aria-label*="Predict Churn Risk"]:hover,
        button:has-text("Predict Churn Risk"):hover,
        form button[type="submit"]:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
        }
        </style>
        <script>
        // Ensure submit button has background color
        setTimeout(function() {
            const submitButtons = document.querySelectorAll('button[type="submit"], form button');
            submitButtons.forEach(function(btn) {
                if (btn.textContent.includes('Predict Churn Risk')) {
                    btn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                    btn.style.color = 'white';
                    btn.style.border = 'none';
                    btn.style.borderRadius = '8px';
                    btn.style.padding = '0.75rem 2rem';
                    btn.style.fontWeight = '600';
                    btn.style.fontSize = '1.1rem';
                    btn.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
                }
            });
        }, 200);
        </script>
        """, unsafe_allow_html=True)
        
        if submitted:
            # Prepare user input
            user_input = {
                'Age': age,
                'Gender': gender,
                'spotify_usage_period': usage_period,
                'spotify_listening_device': device,
                'spotify_subscription_plan': subscription_plan,
                'premium_sub_willingness': premium_willingness,
                'preffered_premium_plan': premium_plan,
                'preferred_listening_content': listening_content,
                'fav_music_genre': music_genre,
                'music_time_slot': time_slot,
                'music_Influencial_mood': mood,
                'music_lis_frequency': listening_frequency,
                'music_expl_method': expl_method,
                'music_recc_rating': rec_rating,
                'pod_lis_frequency': pod_frequency,
                'fav_pod_genre': pod_genre,
                'preffered_pod_format': pod_format,
                'pod_host_preference': pod_host,
                'preffered_pod_duration': pod_duration,
                'pod_variety_satisfaction': pod_satisfaction
            }
            
            try:
                # Preprocess and predict
                feature_names = preprocessor.get('feature_names', [])
                if not feature_names:
                    st.error("Feature names not found in preprocessor. Please retrain the model.")
                    return
                
                X_input = preprocess_user_input(user_input, preprocessor, feature_names)
                
                # Validate input shape
                if X_input.shape[1] != len(feature_names):
                    st.error(f"Feature mismatch: Expected {len(feature_names)} features, got {X_input.shape[1]}")
                    return
                
                # Make prediction
                churn_proba = model.predict_proba(X_input)[0][1]
                churn_pred = model.predict(X_input)[0]
                
                # Convert numpy types to Python native types for Streamlit
                churn_proba = float(churn_proba)
                churn_pred = int(churn_pred)
                
                # Validate probability range
                if not (0 <= churn_proba <= 1):
                    st.warning(f"Invalid probability value: {churn_proba}. Clamping to valid range.")
                    churn_proba = max(0.0, min(1.0, churn_proba))
                
                # Display results
                st.markdown("---")
                st.markdown('<div class="sub-header">📊 Prediction Results</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    risk_class = "high-risk" if churn_proba >= 0.5 else "low-risk"
                    risk_label = "🔴 HIGH RISK" if churn_proba >= 0.5 else "🟢 LOW RISK"
                    
                    st.markdown(f"""
                    <div class="prediction-box {risk_class}">
                        <h2>{risk_label}</h2>
                        <h1 style="font-size: 3rem; margin: 1rem 0;">{churn_proba*100:.1f}%</h1>
                        <p style="font-size: 1.2rem;">Churn Probability</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Progress bar - ensure it's a Python float
                st.progress(float(churn_proba))
                
                # Recommendations
                st.markdown("### 💡 Recommendations")
                if churn_proba >= 0.7:
                    st.warning("""
                    **High Churn Risk Detected!** 🚨
                    - Offer personalized premium trial
                    - Provide music discovery recommendations
                    - Send engagement campaigns
                    - Consider discount offers
                    """)
                elif churn_proba >= 0.5:
                    st.info("""
                    **Moderate Churn Risk** ⚠️
                    - Increase engagement through playlists
                    - Send personalized content recommendations
                    - Highlight premium features
                    """)
                else:
                    st.success("""
                    **Low Churn Risk** ✅
                    - Continue current engagement strategy
                    - Upsell premium features
                    - Maintain regular communication
                    """)
                
            except Exception as e:
                st.error(f"Error making prediction: {str(e)}")
                st.info("Please ensure all fields are filled correctly.")

def show_analytics_dashboard(df):
    """Display analytics dashboard"""
    st.markdown('<div class="sub-header">📈 Customer Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Customers", len(df))
    with col2:
        try:
            free_users = len(df[df['spotify_subscription_plan'].str.contains('Free', case=False, na=False)])
            st.metric("Free Users", free_users)
        except:
            st.metric("Free Users", 0)
    with col3:
        try:
            premium_users = len(df[df['spotify_subscription_plan'].str.contains('Premium', case=False, na=False)])
            st.metric("Premium Users", premium_users)
        except:
            st.metric("Premium Users", 0)
    with col4:
        avg_rating = df['music_recc_rating'].mean() if 'music_recc_rating' in df.columns else 0
        st.metric("Avg. Rating", f"{avg_rating:.2f}")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Subscription plan distribution
        if 'spotify_subscription_plan' in df.columns:
            try:
                plan_counts = df['spotify_subscription_plan'].value_counts()
                fig = px.pie(values=plan_counts.values, names=plan_counts.index, 
                            title="Subscription Plan Distribution",
                            color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display subscription plan chart: {str(e)}")
        
        # Age distribution
        if 'Age' in df.columns:
            try:
                age_counts = df['Age'].value_counts()
                fig = px.bar(x=age_counts.index, y=age_counts.values,
                            title="Age Group Distribution",
                            labels={'x': 'Age Group', 'y': 'Count'},
                            color=age_counts.values,
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display age distribution chart: {str(e)}")
    
    with col2:
        # Premium willingness
        if 'premium_sub_willingness' in df.columns:
            try:
                willingness_counts = df['premium_sub_willingness'].value_counts()
                fig = px.bar(x=willingness_counts.index, y=willingness_counts.values,
                            title="Premium Subscription Willingness",
                            labels={'x': 'Willingness', 'y': 'Count'},
                            color=willingness_counts.values,
                            color_continuous_scale='Plasma')
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display premium willingness chart: {str(e)}")
        
        # Music recommendation rating distribution
        if 'music_recc_rating' in df.columns:
            try:
                rating_counts = df['music_recc_rating'].value_counts().sort_index()
                fig = px.bar(x=rating_counts.index, y=rating_counts.values,
                            title="Music Recommendation Rating Distribution",
                            labels={'x': 'Rating', 'y': 'Count'},
                            color=rating_counts.values,
                            color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display rating distribution chart: {str(e)}")
    
    # Additional visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Listening device
        if 'spotify_listening_device' in df.columns:
            try:
                device_counts = df['spotify_listening_device'].value_counts()
                fig = px.treemap(names=device_counts.index, parents=['']*len(device_counts),
                               values=device_counts.values,
                               title="Listening Device Distribution",
                               color=device_counts.values,
                               color_continuous_scale='Greens')
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display listening device chart: {str(e)}")
    
    with col2:
        # Music genre preference
        if 'fav_music_genre' in df.columns:
            try:
                genre_counts = df['fav_music_genre'].value_counts().head(10)
                fig = px.bar(x=genre_counts.values, y=genre_counts.index,
                            orientation='h',
                            title="Top 10 Favorite Music Genres",
                            labels={'x': 'Count', 'y': 'Genre'},
                            color=genre_counts.values,
                            color_continuous_scale='Reds')
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display music genre chart: {str(e)}")

def show_model_performance():
    """Display model performance metrics"""
    st.markdown('<div class="sub-header">📊 Model Performance Metrics</div>', unsafe_allow_html=True)
    
    try:
        # Load results summary
        results_df = pd.read_csv('model_results_summary.csv', index_col=0)
        
        # Display dataframe without styling to avoid matplotlib version conflicts
        st.dataframe(results_df, use_container_width=True)
        
        # Format the dataframe for better display
        st.markdown("### 📊 Metrics Breakdown")
        for model_name in results_df.index:
            with st.expander(f"**{model_name}** Details"):
                metrics = results_df.loc[model_name]
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Accuracy", f"{metrics['accuracy']:.4f}")
                with col2:
                    st.metric("Precision", f"{metrics['precision']:.4f}")
                with col3:
                    st.metric("Recall", f"{metrics['recall']:.4f}")
                with col4:
                    st.metric("F1-Score", f"{metrics['f1_score']:.4f}")
                with col5:
                    st.metric("ROC-AUC", f"{metrics['roc_auc']:.4f}")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                fig = px.bar(results_df, x=results_df.index, y='accuracy',
                            title="Model Accuracy Comparison",
                            labels={'x': 'Model', 'y': 'Accuracy'},
                            color='accuracy',
                            color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display accuracy chart: {str(e)}")
        
        with col2:
            try:
                fig = px.bar(results_df, x=results_df.index, y='f1_score',
                            title="Model F1-Score Comparison",
                            labels={'x': 'Model', 'y': 'F1-Score'},
                            color='f1_score',
                            color_continuous_scale='Greens')
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not display F1-score chart: {str(e)}")
        
        # Show images if available
        try:
            st.markdown("### 📈 Detailed Performance Visualizations")
            col1, col2 = st.columns(2)
            with col1:
                try:
                    st.image('model_comparison.png', caption='Model Comparison')
                except FileNotFoundError:
                    st.info("Model comparison image not found.")
            with col2:
                try:
                    st.image('roc_curves.png', caption='ROC Curves')
                except FileNotFoundError:
                    st.info("ROC curves image not found.")
            
            try:
                st.image('feature_importance.png', caption='Feature Importance')
            except FileNotFoundError:
                st.info("Feature importance image not found.")
        except Exception as e:
            st.info(f"Performance visualization images not found. Run model_training.py to generate them. Error: {str(e)}")
    
    except FileNotFoundError:
        st.warning("Model results not found. Please run model_training.py first.")
        st.info("""
        To generate model performance metrics:
        1. Run `python data_preprocessing.py`
        2. Run `python model_training.py`
        3. Refresh this page
        """)

if __name__ == '__main__':
    main()

