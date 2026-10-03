"""
Iris Classifier - Streamlit Web App
A beautiful web interface to classify iris flowers by their measurements.
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
    page_title="Iris Classifier",
    page_icon="🌸",
    layout="wide"
)

# Custom dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #ff6b9d !important;
    }
    .flower-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid;
        text-align: center;
        margin: 10px 0;
    }
    .setosa { border-color: #ff6b6b; }
    .versicolor { border-color: #4ecdc4; }
    .virginica { border-color: #45b7d1; }
    .flower-name {
        font-size: 28px;
        font-weight: bold;
        margin: 10px 0;
    }
    .confidence-bar {
        height: 25px;
        border-radius: 12px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the trained model, scaler, and class info from disk."""
    model_path = Path(__file__).parent / "model.pkl"
    scaler_path = Path(__file__).parent / "scaler.pkl"
    info_path = Path(__file__).parent / "class_info.pkl"

    if not all(p.exists() for p in [model_path, scaler_path, info_path]):
        return None, None, None

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
    with open(info_path, "rb") as f:
        class_info = pickle.load(f)

    return model, scaler, class_info


def predict_species(features, model, scaler):
    """
    Predict iris species based on flower measurements.

    Args:
        features: [sepal_length, sepal_width, petal_length, petal_width]
        model: Trained KNN classifier
        scaler: Fitted StandardScaler

    Returns:
        prediction: Species index (0, 1, or 2)
        probabilities: Array of class probabilities
    """
    # Scale features
    features_scaled = scaler.transform([features])

    # Predict
    prediction = model.predict(features_scaled)[0]
    probabilities = model.predict_proba(features_scaled)[0]

    return prediction, probabilities


def main():
    # Header
    st.markdown("# 🌸 Iris Flower Classifier")
    st.markdown("*Enter flower measurements to predict the species*")
    st.divider()

    # Load model
    model, scaler, class_info = load_model()

    if model is None:
        st.error("Model not found! Please run `python train.py` first.")
        st.code("python train.py", language="bash")
        return

    # Create two columns: input and visualization
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📏 Enter Flower Measurements")

        # Feature sliders with realistic ranges from the dataset
        sepal_length = st.slider(
            "Sepal Length (cm)",
            4.3, 7.9, 5.8,
            help="Length of the sepal in centimeters"
        )

        sepal_width = st.slider(
            "Sepal Width (cm)",
            2.0, 4.4, 3.0,
            help="Width of the sepal in centimeters"
        )

        petal_length = st.slider(
            "Petal Length (cm)",
            1.0, 6.9, 4.0,
            help="Length of the petal in centimeters"
        )

        petal_width = st.slider(
            "Petal Width (cm)",
            0.1, 2.5, 1.2,
            help="Width of the petal in centimeters"
        )

        features = [sepal_length, sepal_width, petal_length, petal_width]

        # Show feature summary
        st.divider()
        st.markdown("#### Your Measurements")
        feature_df = pd.DataFrame({
            "Feature": class_info["feature_names"],
            "Value": features
        })
        st.dataframe(feature_df, hide_index=True, use_container_width=True)

        # Predict button
        if st.button("🔍 Classify Species", type="primary", use_container_width=True):
            with st.spinner("Analyzing..."):
                prediction, probabilities = predict_species(features, model, scaler)
                species_name = class_info["target_names"][prediction]

                st.divider()

                # Display result with appropriate styling
                css_classes = ["setosa", "versicolor", "virginica"]
                emoji = ["🌺", "🌷", "💐"]
                descriptions = [
                    "Small petals, narrow sepals",
                    "Medium petals, medium sepals",
                    "Large petals, wide sepals"
                ]

                st.markdown(f"""
                <div class="flower-card {css_classes[prediction]}">
                    <div style="font-size: 60px;">{emoji[prediction]}</div>
                    <div class="flower-name">{species_name.upper()}</div>
                    <p>{descriptions[prediction]}</p>
                </div>
                """, unsafe_allow_html=True)

                # Confidence display
                st.markdown("#### Confidence Scores")
                colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
                for i, (name, prob) in enumerate(zip(class_info["target_names"], probabilities)):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{name}**")
                        progress_color = colors[i]
                        st.markdown(
                            f'<div style="background-color: #333; border-radius: 10px; overflow: hidden;">'
                            f'<div style="background-color: {progress_color}; width: {prob*100}%; '
                            f'height: 20px; border-radius: 10px;"></div></div>',
                            unsafe_allow_html=True
                        )
                    with col2:
                        st.metric("", f"{prob*100:.1f}%")

    with col2:
        st.markdown("### 📊 Species Overview")

        # Create visualization comparing the three species
        fig, ax = plt.subplots(figsize=(8, 5))

        # Data for the three species (mean values)
        species_data = {
            'Setosa': [5.00, 3.42, 1.46, 0.24],
            'Versicolor': [5.94, 2.77, 4.26, 1.33],
            'Virginica': [6.59, 2.97, 5.55, 2.03]
        }

        features = ['Sepal\nLength', 'Sepal\nWidth', 'Petal\nLength', 'Petal\nWidth']
        x = np.arange(len(features))
        width = 0.25

        for i, (species, values) in enumerate(species_data.items()):
            ax.bar(x + i*width, values, width, label=species,
                   color=['#ff6b6b', '#4ecdc4', '#45b7d1'][i])

        ax.set_xlabel('Features')
        ax.set_ylabel('Measurement (cm)')
        ax.set_title('Average Measurements by Species')
        ax.set_xticks(x + width)
        ax.set_xticklabels(features)
        ax.legend()
        ax.set_facecolor('#1e2530')
        fig.patch.set_facecolor('#0e1117')
        ax.tick_params(colors='white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(axis='y', alpha=0.3)

        st.pyplot(fig)

        # Show decision boundary image if available
        db_path = Path(__file__).parent / "decision_boundaries.png"
        if db_path.exists():
            st.markdown("#### Decision Boundaries")
            st.image(db_path, use_container_width=True)

    # Info section
    st.divider()
    st.markdown("""
    <div style="background-color: #1e2530; padding: 15px; border-radius: 8px; border-left: 4px solid #ff6b9d;">
    <strong>How It Works:</strong><br>
    This classifier uses <strong>K-Nearest Neighbors (KNN)</strong> with K=5 neighbors.
    When you input measurements, the algorithm finds the 5 most similar flowers in the
    training data and predicts the species by majority vote.
    </div>
    """, unsafe_allow_html=True)

    # Quick presets
    st.markdown("### 🎯 Quick Presets")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🌺 Setosa", use_container_width=True):
            st.session_state.s_l = 5.0
            st.session_state.s_w = 3.4
            st.session_state.p_l = 1.5
            st.session_state.p_w = 0.2
            st.rerun()

    with col2:
        if st.button("🌷 Versicolor", use_container_width=True):
            st.session_state.s_l = 5.9
            st.session_state.s_w = 2.8
            st.session_state.p_l = 4.3
            st.session_state.p_w = 1.3
            st.rerun()

    with col3:
        if st.button("💐 Virginica", use_container_width=True):
            st.session_state.s_l = 6.6
            st.session_state.s_w = 3.0
            st.session_state.p_l = 5.6
            st.session_state.p_w = 2.1
            st.rerun()


if __name__ == "__main__":
    main()
