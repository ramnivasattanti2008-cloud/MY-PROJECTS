import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="AI Tutor", page_icon="📚")
st.write("""
<style>
.stApp{background:#0d1117;color:#e6edf3}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:#161b22;border:1px solid #30363d;color:#e6edf3;border-radius:8px}
.stSelectbox>div>div>div{background:#161b22;border:1px solid #30363d;border-radius:8px}
.stButton>button{background:#238636;color:#fff;border:none;border-radius:8px;padding:0.5rem 1.5rem;font-weight:600}
.stButton>button:hover{background:#2ea043}
.result-box{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:1.5rem;margin:1rem 0}
.section-header{color:#58a6ff;font-size:1.1rem;font-weight:600;margin-top:1rem}
</style>
""", unsafe_allow_html=True)

st.title("📚 AI Tutor")
st.caption("Generate personalized lessons with key concepts, examples & quizzes")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    st.caption("Get key at [aistudio.google.com](https://aistudio.google.com)")
    if api_key:
        genai.configure(api_key=api_key)

st.divider()

subject = st.text_input("Subject", placeholder="e.g., Mathematics, Physics, History...")
topic = st.text_input("Topic", placeholder="e.g., Quadratic Equations, Newton's Laws...")
difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
generate = st.button("Generate Lesson", use_container_width=True)

if generate and api_key and subject and topic:
    with st.spinner("Creating your lesson..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""Create a comprehensive lesson on {topic} for {subject} at a {difficulty} level.

Include:
1. **Key Concepts**: 5-7 essential concepts with clear explanations
2. **Real-World Examples**: 3 practical examples
3. **Common Mistakes**: 4 things students often get wrong
4. **Quick Quiz**: 5 multiple choice questions with answers

Format with clear headings using markdown."""
            response = model.generate_content(prompt)
            st.session_state["lesson"] = response.text
        except Exception as e:
            st.error(f"Error: {e}")

if "lesson" in st.session_state:
    st.divider()
    st.markdown(st.session_state["lesson"])
