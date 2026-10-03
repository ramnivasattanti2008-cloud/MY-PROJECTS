import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="LinkedIn Post Generator", page_icon="", layout="centered")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1a1a2e 0%, #0077b5 100%); }
.stTextInput input, .stTextArea textarea { background: #0f3460 !important; color: white !important; border-radius: 12px; }
.stButton>button { background: linear-gradient(90deg, #0077b5, #00a8e8); color: white; border: none; border-radius: 25px; padding: 0.5rem 2rem; font-weight: bold; }
h1, h2 { color: #00a8e8 !important; }
.stSelectbox>div { background: #0f3460 !important; border-radius: 12px; }
.stSuccess { background: #0f3460 !important; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("  LinkedIn Post Generator")
st.caption("Create engaging professional posts with AI")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error(" Set GEMINI_API_KEY in your environment")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

topic = st.text_input(" Post Topic", placeholder="e.g., 5 lessons from my first year as a startup founder")
tone = st.selectbox(" Tone", ["Professional", "Inspirational", "Educational", "Storytelling", "Bold"])
length = st.selectbox(" Length", ["Short (150-200 chars)", "Medium (200-400 chars)", "Long (400-600 chars)"])

include_cta = st.checkbox(" Include Call-to-Action")
include_emoji = st.checkbox(" Use Emojis")
industry = st.text_input(" Industry (optional)", placeholder="e.g., Tech, Finance, Healthcare")

if st.button("  Generate Post"):
    if topic:
        with st.spinner("  Crafting your LinkedIn post..."):
            length_hint = {"Short": "150-200", "Medium": "200-400", "Long": "400-600"}.get(length.split()[0], "200-400")
            cta_hint = "Include a clear call-to-action at the end asking readers to comment or share" if include_cta else "No call-to-action needed"
            emoji_hint = "Use relevant emojis throughout" if include_emoji else "No emojis"

            prompt = f"""Write a viral-worthy LinkedIn post:
Topic: {topic}
Industry: {industry if industry else "General business"}
Tone: {tone}
Target length: {length_hint} characters
Style: {cta_hint}. {emoji_hint}.

Structure:
1. Hook (first line to grab attention)
2. Body (main content with value)
3. Key takeaways (bullet points)
4. Call-to-action (if requested)
5. Relevant hashtags (3-5 max)

Make it engaging, authentic, and professional. No clickbait."""

            try:
                response = model.generate_content(prompt)
                st.success("  Your LinkedIn post is ready!")
                st.markdown("---")
                st.markdown(response.text.replace('\n', '\n\n'))
                st.markdown("---")

                char_count = len(response.text)
                st.caption(f" Character count: {char_count}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("  Please enter a topic")

st.markdown("---")
st.markdown("  *Powered by Gemini AI*", unsafe_allow_html=True)
