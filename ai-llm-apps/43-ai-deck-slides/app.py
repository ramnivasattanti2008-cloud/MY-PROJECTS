"""
AI Deck Slides - Generate PowerPoint slide content outlines
"""
import streamlit as st
import google.generativeai as genai
import os

# Configure page
st.set_page_config(page_title="AI Deck Slides", page_icon="📊", layout="wide")

# Dark theme styles
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
    .slide-card { background: #0f3460; padding: 20px; border-radius: 12px; margin: 15px 0; border-top: 3px solid #9b59b6; }
    .slide-number { color: #9b59b6; font-weight: bold; font-size: 1.1em; }
    .bullet-point { color: #ecf0f1; padding-left: 20px; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📊 AI Deck Slides")
st.caption("Generate professional presentation outlines in seconds")

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY not found in environment variables")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Input section
col1, col2 = st.columns([2, 1])

with col1:
    topic = st.text_input("🎯 Presentation Topic", placeholder="e.g., Q4 Business Review, Product Launch")

with col2:
    num_slides = st.slider("Number of Slides", 5, 20, 10)

audience = st.selectbox("👥 Target Audience", ["Executive Leadership", "Business Stakeholders", "Clients", "Team Members", "General Audience"])

purpose = st.selectbox("🎯 Purpose", ["Inform", "Persuade", "Train", "Report", "Pitch"])

col3, col4 = st.columns(2)

with col3:
    include_data = st.checkbox("Include data/statistics slides", value=True)

with col4:
    include_qa = st.checkbox("Include Q&A slide", value=True)

if st.button("✨ Generate Slides", type="primary"):
    if not topic:
        st.warning("Please enter a presentation topic")
    else:
        with st.spinner("Creating your presentation outline..."):
            data_instruction = "Include 2-3 slides with relevant data points and statistics" if include_data else "Focus on qualitative content"
            qa_instruction = "End with a Q&A slide" if include_qa else "End with a call-to-action slide"

            prompt = f"""Create a professional PowerPoint presentation outline for: "{topic}"

Parameters:
- Number of slides: {num_slides}
- Target audience: {audience}
- Purpose: {purpose}
- {data_instruction}
- {qa_instruction}

For each slide provide:
1. Slide title
2. Key points (3-5 bullet points)
3. Suggested visual element

Structure:
- Title slide
- Agenda/Overview
- Main content slides (organized by theme)
- Conclusion
- {qa_instruction.split("End with ")[1] if include_qa else "Thank you slide"}

Format clearly with slide numbers."""

            try:
                response = model.generate_content(prompt)
                st.success("Slides generated successfully!")

                st.markdown("---")
                st.subheader("📑 Your Presentation Outline")

                slides = response.text
                lines = slides.split('\n')
                current_slide = 0

                for line in lines:
                    if line.strip():
                        stripped = line.strip()
                        if stripped.startswith('#') or stripped.startswith('Slide'):
                            st.markdown(f"### {stripped}")
                        elif stripped.startswith(('•', '-', '*', '>')):
                            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{stripped}")
                        else:
                            st.markdown(stripped)

                # Export options
                st.markdown("---")
                st.session_state.slides = slides

            except Exception as e:
                st.error(f"Error generating slides: {str(e)}")

# Tips
st.markdown("---")
st.markdown("### 💡 Presentation Tips")
tips = """
- **One idea per slide** keeps audiences focused
- **Visuals beat text** - use images, not paragraphs
- **Start strong** - your opening determines engagement
- **End with action** - give a clear next step
"""
st.info(tips)
