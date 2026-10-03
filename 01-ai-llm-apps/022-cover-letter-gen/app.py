import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Cover Letter Generator", page_icon="✉️")
st.write("""
<style>
.stApp{background:#0d1117;color:#e6edf3}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:#161b22;border:1px solid #30363d;color:#e6edf3;border-radius:8px}
.stButton>button{background:#1f6feb;color:#fff;border:none;border-radius:8px;padding:0.6rem 2rem;font-weight:600}
.stButton>button:hover{background:#388bfd}
.info-box{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:1.5rem}
</style>
""", unsafe_allow_html=True)

st.title("✉️ Cover Letter Generator")
st.caption("Create professional, tailored cover letters in seconds")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    st.caption("Get key at [aistudio.google.com](https://aistudio.google.com)")
    if api_key:
        genai.configure(api_key=api_key)
    st.divider()
    st.caption("Tip: Be specific about your experience for better results.")

st.divider()

with st.container():
    st.subheader("Job Details")
    job_title = st.text_input("Job Title", placeholder="e.g., Senior Software Engineer")
    company = st.text_input("Company Name", placeholder="e.g., Google")
    job_desc = st.text_area("Job Description", placeholder="Paste the job posting here...", height=120)

with st.container():
    st.subheader("Your Background")
    skills = st.text_area("Your Skills & Experience", placeholder="List your relevant skills, years of experience, notable achievements...", height=100)
    tone = st.selectbox("Tone", ["Professional", "Enthusiastic", "Formal", "Casual"])

generate = st.button("Generate Cover Letter", use_container_width=True)

if generate and api_key and job_title and job_desc and skills:
    with st.spinner("Writing your cover letter..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""Write a professional cover letter for:
Job Title: {job_title}
Company: {company}
Tone: {tone}

Job Description:
{job_desc}

Candidate Background:
{skills}

Make it compelling, specific, and不超过 400 words. Start with the company name, highlight relevant experience."""
            response = model.generate_content(prompt)
            st.session_state["letter"] = response.text
        except Exception as e:
            st.error(f"Error: {e}")

if "letter" in st.session_state:
    st.divider()
    st.subheader("Your Cover Letter")
    st.markdown(st.session_state["letter"])
    st.download_button("Download as Text", st.session_state["letter"], "cover_letter.txt", mime="text/plain")
