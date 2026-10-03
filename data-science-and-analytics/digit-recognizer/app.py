"""
Digit Recognizer - Streamlit Web App
A beautiful web interface to draw and recognize handwritten digits.
"""

import pickle
from io import BytesIO

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="Digit Recognizer",
    page_icon="🔢",
    layout="centered"
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
    .prediction-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 40px;
        border-radius: 20px;
        border: 3px solid #00d4ff;
        text-align: center;
        margin: 20px 0;
    }
    .digit-display {
        font-size: 120px;
        font-weight: bold;
        color: #00d4ff;
        margin: 20px 0;
    }
    .confidence-bar {
        height: 30px;
        border-radius: 15px;
        margin: 8px 0;
        display: flex;
        align-items: center;
        padding: 0 15px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the trained model and scaler from disk."""
    model_path = Path(__file__).parent / "model.pkl"
    scaler_path = Path(__file__).parent / "scaler.pkl"

    if not all(p.exists() for p in [model_path, scaler_path]):
        return None, None

    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)

    return model, scaler


def preprocess_digit_image(image_array):
    """
    Preprocess the drawn image to match the training data format.
    - Resize to 8x8
    - Normalize pixel values
    - Flatten to 1D array
    """
    # Convert to PIL Image if needed
    if not isinstance(image_array, Image.Image):
        image_array = Image.fromarray(image_array.astype('uint8'), 'L')

    # Resize to 8x8 (MNIST digit size)
    image_array = image_array.resize((8, 8), Image.LANCZOS)

    # Convert to numpy array
    img = np.array(image_array)

    # Invert: MNIST has white digits on black, we draw black on white
    img = 255 - img

    # Normalize to 0-16 range (like MNIST)
    img = (img / 255) * 16
    img = img.astype('float64')

    # Flatten
    return img.flatten().reshape(1, -1)


def predict_digit(image_array, model, scaler):
    """
    Predict the digit from a drawn image.

    Args:
        image_array: 2D numpy array of pixel values
        model: Trained SVM classifier
        scaler: Fitted StandardScaler

    Returns:
        prediction: The predicted digit (0-9)
        probabilities: Array of class probabilities
    """
    # Preprocess
    X = preprocess_digit_image(image_array)

    # Scale
    X_scaled = scaler.transform(X)

    # Predict
    prediction = model.predict(X_scaled)[0]
    probabilities = model.predict_proba(X_scaled)[0]

    return prediction, probabilities


def main():
    # Header
    st.markdown("# 🔢 Handwritten Digit Recognizer")
    st.markdown("*Draw a digit and let the AI identify it!*")
    st.divider()

    # Load model
    model, scaler = load_model()

    if model is None:
        st.error("Model not found! Please run `python train.py` first.")
        st.code("python train.py", language="bash")
        return

    # Create canvas for drawing
    st.markdown("### ✏️ Draw a Digit (0-9)")
    st.markdown("Use your mouse or finger to draw a single digit")

    # Canvas component using simple HTML/JS
    canvas_html = """
    <style>
        .canvas-container {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }
        canvas {
            border: 3px solid #00d4ff;
            border-radius: 10px;
            cursor: crosshair;
            background-color: white;
        }
    </style>
    <div class="canvas-container">
        <canvas id="digitCanvas" width="280" height="280"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('digitCanvas');
        const ctx = canvas.getContext('2d');
        let isDrawing = false;

        // Set white background
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Drawing settings
        ctx.strokeStyle = 'black';
        ctx.lineWidth = 15;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        canvas.addEventListener('mousedown', startDrawing);
        canvas.addEventListener('mousemove', draw);
        canvas.addEventListener('mouseup', stopDrawing);
        canvas.addEventListener('mouseleave', stopDrawing);

        // Touch support
        canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            startDrawing(e.touches[0]);
        });
        canvas.addEventListener('touchmove', (e) => {
            e.preventDefault();
            draw(e.touches[0]);
        });
        canvas.addEventListener('touchend', stopDrawing);

        function startDrawing(e) {
            isDrawing = true;
            const rect = canvas.getBoundingClientRect();
            ctx.beginPath();
            ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
        }

        function draw(e) {
            if (!isDrawing) return;
            const rect = canvas.getBoundingClientRect();
            ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
            ctx.stroke();
        }

        function stopDrawing() {
            isDrawing = false;
        }
    </script>
    """

    # We use a file uploader as a workaround since Streamlit doesn't have a native canvas
    # But we'll show instructions for the user
    st.info("📌 To use this app, either draw on the canvas below or upload a handwritten digit image")

    # Use webcam/camera if available, otherwise use file upload
    uploaded_file = st.file_uploader(
        "Or upload an image of a handwritten digit:",
        type=['png', 'jpg', 'jpeg'],
        help="Upload an image containing a single handwritten digit (0-9)"
    )

    # Process button
    col1, col2 = st.columns(2)
    with col1:
        predict_clicked = st.button("🔍 Recognize Digit", type="primary", use_container_width=True)
    with col2:
        clear_clicked = st.button("🗑️ Clear Canvas", use_container_width=True)

    # Simple canvas using HTML (will be replaced by uploaded image processing)
    st.components.v1.html(canvas_html, height=350)

    # Also process uploaded images
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('L')
        st.image(image, caption="Uploaded Image", width=150)

    # Make prediction
    if predict_clicked:
        if uploaded_file is not None:
            image = Image.open(uploaded_file).convert('L')
            np_image = np.array(image)

            with st.spinner("Analyzing..."):
                prediction, probabilities = predict_digit(np_image, model, scaler)

            display_results(prediction, probabilities)
        else:
            # If using canvas, we need to capture it - show info message
            st.info("💡 For best results, upload a clear image of a handwritten digit, or use the sample digits below")

            # Show sample digit buttons
            st.markdown("### Or try a sample digit:")
            sample_cols = st.columns(5)
            for i in range(5):
                with sample_cols[i]:
                    if st.button(f"Try {i}", key=f"sample_{i}", use_container_width=True):
                        # Use a simple synthetic digit for demo
                        # In production, you'd use actual digit images
                        st.session_state.sample_digit = i
                        st.rerun()

            if hasattr(st.session_state, 'sample_digit'):
                # Show a message about the sample
                st.success(f"You selected digit {st.session_state.sample_digit}. Upload a real image to test the model!")

    # Show sample images
    st.divider()
    st.markdown("### 📚 How It Works")
    st.markdown("""
    <div style="background-color: #1e2530; padding: 15px; border-radius: 8px; border-left: 4px solid #00d4ff;">
    <strong>Machine Learning Pipeline:</strong><br><br>
    1. <strong>Data:</strong> Model trained on 1,797 handwritten digit images (8x8 pixels each)<br>
    2. <strong>Preprocessing:</strong> Images are resized and normalized to match training format<br>
    3. <strong>SVM Classifier:</strong> Support Vector Machine with RBF kernel classifies the digit<br>
    4. <strong>Confidence:</strong> Probability estimates show how sure the model is<br>
    </div>
    """, unsafe_allow_html=True)

    # Show sample digit image if available
    sample_path = Path(__file__).parent / "sample_digits.png"
    if sample_path.exists():
        st.markdown("### Sample Digits from Training Data")
        st.image(sample_path, use_container_width=True)


def display_results(prediction, probabilities):
    """Display the prediction results."""
    st.divider()

    # Main prediction
    st.markdown(f"""
    <div class="prediction-box">
        <div style="font-size: 24px; color: #888;">Recognized Digit:</div>
        <div class="digit-display">{prediction}</div>
        <div style="color: #888;">with {probabilities[prediction]*100:.1f}% confidence</div>
    </div>
    """, unsafe_allow_html=True)

    # Confidence bars
    st.markdown("### Confidence for Each Digit")
    colors = ['#ff6b9d', '#4ecdc4', '#45b7d1', '#ffd93d', '#6bcb77',
              '#ff8c42', '#a66cff', '#ff6b6b', '#00d4ff', '#c9f']

    for i, (prob, color) in enumerate(zip(probabilities, colors)):
        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            st.markdown(f"**{i}**")
        with col2:
            # Progress bar using HTML
            st.markdown(
                f'<div style="background-color: #333; border-radius: 10px; overflow: hidden;">'
                f'<div style="background-color: {color}; width: {prob*100}%; '
                f'height: 25px; border-radius: 10px;"></div></div>',
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(f"{prob*100:.1f}%")


if __name__ == "__main__":
    main()
