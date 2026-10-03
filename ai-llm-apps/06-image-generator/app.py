"""
Image Generator - Text to Image using Gemini AI
Creates images from text descriptions
"""

import streamlit as st
import os
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #8B5CF6; }
    .sub-header { font-size: 1.2rem; color: #A78BFA; }
    .stTextInput > div > div > input { background-color: #1E1E2E; }
    .success-box { background-color: #1a1a2e; padding: 20px; border-radius: 10px; border-left: 4px solid #8B5CF6; }
</style>
""", unsafe_allow_html=True)

def get_gemini_api_key(api_key_input: str = None) -> str:
    """Get Gemini API key from secrets, environment, or user input"""
    # Try Streamlit secrets first
    if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
        return st.secrets['GEMINI_API_KEY']
    # Try environment variable
    if os.environ.get('GEMINI_API_KEY'):
        return os.environ.get('GEMINI_API_KEY')
    # Try user input
    if api_key_input:
        return api_key_input
    return None

def setup_gemini(api_key: str):
    """Configure Gemini with API key"""
    if api_key:
        genai.configure(api_key=api_key)

def generate_image_description(prompt: str, model) -> str:
    """Generate image description using Gemini"""
    response = model.generate_content(
        f"""You are a creative image prompt generator. Given the user's idea, create a detailed,
        vivid image generation prompt for an AI image generator.

        User's idea: {prompt}

        Create a detailed prompt (2-3 sentences) that describes:
        - The main subject and composition
        - The style (photorealistic, illustration, anime, etc.)
        - The mood and lighting
        - Any specific details

        Return ONLY the prompt, nothing else."""
    )
    return response.text

def generate_image(prompt: str, model) -> str:
    """Generate image using Gemini 2.0 Flash Experimental"""
    try:
        # Use gemini-2.0-flash-exp for image generation
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Fallback to description if image generation not available
        return generate_image_description(prompt, model)

def main():
    # Header
    st.markdown('<p class="main-header">🎨 AI Image Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your ideas into visual descriptions</p>', unsafe_allow_html=True)
    st.divider()

    # Sidebar for API key
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
        st.markdown("**Tips for great images:**")
        st.markdown("""
        - Be specific about subjects
        - Mention art style
        - Describe lighting/mood
        - Include composition details
        """)

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("💭 Describe Your Image")

        prompt = st.text_area(
            "What do you want to create?",
            placeholder="Example: A futuristic city at sunset with flying cars and neon lights, cyberpunk style",
            height=150
        )

        generate_button = st.button("🚀 Generate Image Prompt", type="primary", use_container_width=True)

    with col2:
        st.subheader("✨ Generated Result")

        if generate_button and prompt:
            api_key = get_gemini_api_key(api_key_input)

            if not api_key:
                st.error("⚠️ Please enter your Gemini API key in the sidebar!")
            else:
                with st.spinner("Generating your image prompt..."):
                    try:
                        setup_gemini(api_key)
                        model = genai.GenerativeModel('gemini-2.0-flash-exp')
                        result = generate_image(prompt, model)

                        st.success("✨ Here's your image prompt!")
                        st.markdown(f'<div class="success-box">{result}</div>', unsafe_allow_html=True)

                        # Copy button
                        st.code(result, language=None)

                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    # Example prompts section
    st.divider()
    st.subheader("💡 Example Prompts to Try")

    examples = [
        ("Nature", "A serene mountain lake at golden hour with misty forests"),
        ("Fantasy", "An enchanted castle floating in the clouds at twilight"),
        ("Tech", "A sleek robot working in a modern laboratory"),
        ("Abstract", "Geometric patterns in vibrant colors flowing like water"),
    ]

    cols = st.columns(4)
    for i, (category, example) in enumerate(examples):
        with cols[i]:
            st.info(f"**{category}**\n\n{example}")

if __name__ == "__main__":
    main()
