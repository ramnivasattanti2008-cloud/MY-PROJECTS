"""
AI Scheduler - Create optimal daily schedules with AI
"""
import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# Configure page
st.set_page_config(page_title="AI Scheduler", page_icon="📅", layout="wide")

# Dark theme styles
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
    .schedule-block { background: #0f3460; padding: 15px; border-radius: 10px; margin: 8px 0; border-left: 4px solid #00d9ff; }
    .time-slot { color: #00d9ff; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📅 AI Scheduler")
st.caption("Let AI optimize your day for maximum productivity")

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY not found in environment variables")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Input section
st.subheader("⏰ Your Available Time")
col1, col2 = st.columns(2)

with col1:
    start_time = st.text_input("Start Time", value="09:00")

with col2:
    end_time = st.text_input("End Time", value="18:00")

st.subheader("📋 Tasks to Schedule")
tasks_input = st.text_area("Enter your tasks (one per line)", height=150,
    placeholder="Complete project report\nTeam meeting\nCode review\nLunch break\nEmail responses")

st.subheader("⚡ Priority & Preferences")
col3, col4 = st.columns(2)

with col3:
    focus_areas = st.multiselect("Focus Areas", ["Deep Work", "Meetings", "Admin", "Creative", "Learning"],
        default=["Deep Work"])

with col4:
    energy_level = st.select_slider("Energy Level", options=["Low", "Medium", "High"], value="Medium")

if st.button("🚀 Generate Schedule", type="primary"):
    if not tasks_input.strip():
        st.warning("Please enter at least one task")
    else:
        with st.spinner("Optimizing your schedule..."):
            prompt = f"""Create an optimal daily schedule for {start_time} to {end_time}.

Tasks to schedule:
{tasks_input}

Energy level: {energy_level}
Focus areas: {', '.join(focus_areas)}

Requirements:
- Assign specific time slots to each task
- Include short breaks between tasks (5-15 min)
- Schedule demanding tasks during peak energy hours
- Group similar tasks together
- Include a lunch break
- Be realistic with time estimates

Format as a clear schedule with times and task descriptions."""

            try:
                response = model.generate_content(prompt)
                st.success("Schedule optimized!")

                st.markdown("---")
                st.subheader("📆 Your Optimized Schedule")

                schedule = response.text
                lines = schedule.split('\n')

                for line in lines:
                    if line.strip():
                        # Check for time patterns
                        if any(char.isdigit() for char in line[:10]):
                            st.markdown(f'<div class="schedule-block">{line.strip()}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(line.strip())

            except Exception as e:
                st.error(f"Error generating schedule: {str(e)}")

# Tips
st.markdown("---")
st.markdown("### 💡 Schedule Optimization Tips")
tips = """
- **Morning hours** are best for complex, creative work
- **Batch similar tasks** to minimize context switching
- **Regular breaks** maintain focus and prevent burnout
- **Buffer time** helps handle unexpected tasks
"""
st.info(tips)
