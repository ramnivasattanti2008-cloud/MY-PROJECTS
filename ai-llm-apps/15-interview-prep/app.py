import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Interview Prep", page_icon="💼", layout="centered")
st.title("💼 AI Interview Prep")
st.markdown("Generate practice questions and sample answers")

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
st.subheader("🎯 Job Role Details")
job_role = st.text_input("Job Role", placeholder="e.g., Software Engineer, Data Scientist, Product Manager")
industry = st.selectbox("🏭 Industry", ["Technology", "Finance", "Healthcare", "Consulting", "Marketing", "Education", "Retail", "Other"])
experience = st.selectbox("📊 Experience Level", ["Entry Level", "Mid Level", "Senior", "Executive"])
interview_type = st.multiselect("📋 Interview Type", ["Technical", "Behavioral", "HR/HR", "Case Study", "System Design"], default=["Behavioral", "Technical"])

if st.button("✨ Generate Questions", type="primary") and job_role:
    with st.spinner("Generating interview questions..."):
        prompt = f"""Generate interview preparation material for:

Role: {job_role}
Industry: {industry}
Experience: {experience}
Interview Types: {', '.join(interview_type)}

Provide:
1. **5 Common Questions** - Most frequently asked questions
2. **Sample Answers** - Strong, detailed answers with STAR method for behavioral questions
3. **Technical Questions** - Role-specific technical questions (if applicable)
4. **Red Flags to Avoid** - Common mistakes candidates make
5. **Pro Tips** - How to stand out in the interview

Format clearly with sections and use the STAR method (Situation, Task, Action, Result) for behavioral answers."""

        try:
            response = model.generate_content(prompt)
            st.success("Here are your interview questions!")
            st.markdown(response.text)
            st.info("💡 Tip: Practice answering out loud for best results!")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Tips section
st.markdown("---")
st.subheader("📚 Quick Interview Tips")
tips = {
    "🗣️ Communication": "Speak clearly and structure your answers",
    "📊 STAR Method": "Situation, Task, Action, Result for behavioral questions",
    "❓ Ask Questions": "Always have thoughtful questions ready",
    "🔍 Research": "Know the company and role inside out",
    "💪 Body Language": "Maintain eye contact and confident posture"
}
for tip, desc in tips.items():
    st.markdown(f"**{tip}**: {desc}")

st.markdown("---")
st.caption("Built with Streamlit & Gemini AI")
