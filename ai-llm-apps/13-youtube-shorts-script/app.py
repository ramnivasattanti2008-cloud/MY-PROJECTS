import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="YouTube Shorts Script", page_icon="🎬", layout="centered")
st.title("🎬 YouTube Shorts Script Generator")
st.markdown("Create engaging Shorts scripts with hook, body & CTA")

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
topic = st.text_input("🎯 Topic", placeholder="e.g., 3 tips to learn coding fast")
style = st.selectbox("🎨 Style", ["Educational", "Entertainment", "Motivational", "How-To", "Trending"])
target_audience = st.text_input("👥 Target Audience", placeholder="e.g., Beginners, Students, Professionals")

col1, col2 = st.columns(2)
with col1:
    duration = st.selectbox("⏱️ Duration", ["15 seconds", "30 seconds", "60 seconds"])
with col2:
    num_scripts = st.radio("📝 Number of scripts", [1, 2, 3], horizontal=True)

if st.button("✨ Generate Script", type="primary") and topic:
    with st.spinner("Creating your Shorts script..."):
        prompt = f"""Generate {num_scripts} YouTube Shorts script(s) for:

Topic: {topic}
Style: {style}
Target Audience: {target_audience if target_audience else 'General'}
Duration: {duration}

For each script, include:
1. **HOOK** (first 3 seconds) - Grab attention immediately
2. **BODY** - Main content in engaging format
3. **CTA** (last 2-3 seconds) - Call to action

Format for each:
---
Script {num}:
[HOOK] - What you say/do in first 3 seconds
[BODY] - The main script content
[CTA] - Like, comment, follow, subscribe
[Captions ideas] - Key text overlays
[Suggested thumbnails] - Thumbnail ideas
---

Keep it punchy, fast-paced, and engaging."""

        try:
            response = model.generate_content(prompt)
            st.success("Here are your Shorts scripts!")
            st.markdown(response.text)
            st.info("💡 Tip: Practice your script timing before recording!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("Built with Streamlit & Gemini AI")
