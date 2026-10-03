import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Music Lyrics Generator", page_icon="🎵", layout="wide")

st.markdown("""
<style>
.stApp{background:#0d1117;color:#e6edf3}
.stTextArea textarea,.stTextInput>div>div>input{background:#161b22!important;color:#e6edf3!important;border:1px solid #30363d!important}
.stSelectbox>div>div{background:#161b22!important}
.stButton>button{background:#a371f7;color:#fff;border:none;padding:0.5rem 2rem;border-radius:8px;font-weight:600}
.stButton>button:hover{background:#b98ef8}
.lyrics-box{background:#161b22;padding:1.5rem;border-radius:12px;border:1px solid #30363d;margin:1rem 0;font-style:italic;white-space:pre-wrap}
</style>
""", unsafe_allow_html=True)

st.title("🎵 AI Music Lyrics Generator")
st.markdown("Create original song lyrics with AI - just describe your mood or theme")

col1, col2 = st.columns([1, 1])

with col1:
    theme = st.text_input("🎭 Theme/Mood", placeholder="e.g., 'Heartbreak and healing'")
    topic = st.text_input("📖 Story/Topic", placeholder="e.g., 'Moving on after a breakup'")

with col2:
    genre = st.selectbox("🎸 Music Genre", [
        "Pop", "Rock", "Hip-Hop/Rap", "R&B", "Country", "Ballad", "EDM", "Indie", "Folk"
    ])
    style = st.selectbox("🎤 Song Style", [
        "Storytelling", "Emotional", "Upbeat", "Melancholic", "Nostalgic", "Empowering"
    ])

lines = st.slider("📝 Number of Verses", 2, 6, 4)

if st.button("🎤 Generate Lyrics", use_container_width=True):
    if theme.strip() or topic.strip():
        with st.spinner("Composing lyrics..."):
            prompt = f"""Write original song lyrics with {lines} verses.

Theme/Mood: {theme if theme else 'General'}
Story/Topic: {topic if topic else 'Express the given mood'}
Genre: {genre}
Style: {style}

Include:
- Verse(s) with storytelling and emotional depth
- A memorable chorus that repeats
- Clear structure with line breaks
- Rhyming where appropriate"""

            response = model.generate_content(prompt)
            st.markdown(f'<div class="lyrics-box">{response.text}</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a theme or topic")

st.markdown("---")
st.markdown("🎹 **Tip:** Combining a specific mood + story creates more compelling lyrics")
