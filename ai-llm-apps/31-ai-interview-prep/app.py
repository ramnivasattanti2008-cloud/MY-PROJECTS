import streamlit as st
import os
import google.genai as genai

st.set_page_config(page_title="AI Interview Prep", page_icon="💼", layout="centered")
st.markdown("""
<style>
.stApp{background:#0e0e1a}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:#1a1a2e;color:#e0e0e0;border:1px solid #333}
.stButton>button{background:linear-gradient(135deg,#6c63ff,#ff6584);color:#fff;border:none;border-radius:8px;padding:.5rem 1.5rem;font-weight:700}
.stSelectbox>div>div{background:#1a1a2e;color:#e0e0e0}
h1,h2,h3{color:#c8c8ff!important}
.css-1v0mbdj img{border-radius:8px}
</style>
""", unsafe_allow_html=True)

st.title("💼 AI Interview Prep Coach")
st.markdown("*Your personal interview assistant — questions, answers, and tips*")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Set `GEMINI_API_KEY` environment variable to use this app.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

with st.sidebar:
    st.header("⚙️ Settings")
    job_role = st.text_input("Job Role / Title", placeholder="e.g. Data Scientist")
    experience = st.selectbox("Experience Level", ["Fresher", "Mid-Level", "Senior", "Lead / Manager"])
    focus = st.multiselect("Focus Areas", ["Technical", "Behavioral", "Situational", "HR/Round 1"], default=["Technical", "Behavioral"])

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("🎯 Interview Questions")
with col2:
    generate = st.button("✨ Generate")

if generate:
    if not job_role:
        st.warning("Please enter a job role in the sidebar.")
    else:
        with st.spinner("Generating interview questions..."):
            prompt = f"""You are an expert interview coach. For the role of **{job_role}** at **{experience}** level, generate 8-10 realistic interview questions covering: {', '.join(focus)}.

For each question provide:
1. The question
2. A strong sample answer (2-3 sentences)
3. A quick tip

Format as markdown with clear sections."""

            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.subheader("📝 Practice Mode")
question_input = st.text_area("Paste a question you got (or want to practice):", height=80)
if st.button("💡 Get Help") and question_input:
    with st.spinner("Thinking..."):
        prompt = f"""As an interview coach, help with this interview question:
"{question_input}"

Provide: a strong answer outline, tips to impress, and common mistakes to avoid."""
        try:
            resp = model.generate_content(prompt)
            st.markdown(resp.text)
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
st.caption("🔑 Uses Google Gemini — ensure `GEMINI_API_KEY` is set in your environment.")
