import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Bio Writer", page_icon="", layout="centered")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
.stTextInput input, .stTextArea textarea { background: #0f3460 !important; color: white !important; border-radius: 12px; }
.stButton>button { background: linear-gradient(90deg, #9b59b6, #3498db); color: white; border: none; border-radius: 25px; padding: 0.5rem 2rem; font-weight: bold; }
h1, h2, h3 { color: #9b59b6 !important; }
.stSelectbox>div { background: #0f3460 !important; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("  AI Bio Writer")
st.caption("Craft perfect LinkedIn & Twitter bios in seconds")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error(" Set GEMINI_API_KEY in your environment")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input(" Name", placeholder="Your full name")
    title = st.text_input(" Professional Title", placeholder="e.g., Software Engineer")
with col2:
    industry = st.text_input(" Industry", placeholder="e.g., Technology")
    experience = st.number_input(" Years of Experience", min_value=0, max_value=50, value=5)

skills = st.text_area(" Key Skills (comma-separated)", placeholder="Python, JavaScript, Leadership...")
achievements = st.text_area(" Notable Achievements", placeholder="Led team of 10, Increased revenue by 30%...")
platform = st.selectbox(" Platform", ["LinkedIn", "Twitter/X", "Both"])

if st.button("  Generate Bio"):
    if name and title and skills:
        with st.spinner("  Crafting your perfect bio..."):
            prompt = f"""Write a compelling {platform} bio for:
Name: {name}
Title: {title}
Industry: {industry}
Experience: {experience} years
Skills: {skills}
Achievements: {achievements}

For LinkedIn: Professional, 200 chars max, include keywords
For Twitter: Catchy, 160 chars max, engaging tone
Return the bio(s) clearly labeled."""

            try:
                response = model.generate_content(prompt)
                st.success("  Your bio is ready!")
                st.markdown(response.text.replace('\n', '\n\n'))
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("  Please fill in name, title, and skills")

st.markdown("---")
st.markdown("  *Powered by Gemini AI*", unsafe_allow_html=True)
