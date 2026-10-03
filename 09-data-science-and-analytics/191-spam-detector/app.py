"""
Spam Detector - Streamlit Web App
A simple web interface to check if a message is spam or not.
"""

import pickle
from pathlib import Path

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Spam Detector",
    page_icon="📧",
    layout="centered"
)

# Custom dark theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0e1117;
    }

    /* Text color */
    stMarkdown, stText, p, span {
        color: #fafafa !important;
    }

    /* Headers */
    h1, h2, h3 {
        color: #00d4ff !important;
    }

    /* Success/Error boxes */
    .spam-box, .ham-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
    }
    .spam-box {
        background-color: #ff4b4b;
        color: white;
    }
    .ham-box {
        background-color: #00cc66;
        color: white;
    }

    /* Custom info box */
    .info-box {
        background-color: #1e2530;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00d4ff;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the trained model and vectorizer from disk."""
    model_path = Path(__file__).parent / "model.pkl"
    vectorizer_path = Path(__file__).parent / "vectorizer.pkl"

    if not model_path.exists() or not vectorizer_path.exists():
        return None, None

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

    return model, vectorizer


def predict_spam(message, model, vectorizer):
    """
    Predict if a message is spam or ham.

    Args:
        message: The text message to check
        model: Trained classifier
        vectorizer: Fitted CountVectorizer

    Returns:
        prediction: 0 (ham) or 1 (spam)
        probability: Confidence score
    """
    # Convert text to numerical features
    X = vectorizer.transform([message])

    # Get prediction and probability
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]

    return prediction, probability


def main():
    # Header
    st.markdown("# 📧 Spam Detector")
    st.markdown("*Check if your message is spam or legitimate*")
    st.divider()

    # Load model
    model, vectorizer = load_model()

    if model is None:
        st.error("Model not found! Please run `python train.py` first to train the model.")
        st.code("python train.py", language="bash")
        return

    # Input section
    st.markdown("### Enter a Message to Check")
    message = st.text_area(
        "Type or paste your message here:",
        height=150,
        placeholder="e.g., 'Congratulations! You won a free iPhone! Click here to claim.'"
    )

    # Predict button
    if st.button("🔍 Check for Spam", type="primary", use_container_width=True):
        if message.strip():
            with st.spinner("Analyzing message..."):
                prediction, probability = predict_spam(message, model, vectorizer)

                st.divider()

                # Show result
                if prediction == 1:
                    st.markdown('<div class="spam-box">🚫 SPAM DETECTED</div>', unsafe_allow_html=True)
                    confidence = probability[1] * 100
                    st.markdown(f"**Confidence:** {confidence:.1f}%")
                else:
                    st.markdown('<div class="ham-box">✅ LEGITIMATE MESSAGE (HAM)</div>', unsafe_allow_html=True)
                    confidence = probability[0] * 100
                    st.markdown(f"**Confidence:** {confidence:.1f}%")

                # Show probability breakdown
                st.markdown("### Probability Breakdown")
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Ham Probability", f"{probability[0]*100:.1f}%")
                with col2:
                    st.metric("Spam Probability", f"{probability[1]*100:.1f}%")

                # Progress bars
                st.progress(probability[0], text="Ham")
                st.progress(probability[1], text="Spam")
        else:
            st.warning("Please enter a message to check.")

    # Info section
    st.divider()
    st.markdown("### How It Works")
    st.markdown("""
    <div class="info-box">
    <strong>Machine Learning Pipeline:</strong><br>
    1. <strong>Bag of Words:</strong> Text is converted to numerical features based on word frequency<br>
    2. <strong>Naive Bayes:</strong> A probabilistic classifier that calculates the likelihood of spam<br>
    3. <strong>Training:</strong> Model learns from thousands of labeled spam/ham examples<br>
    4. <strong>Prediction:</strong> New messages are classified based on learned patterns
    </div>
    """, unsafe_allow_html=True)

    # Example messages
    st.markdown("### Try These Examples")
    examples = [
        "Hey, are we still meeting for lunch today?",
        "Congratulations! You've won a free iPhone! Click here now!",
        "Can you send me the report when you get a chance?",
        "URGENT: Your account has been compromised. Verify now!",
    ]

    for i, ex in enumerate(examples):
        if st.button(f"📝 {ex[:50]}...", key=f"ex_{i}", use_container_width=True):
            st.session_state.message_input = ex
            st.rerun()


if __name__ == "__main__":
    main()
