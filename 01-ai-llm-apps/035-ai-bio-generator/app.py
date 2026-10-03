import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Bio Generator", page_icon="👤", layout="wide")

st.markdown("""
<style>
.stApp{background:#0d1117;color:#e6edf3}
.stTextInput>div>div>input,.stSelectbox>div>div{background:#161b22!important;color:#e6edf3!important;border:1px solid #30363d!important}
.stTextArea textarea{background:#161b22!important;color:#e6edf3!important;border:1px solid #30363d!important}
.stButton>button{background:#ec4899;color:#fff;border:none;padding:0.5rem 2rem;border-radius:8px;font-weight:600}
.stButton>button:hover{background:#f472b6}
.bio-card{background:#161b22;padding:1.5rem;border-radius:12px;border:1px solid #30363d;margin:1rem 0;cursor:pointer;transition:all 0.3s}
.bio-card:hover{border-color:#ec4899;transform:translateY(-2px)}
.platform-tag{background:#ec489930;color:#ec4899;padding:0.2rem 0.8rem;border-radius:20px;font-size:0.8rem;display:inline-block;margin-bottom:0.5rem}
.copy-btn{background:#30363d;color:#e6edf3;border:none;padding:0.3rem 1rem;border-radius:6px;cursor:pointer}
</style>
""", unsafe_allow_html=True)

st.title("👤 AI Bio Generator")
st.markdown("Create catchy social media bios for any profession")

col1, col2 = st.columns([1, 1])

with col1:
    profession = st.text_input("💼 Profession", placeholder="e.g., 'Software Engineer'")

with col2:
    personality = st.text_input("🎨 Personality", placeholder="e.g., 'Creative problem solver'")

platform = st.selectbox("📱 Platform", ["Twitter/X", "LinkedIn", "Instagram", "Bio (general)"])
style = st.selectbox("✨ Style", ["Professional", "Casual", "Witty", "Inspirational", "Minimal"])

num_bios = st.slider("🔢 Number of Options", 3, 8, 5)

interests = st.text_area("🏷️ Interests/Hobbies", placeholder="e.g., AI, hiking, coffee, open source")

if st.button("✨ Generate Bios", use_container_width=True):
    if profession.strip():
        with st.spinner("Creating your bios..."):
            prompt = f"""Generate {num_bios} unique social media bios.

Profession: {profession}
Personality: {personality if personality else 'Professional and friendly'}
Platform: {platform}
Style: {style}
Interests: {interests if interests else 'Various'}

Create catchy, engaging bios that:
- Fit the {platform} format (150-300 chars for Twitter)
- Highlight unique strengths
- Include relevant emojis where appropriate
- Sound natural and authentic

Format each as:
**Bio 1:** [Bio text]
---
**Bio 2:** [Bio text]
etc."""

            response = model.generate_content(prompt)
            bios = response.text.split("---")

            st.markdown(f'<span class="platform-tag">{platform}</span>', unsafe_allow_html=True)

            for i, bio in enumerate(bios):
                if bio.strip() and "Bio" in bio:
                    st.markdown(f'<div class="bio-card">{bio.strip()}</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter your profession")

st.markdown("---")
st.markdown("💡 **Tip:** The more personality traits you add, the more unique your bios will be")
