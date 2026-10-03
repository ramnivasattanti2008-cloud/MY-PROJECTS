import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Job Description Analyzer", page_icon="📋", layout="wide")

st.markdown("""
<style>
.stApp{background:#0d1117;color:#e6edf3}
.stTextArea textarea{background:#161b22!important;color:#e6edf3!important;border:1px solid #30363d!important}
.stButton>button{background:#238636;color:#fff;border:none;padding:0.5rem 2rem;border-radius:8px;font-weight:600}
.stButton>button:hover{background:#2ea043}
.result-card{background:#161b22;padding:1.5rem;border-radius:12px;border:1px solid #30363d;margin:1rem 0}
.section-title{color:#58a6ff;font-size:1.3rem;font-weight:700;margin:1rem 0 0.5rem}
</style>
""", unsafe_allow_html=True)

st.title("📋 Job Description Analyzer")
st.markdown("Paste a job description and get AI-powered resume improvement suggestions")

col1, col2 = st.columns([1, 1])

with col1:
    job_desc = st.text_area("Paste Job Description", height=400,
        placeholder="Paste the full job description here...")

with col2:
    st.markdown("### 🎯 Analysis Results")
    if st.button("🔍 Analyze Requirements", use_container_width=True):
        if job_desc.strip():
            with st.spinner("Analyzing..."):
                prompt = f"""Analyze this job description and provide:
1. **Key Skills Required** (technical & soft skills)
2. **Experience Level** (entry/mid/senior)
3. **Qualifications** (education, certifications)
4. **Resume Improvement Tips** (specific suggestions)

Job Description:
{job_desc}

Format with clear sections and bullet points."""

                response = model.generate_content(prompt)
                st.markdown(f'<div class="result-card">{response.text}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please paste a job description first")

st.markdown("---")
st.markdown("💡 **Tip:** Copy-paste job postings from LinkedIn, Indeed, or company career pages")
