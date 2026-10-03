import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Caption Generator", page_icon="", layout="centered")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1a1a2e 0%, #2d132c 100%); }
.stTextInput input, .stTextArea textarea { background: #1a1a2e !important; color: white !important; border: 2px solid #e94560 !important; border-radius: 12px; }
.stButton>button { background: linear-gradient(90deg, #e94560, #ff6b6b); color: white; border: none; border-radius: 25px; padding: 0.5rem 2rem; font-weight: bold; }
h1, h2 { color: #e94560 !important; }
.stFileUploader>div { background: #1a1a2e; border: 2px dashed #e94560; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("  AI Caption Generator")
st.caption("Create viral-worthy captions for any image")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error(" Set GEMINI_API_KEY in your environment")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

tab1, tab2 = st.tabs([" Upload Image", " Describe Image"])

with tab1:
    uploaded_file = st.file_uploader(" Choose an image", type=["jpg", "jpeg", "png", "webp"])
    image_description = ""
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption=" Your image", use_column_width=True)
        image_description = f"Image shows: {uploaded_file.name}"

with tab2:
    image_description = st.text_area(" Describe your image", placeholder="A golden sunset over mountains with a lone traveler...")

platform = st.selectbox(" Platform", ["Instagram", "Twitter/X", "Both"])
style = st.selectbox(" Caption Style", ["Casual & Fun", "Professional", "Inspirational", "Humorous", "Storytelling"])

if st.button("  Generate Captions"):
    if image_description:
        with st.spinner("  Creating viral captions..."):
            prompt = f"""Generate 5 creative captions for {platform} for this image:
{image_description}

Style: {style}
For Instagram: Include relevant emojis, line breaks, and hashtags
For Twitter: Keep it punchy, 280 chars max with hashtags

Return 5 captions, each clearly labeled and separated."""

            try:
                response = model.generate_content(prompt)
                st.success("  Captions generated!")
                st.markdown(response.text.replace('\n', '\n\n'))
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("  Please upload or describe an image")

st.markdown("---")
st.markdown("  *Powered by Gemini AI*", unsafe_allow_html=True)
