"""
House Price Predictor - Streamlit Web App
A beautiful web interface to predict house prices based on features.
"""

import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Page configuration
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# Custom dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #00d4ff !important;
    }
    .price-display {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #00d4ff;
        text-align: center;
        margin: 20px 0;
    }
    .price-value {
        font-size: 48px;
        font-weight: bold;
        color: #00d4ff;
    }
    .price-label {
        font-size: 18px;
        color: #888;
        margin-top: 10px;
    }
    .feature-card {
        background-color: #1e2530;
        padding: 15px;
        border-radius: 10px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the trained model, scaler, and feature info from disk."""
    model_path = Path(__file__).parent / "model.pkl"
    scaler_path = Path(__file__).parent / "scaler.pkl"
    info_path = Path(__file__).parent / "feature_info.pkl"

    if not all(p.exists() for p in [model_path, scaler_path, info_path]):
        return None, None, None

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    with open(info_path, "rb") as f:
        feature_info = pickle.load(f)

    return model, scaler, feature_info


def predict_price(features, model, scaler):
    """
    Predict house price based on features.

    Args:
        features: dict with keys 'area', 'bedrooms', 'bathrooms', 'age', 'location'
        model: Trained Linear Regression model
        scaler: Fitted StandardScaler

    Returns:
        predicted_price: float
    """
    # Create feature array in correct order
    feature_names = ['area', 'bedrooms', 'bathrooms', 'age', 'location']
    X = np.array([[features[name] for name in feature_names]])

    # Scale and predict
    X_scaled = scaler.transform(X)
    price = model.predict(X_scaled)[0]

    # Ensure reasonable bounds
    return max(price, 50000)


def main():
    # Header
    st.markdown("# 🏠 House Price Predictor")
    st.markdown("*Predict house prices using machine learning*")
    st.divider()

    # Load model
    model, scaler, feature_info = load_model()

    if model is None:
        st.error("Model not found! Please run `python train.py` first.")
        st.code("python train.py", language="bash")
        return

    # Create layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📝 Enter House Details")

        # Input fields with sliders
        col_a, col_b = st.columns(2)

        with col_a:
            area = st.slider(
                "Area (sq ft)",
                int(feature_info['feature_ranges']['area'][0]),
                int(feature_info['feature_ranges']['area'][1]),
                2000,
                step=50,
                help="Total living area in square feet"
            )

            bedrooms = st.select_slider(
                "Bedrooms",
                options=[1, 2, 3, 4, 5, 6],
                value=3,
                help="Number of bedrooms"
            )

        with col_b:
            bathrooms = st.select_slider(
                "Bathrooms",
                options=[1, 1.5, 2, 2.5, 3, 3.5, 4],
                value=2,
                help="Number of bathrooms"
            )

            age = st.slider(
                "Age (years)",
                0, 100, 15,
                help="Age of the house in years"
            )

        location = st.slider(
            "Location Quality",
            1, 5, 3,
            help="1 = Poor, 5 = Excellent"
        )

        features = {
            'area': area,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'age': age,
            'location': location
        }

        # Show summary
        st.divider()
        st.markdown("#### Your Input Summary")
        summary_df = pd.DataFrame([
            ["Area", f"{area:,} sq ft"],
            ["Bedrooms", bedrooms],
            ["Bathrooms", bathrooms],
            ["Age", f"{age} years"],
            ["Location", f"{'⭐' * location}"]
        ], columns=["Feature", "Value"])
        st.dataframe(summary_df, hide_index=True, use_container_width=True)

        # Predict button
        if st.button("💰 Predict Price", type="primary", use_container_width=True):
            with st.spinner("Calculating..."):
                price = predict_price(features, model, scaler)

                st.divider()

                # Display price
                st.markdown(f"""
                <div class="price-display">
                    <div class="price-value">${price:,.0f}</div>
                    <div class="price-label">Estimated House Price</div>
                </div>
                """, unsafe_allow_html=True)

                # Price breakdown estimate
                st.markdown("#### Price Breakdown (Estimated)")
                base = 50000
                area_contribution = area * 100
                bedroom_contribution = bedrooms * 15000
                bathroom_contribution = bathrooms * 20000
                age_contribution = -age * 500
                location_contribution = location * 25000

                breakdown = pd.DataFrame([
                    ["Base Price", base, "#4ecdc4"],
                    [f"Area ({area:,} sq ft)", area_contribution, "#ff6b9d"],
                    [f"Bedrooms ({bedrooms})", bedroom_contribution, "#45b7d1"],
                    [f"Bathrooms ({bathrooms})", bathroom_contribution, "#ffd93d"],
                    [f"Age Deduction ({age} yrs)", age_contribution, "#ff4b4b"],
                    [f"Location (⭐{location})", location_contribution, "#6bcb77"],
                ], columns=["Factor", "Contribution", "Color"])

                for _, row in breakdown.iterrows():
                    color = row["Color"]
                    value = row["Contribution"]
                    st.markdown(
                        f'<div style="display: flex; justify-content: space-between; padding: 8px 0; '
                        f'border-bottom: 1px solid #333;">'
                        f'<span>{row["Factor"]}</span>'
                        f'<span style="color: {color};">{"+" if value >= 0 else ""}${value:,}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

    with col2:
        st.markdown("### 📊 Model Insights")

        # Show analysis image if available
        analysis_path = Path(__file__).parent / "model_analysis.png"
        if analysis_path.exists():
            st.image(analysis_path, use_container_width=True)

        # Feature importance
        st.markdown("#### Feature Impact")
        feature_impact = pd.DataFrame({
            'Feature': ['Area', 'Bedrooms', 'Bathrooms', 'Age', 'Location'],
            'Impact': ['+$100/sq ft', '+$15,000/bed', '+$20,000/bath', '-$500/year', '+$25,000/level'],
            'Type': ['Positive', 'Positive', 'Positive', 'Negative', 'Positive']
        })
        st.dataframe(feature_impact, hide_index=True, use_container_width=True)

    # Info section
    st.divider()
    st.markdown("""
    <div style="background-color: #1e2530; padding: 15px; border-radius: 8px; border-left: 4px solid #00d4ff;">
    <strong>How It Works:</strong><br>
    This predictor uses <strong>Linear Regression</strong> to find the best-fit line through your data.
    It learns how each feature (area, bedrooms, etc.) contributes to the final price and combines
    them to make predictions. The model was trained on 500 sample houses with realistic pricing patterns.
    </div>
    """, unsafe_allow_html=True)

    # Quick presets
    st.markdown("### 🎯 Quick Presets")
    col1, col2, col3, col4 = st.columns(4)

    presets = [
        ("🏠 Starter Home", {"area": 1200, "bedrooms": 2, "bathrooms": 1, "age": 30, "location": 2}),
        ("👨‍👩‍👧 Family Home", {"area": 2000, "bedrooms": 3, "bathrooms": 2, "age": 10, "location": 3}),
        ("🏰 Luxury Home", {"area": 3500, "bedrooms": 5, "bathrooms": 3.5, "age": 5, "location": 5}),
        ("🏚️ Fixer-Upper", {"area": 1800, "bedrooms": 3, "bathrooms": 1.5, "age": 50, "location": 2}),
    ]

    for col, (label, preset) in zip([col1, col2, col3, col4], presets):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.preset = preset
                st.rerun()


if __name__ == "__main__":
    main()
