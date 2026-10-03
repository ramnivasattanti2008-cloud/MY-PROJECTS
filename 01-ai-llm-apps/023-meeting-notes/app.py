import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

st.set_page_config(page_title="Meeting Notes Organizer", page_icon="📝")
st.write("""
<style>
.stApp{background:#0d1117;color:#e6edf3}
.stTextArea>div>div>textarea{background:#161b22;border:1px solid #30363d;color:#e6edf3;border-radius:8px}
.stButton>button{background:#a371f7;color:#fff;border:none;border-radius:8px;padding:0.6rem 2rem;font-weight:600}
.stButton>button:hover{background:#b87ff0}
.action-item{background:#161b22;border-left:3px solid #238636;padding:0.8rem 1rem;margin:0.5rem 0;border-radius:0 8px 8px 0}
.decision{background:#161b22;border-left:3px solid #1f6feb;padding:0.8rem 1rem;margin:0.5rem 0;border-radius:0 8px 8px 0}
</style>
""", unsafe_allow_html=True)

st.title("📝 Meeting Notes Organizer")
st.caption("Transform rough notes into structured summaries with action items")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    st.caption("Get key at [aistudio.google.com](https://aistudio.google.com)")
    if api_key:
        genai.configure(api_key=api_key)
    st.divider()
    meeting_type = st.selectbox("Meeting Type", ["General", "Standup", "Brainstorm", "Client Call", "Sprint Review"])

st.divider()

meeting_title = st.text_input("Meeting Title", placeholder="e.g., Q4 Planning Session")
notes = st.text_area("Meeting Notes / Transcript", placeholder="Paste your rough notes or transcript here...", height=200)

col1, col2 = st.columns(2)
with col1:
    date = st.date_input("Date", datetime.now())
with col2:
    attendees = st.text_input("Attendees", placeholder="John, Sarah, Mike...")

format_option = st.selectbox("Output Format", ["Full Summary", "Bullet Points", "Executive Brief"])

generate = st.button("Organize Notes", use_container_width=True)

if generate and api_key and notes:
    with st.spinner("Organizing your notes..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""Analyze these meeting notes and create a structured summary.

Meeting: {meeting_title}
Type: {meeting_type}
Date: {date}
Attendees: {attendees}
Format: {format_option}

Notes:
{notes}

Provide:
1. **Summary** - Brief overview of the meeting
2. **Key Discussion Points** - Main topics discussed
3. **Decisions Made** - Clear list of decisions
4. **Action Items** - With owner and deadline if mentioned
5. **Next Steps** - Follow-up items"""
            response = model.generate_content(prompt)
            st.session_state["organized"] = response.text
        except Exception as e:
            st.error(f"Error: {e}")

if "organized" in st.session_state:
    st.divider()
    st.markdown(st.session_state["organized"])
    st.download_button("Export Notes", st.session_state["organized"], f"meeting_notes_{date}.md", mime="text/markdown")
