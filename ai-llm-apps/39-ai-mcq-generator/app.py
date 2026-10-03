import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="MCQ Generator", page_icon="📝", layout="wide")

st.markdown("""
<style>
.stApp{background:#0d1117;color:#e6edf3}
.stTextInput>div>div>input,.stSelectbox>div>div{background:#161b22!important;color:#e6edf3!important;border:1px solid #30363d!important}
.stButton>button{background:#f97316;color:#fff;border:none;padding:0.5rem 2rem;border-radius:8px;font-weight:600}
.stButton>button:hover{background:#fb923c}
.q-card{background:#161b22;padding:1.5rem;border-radius:12px;border:1px solid #30363d;margin:1rem 0}
.q-number{color:#f97316;font-size:1.1rem;font-weight:700}
.answer-key{background:#21262d;padding:1rem;border-radius:8px;margin-top:1rem}
</style>
""", unsafe_allow_html=True)

st.title("📝 AI MCQ Generator")
st.markdown("Generate multiple choice questions instantly for any topic")

col1, col2 = st.columns([1, 1])

with col1:
    topic = st.text_input("📚 Topic", placeholder="e.g., 'Python Programming'")

with col2:
    subject = st.text_input("🎯 Subject Area", placeholder="e.g., 'Data Types and Variables'")

difficulty = st.selectbox("🎚️ Difficulty Level", ["Easy", "Medium", "Hard"])
num_questions = st.slider("❓ Number of Questions", 3, 15, 5)

include_answers = st.checkbox("✅ Include Answer Key", value=True)

if st.button("🔢 Generate Questions", use_container_width=True):
    if topic.strip():
        with st.spinner("Creating questions..."):
            prompt = f"""Generate {num_questions} multiple choice questions.

Topic: {topic}
Subject: {subject if subject else topic}
Difficulty: {difficulty}

Format each question as:
**Q1. [Question text]**
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Answer: [Letter] - [Brief explanation]"""

            response = model.generate_content(prompt)

            questions = response.text.split("**Q")
            for q in questions[1:]:
                st.markdown(f'<div class="q-card"><span class="q-number">**Q{q}</div>', unsafe_allow_html=True)

            if include_answers:
                st.markdown("---")
                st.markdown("### ✅ Answer Key")
                st.markdown('<div class="answer-key">Generated above with each question</div>', unsafe_allow_html=True)
    else:
        st.warning("Please enter a topic")

st.markdown("---")
st.markdown("💡 **Tip:** Specify the subject area for more targeted questions")
