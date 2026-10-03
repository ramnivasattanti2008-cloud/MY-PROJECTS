import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Hashtag Generator", page_icon="", layout="centered")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
.stTextInput, .stTextArea { background: #0f3460 !important; border-radius: 12px !important; }
.stButton>button { background: linear-gradient(90deg, #e94560, #0f3460); color: white; border: none; border-radius: 25px; padding: 0.5rem 2rem; font-weight: bold; }
.stDownloadButton>button { background: linear-gradient(90deg, #00d9ff, #0f3460); color: white; border: none; border-radius: 25px; }
h1, h2, h3 { color: #00d9ff !important; }
</style>
""", unsafe_allow_html=True)

st.title("  Trending Hashtag Generator")
st.caption("AI-powered hashtag suggestions for maximum engagement")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error(" Set GEMINI_API_KEY in your environment variables")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

with st.container():
    st.subheader("  Enter Your Post")
    post_text = st.text_area("", placeholder="Type your tweet or social media post here...", height=120)
    platform = st.selectbox(" Platform", ["Twitter/X", "Instagram", "LinkedIn", "All Platforms"])

    if st.button("  Generate Hashtags"):
        if post_text.strip():
            with st.spinner("  Analyzing trends..."):
                prompt = f"""Based on this social media post, suggest 15 relevant trending hashtags.
Consider the {platform} platform's best practices.
Post: {post_text}

Return ONLY hashtags, one per line, no descriptions.
Example format:
#Trending #Viral #Topic"""

                try:
                    response = model.generate_content(prompt)
                    hashtags = [h.strip() for h in response.text.strip().split('\n') if h.strip()]

                    st.success("  Here are your trending hashtags!")
                    cols = st.columns(3)
                    for i, tag in enumerate(hashtags[:15]):
                        with cols[i % 3]:
                            st.code(tag, language=None)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("  Please enter a post to analyze")

st.markdown("---")
st.markdown("  *Powered by Gemini AI*", unsafe_allow_html=True)
