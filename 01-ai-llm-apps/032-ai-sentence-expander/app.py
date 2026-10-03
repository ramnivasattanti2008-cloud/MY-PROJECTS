import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Sentence Expander", page_icon="✍️", layout="wide")

st.markdown("""
<style>
.stApp{background:#0d1117;color:#e6edf3}
.stTextArea textarea,.stTextInput>div>div>input{background:#161b22!important;color:#e6edf3!important;border:1px solid #30363d!important}
.stSelectbox>div>div{background:#161b22!important}
.stButton>button{background:#1f6feb;color:#fff;border:none;padding:0.5rem 2rem;border-radius:8px;font-weight:600}
.stButton>button:hover{background:#388bfd}
.expanded-box{background:#161b22;padding:1.5rem;border-radius:12px;border:1px solid #30363d;margin:1rem 0;line-height:1.8}
.word-count{color:#8b949e;font-size:0.9rem}
</style>
""", unsafe_allow_html=True)

st.title("✍️ AI Sentence Expander")
st.markdown("Transform short phrases into compelling full paragraphs")

input_phrase = st.text_input("📝 Enter your short phrase", placeholder="e.g., 'Climate change affects everyone'")
tone = st.selectbox("🎨 Writing Tone", ["Formal", "Casual", "Persuasive", "Academic", "Creative"])

length = st.slider("📏 Target Length (words)", 50, 300, 150)

use_cases = st.multiselect("📂 Use Case", ["Essay", "Article", "Blog Post", "Report", "Speech"],
    default=["Essay"])

if st.button("✨ Expand Sentence", use_container_width=True):
    if input_phrase.strip():
        with st.spinner("Expanding..."):
            prompt = f"""Expand this phrase into a well-structured paragraph suitable for a {use_cases[0].lower()}.
Tone: {tone}
Target length: ~{length} words

Phrase: {input_phrase}

Write a cohesive, engaging paragraph that expands on this idea with supporting details and context."""

            response = model.generate_content(prompt)
            st.markdown(f'<div class="expanded-box">{response.text}</div>', unsafe_allow_html=True)
            st.markdown(f'<p class="word-count">~{len(response.text.split())} words</p>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a phrase to expand")

st.markdown("---")
st.markdown("💡 **Tip:** The more specific your phrase, the better the expansion")
