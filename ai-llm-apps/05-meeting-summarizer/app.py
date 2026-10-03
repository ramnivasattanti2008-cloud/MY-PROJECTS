"""
Meeting Summarizer - AI-powered meeting notes summarizer
Extract key points, summaries, and action items from meeting notes
"""

import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

st.set_page_config(
    page_title="Meeting Summarizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .summary-box {background-color: #1a2332; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0;}
    .action-item {background-color: #1a2332; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ffc107;}
    .key-point {background-color: #1a2332; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #28a745;}
</style>
""", unsafe_allow_html=True)

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        return os.environ.get("GEMINI_API_KEY", "")

def init_gemini(api_key):
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def summarize_meeting(model, notes):
    """Summarize meeting notes"""
    prompt = f"""Analyze these meeting notes and provide a structured summary:

Meeting Notes:
{notes}

Provide:
1. **Executive Summary** - 2-3 sentence overview
2. **Key Points Discussed** - Main topics (bullet points)
3. **Decisions Made** - Any decisions reached
4. **Action Items** - Tasks assigned with who should do them
5. **Next Steps** - Follow-up items or future plans

Format action items as:
- [Task] - [Assigned to/Who] - [Deadline if mentioned]
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def extract_decisions(model, notes):
    """Extract key decisions from notes"""
    prompt = f"""Extract all decisions made in this meeting:

{notes}

List each decision clearly.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def generate_minutes(model, notes):
    """Generate formal meeting minutes"""
    prompt = f"""Convert these meeting notes into formal meeting minutes:

{notes}

Include:
- Meeting Date/Time (if mentioned)
- Attendees (if mentioned)
- Agenda
- Discussion Summary
- Decisions
- Action Items
- Next Meeting (if mentioned)
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("📝 Meeting Summarizer")
    st.caption("Extract insights from your meeting notes")

    with st.sidebar:
        st.header("⚙️ Settings")
        api_key = get_api_key()

        if not api_key:
            st.warning("Enter your Gemini API key")
            api_key = st.text_input("Gemini API Key", type="password")
            if api_key:
                st.session_state.api_key = api_key
                st.rerun()
        else:
            st.success("API Key loaded")

        st.markdown("---")
        st.markdown("### Output Options")
        st.markdown("📋 **Full Summary** - Complete analysis")
        st.markdown("✅ **Decisions Only** - Key decisions")
        st.markdown("📄 **Meeting Minutes** - Formal format")

    if "api_key" not in st.session_state and api_key:
        st.session_state.api_key = api_key

    if not st.session_state.get("api_key"):
        st.error("Please enter your Gemini API key in the sidebar.")
        return

    if not init_gemini(st.session_state.api_key):
        st.error("Failed to initialize Gemini.")
        return

    model = genai.GenerativeModel('gemini-1.5-flash')

    # Output format selection
    output_type = st.radio(
        "📊 Output Format",
        ["Full Summary", "Decisions Only", "Meeting Minutes"],
        horizontal=True
    )

    # Notes input
    st.subheader("📝 Paste Meeting Notes")
    meeting_notes = st.text_area(
        "Enter meeting notes, transcript, or rough notes",
        placeholder="""Paste your meeting notes here...

Example format:
Meeting: Sprint Planning
Date: Sept 6, 2026
Attendees: John, Sarah, Mike

Discussed:
- Q4 roadmap priorities
- Resource allocation for new features
- Timeline for product launch

Decisions:
- Focus on mobile app first
- Hire 2 more developers

Action Items:
- Sarah to update roadmap doc
- Mike to schedule interviews
- Review sprint on Sept 13""",
        height=300,
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        summarize = st.button("✨ Summarize", type="primary")
    with col2:
        clear = st.button("🗑️ Clear", use_container_width=True)

    if clear:
        st.session_state.summary = ""
        st.rerun()

    if summarize and meeting_notes:
        with st.spinner("Analyzing meeting notes..."):
            if output_type == "Full Summary":
                result = summarize_meeting(model, meeting_notes)
            elif output_type == "Decisions Only":
                result = extract_decisions(model, meeting_notes)
            else:
                result = generate_minutes(model, meeting_notes)
            st.session_state.summary = result

    # Display results
    if st.session_state.get("summary"):
        st.markdown("---")

        if output_type == "Full Summary":
            st.subheader("📋 Meeting Summary")
        elif output_type == "Decisions Only":
            st.subheader("✅ Key Decisions")
        else:
            st.subheader("📄 Meeting Minutes")

        st.markdown(st.session_state.summary)

    # Tips
    st.markdown("---")
    with st.expander("💡 Tips for Better Summaries"):
        st.markdown("""
        - Include meeting title and date
        - List attendees names
        - Note any deadlines or timelines
        - Include specific task assignments
        - Add context for decisions made
        """)

if __name__ == "__main__":
    main()
