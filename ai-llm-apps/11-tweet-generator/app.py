import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Tweet Generator", page_icon="🐦", layout="centered")
st.title("🐦 AI Tweet Generator")
st.markdown("Generate engaging tweets with hashtag suggestions")

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password", value=os.environ.get("GEMINI_API_KEY", ""))
    st.markdown("---")
    st.markdown("Get your API key at [Google AI Studio](https://aistudio.google.com/)")

if not api_key:
    st.warning("Please enter your Gemini API key in the sidebar")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Main UI
topic = st.text_input("📝 Enter your topic", placeholder="e.g., AI in healthcare, Startup tips, Climate action")
tone = st.selectbox("🎭 Select tone", ["Professional", "Casual", "Humorous", "Inspirational", "Educational"])
count = st.slider("Number of tweets", 1, 5, 3)

if st.button("✨ Generate Tweets", type="primary") and topic:
    with st.spinner("Generating tweets..."):
        prompt = f"""Generate {count} engaging tweets about: {topic}

Tone: {tone}

For each tweet include:
1. The tweet text (max 280 characters)
2. 3-5 relevant hashtags

Format as:
Tweet 1:
[ Tweet text ]
#hashtag1 #hashtag2 #hashtag3

Tweet 2:
...

Make them engaging, original, and suitable for Twitter."""

        try:
            response = model.generate_content(prompt)
            st.success("Here are your tweets!")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("Built with Streamlit & Gemini AI")
