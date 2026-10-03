"""
AI Translator - Translate text between languages with auto-detect
Uses Gemini AI for intelligent translation
"""

import streamlit as st
import os
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="AI Translator",
    page_icon="🌐",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #10B981; }
    .sub-header { font-size: 1.2rem; color: #34D399; }
    .stTextArea > div > div > textarea { background-color: #1E1E2E; }
    .translation-box { background-color: #1a1a2e; padding: 20px; border-radius: 10px; border-left: 4px solid #10B981; }
</style>
""", unsafe_allow_html=True)

# Supported languages
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese (Simplified)": "zh",
    "Arabic": "ar",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
}

def get_gemini_api_key(api_key_input: str = None) -> str:
    """Get Gemini API key from various sources"""
    if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
        return st.secrets['GEMINI_API_KEY']
    if os.environ.get('GEMINI_API_KEY'):
        return os.environ.get('GEMINI_API_KEY')
    if api_key_input:
        return api_key_input
    return None

def setup_gemini(api_key: str):
    """Configure Gemini with API key"""
    if api_key:
        genai.configure(api_key=api_key)

def detect_language(text: str, model) -> str:
    """Detect the language of input text"""
    try:
        response = model.generate_content(
            f"""Detect the language of the following text. Return ONLY the language name in English.
            Examples: "Hello" → English, "Bonjour" → French, "Hola" → Spanish

            Text: {text[:200]}

            Return ONLY the language name, nothing else."""
        )
        return response.text.strip()
    except Exception as e:
        return f"Unknown ({str(e)})"

def translate_text(text: str, source_lang: str, target_lang: str, model) -> str:
    """Translate text using Gemini"""
    try:
        response = model.generate_content(
            f"""Translate the following text from {source_lang} to {target_lang}.
            Preserve the tone, style, and nuance of the original text.
            If it's a formal text, keep it formal. If informal, keep it casual.

            Text to translate:
            {text}

            Return ONLY the translation, nothing else."""
        )
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Header
    st.markdown('<p class="main-header">🌐 AI Translator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Intelligent translation with auto-detect and 22+ languages</p>', unsafe_allow_html=True)
    st.divider()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        api_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get your API key from Google AI Studio"
        )

        st.markdown("---")
        st.markdown("""
        **How to get an API key:**
        1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Create a new API key
        3. Paste it here
        """)

        st.markdown("---")
        st.markdown("**Supported Languages:**")
        for lang in list(LANGUAGES.keys())[:10]:
            st.markdown(f"- {lang}")
        st.markdown("*... and 12 more*")

    # Main content
    st.subheader("📝 Enter Text to Translate")

    col1, col2 = st.columns([1, 1])

    with col1:
        input_text = st.text_area(
            "Your text",
            placeholder="Type or paste text in any language...",
            height=200
        )

        auto_detect = st.checkbox("🔍 Auto-detect language", value=True)

        if not auto_detect:
            source_lang = st.selectbox("Source Language", list(LANGUAGES.keys()), index=0)
        else:
            source_lang = None

    with col2:
        target_lang = st.selectbox("Target Language", list(LANGUAGES.keys()), index=0)

        translate_btn = st.button("🔄 Translate", type="primary", use_container_width=True)

    # Detection result
    if input_text and auto_detect:
        api_key = get_gemini_api_key(api_key_input)
        if api_key:
            with st.spinner("Detecting language..."):
                try:
                    setup_gemini(api_key)
                    model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    detected = detect_language(input_text, model)
                    st.success(f"🔍 Detected: **{detected}**")
                except:
                    st.info("Enter API key to detect language")
        else:
            st.info("Enter API key in sidebar to auto-detect language")

    st.divider()

    # Translation result
    if translate_btn and input_text:
        api_key = get_gemini_api_key(api_key_input)

        if not api_key:
            st.error("⚠️ Please enter your Gemini API key in the sidebar!")
        else:
            detected_lang = None

            if auto_detect:
                with st.spinner("Detecting language..."):
                    try:
                        setup_gemini(api_key)
                        model = genai.GenerativeModel('gemini-2.0-flash-exp')
                        detected_lang = detect_language(input_text, model)
                    except Exception as e:
                        st.error(f"Detection error: {e}")
                        return

            source_display = detected_lang if detected_lang else source_lang

            with st.spinner("Translating..."):
                try:
                    setup_gemini(api_key)
                    model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    result = translate_text(input_text, source_display, target_lang, model)

                    st.success(f"✅ Translated from {source_display} to {target_lang}")
                    st.markdown(f'<div class="translation-box">{result}</div>', unsafe_allow_html=True)

                    # Character count
                    st.caption(f"Original: {len(input_text)} chars | Translation: {len(result)} chars")

                    # Copy button
                    st.code(result, language=None)

                except Exception as e:
                    st.error(f"Translation error: {str(e)}")

    # Quick examples
    st.divider()
    st.subheader("💡 Quick Examples")

    examples = [
        ("English → Spanish", "Hello, how are you?"),
        ("French → English", "Bonjour, comment allez-vous?"),
        ("Japanese → English", "今日は良い天気ですね"),
        ("Hindi → English", "आप कैसे हैं?"),
    ]

    cols = st.columns(4)
    for i, (desc, text) in enumerate(examples):
        with cols[i]:
            st.code(text[:50] + "..." if len(text) > 50 else text, language=None)
            st.caption(desc)

if __name__ == "__main__":
    main()
