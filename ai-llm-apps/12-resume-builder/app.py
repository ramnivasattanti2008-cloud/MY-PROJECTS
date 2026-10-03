import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Resume Builder", page_icon="📄", layout="centered")
st.title("📄 AI Resume Builder")
st.markdown("Generate professional resume bullet points")

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password", value=os.environ.get("GEMINI_API_KEY", ""))
    st.markdown("---")
    st.markdown("Get your API key at [Google AI Studio](https://aistudio.google.com/)")

if not api_key:
    st.warning("Please enter your Gemini API key in the sidebar")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Main UI
st.subheader("🎯 Job Details")
job_title = st.text_input("Job Title", placeholder="e.g., Software Engineer, Data Analyst")
experience = st.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior", "Executive"])
skills = st.text_area("Your Skills (comma separated)", placeholder="Python, SQL, Machine Learning, Communication")
achievements = st.text_area("Key Achievements (optional)", placeholder="Any notable accomplishments...")

if st.button("✨ Generate Bullet Points", type="primary") and job_title and skills:
    with st.spinner("Generating resume content..."):
        prompt = f"""Generate professional resume bullet points for:

Job Title: {job_title}
Experience Level: {experience}
Skills: {skills}
Achievements: {achievements if achievements else "Not provided"}

Generate:
1. 5-7 strong action-verb bullet points for work experience
2. 3-4 bullet points highlighting key skills
3. 1-2 bullet points for education/ certifications

Use strong action verbs (Developed, Led, Implemented, Increased, Reduced, etc.)
Quantify achievements where possible.
Make them ATS-friendly and impactful."""

        try:
            response = model.generate_content(prompt)
            st.success("Here are your resume bullet points!")
            st.markdown("### 📋 Work Experience")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("Built with Streamlit & Gemini AI")
