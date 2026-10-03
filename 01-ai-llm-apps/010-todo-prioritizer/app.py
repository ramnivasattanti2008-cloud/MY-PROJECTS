"""
Todo Prioritizer - AI-powered task prioritization
Uses Gemini AI to analyze and prioritize your tasks
"""

import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Todo Prioritizer",
    page_icon="✅",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #8B5CF6; }
    .sub-header { font-size: 1.2rem; color: #A78BFA; }
    .task-card { background-color: #1E1E2E; padding: 15px; border-radius: 10px; margin: 8px 0; }
    .high-priority { border-left: 4px solid #EF4444; }
    .medium-priority { border-left: 4px solid #F59E0B; }
    .low-priority { border-left: 4px solid #10B981; }
    .reasoning { background-color: #1a1a2e; padding: 15px; border-radius: 10px; margin: 10px 0; }
    .stTextArea > div > div > textarea { background-color: #1E1E2E; }
</style>
""", unsafe_allow_html=True)

# Priority colors
PRIORITY_COLORS = {
    "High": "#EF4444",
    "Medium": "#F59E0B",
    "Low": "#10B981"
}

def get_gemini_api_key(api_key_input: str = None) -> str:
    """Get Gemini API key from various sources"""
    if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
        return st.secrets['GEMINI_API_KEY']
    if os.environ.get('GEMINI_API_KEY'):
        return os.environ.get('GEMINI_API_KEY')
    if api_key_input:
        return api_key_input
    return None

def setup_gemini(api_key: str):
    """Configure Gemini with API key"""
    if api_key:
        genai.configure(api_key=api_key)

def parse_tasks_input(text: str) -> list:
    """Parse task input into list"""
    lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
    tasks = []
    for line in lines:
        # Remove common prefixes like "1.", "-", "*", etc.
        task = line.lstrip('0123456789.-* )').strip()
        if task:
            tasks.append(task)
    return tasks

def prioritize_tasks(tasks: list, model) -> dict:
    """Prioritize tasks using Gemini AI"""
    task_list = '\n'.join([f"{i+1}. {task}" for i, task in enumerate(tasks)])

    prompt = f"""Analyze and prioritize the following tasks. For each task, assign:
1. Priority level: High, Medium, or Low
2. A brief reason for this priority

Consider:
- Deadlines and urgency
- Impact and importance
- Dependencies (some tasks enable others)
- Effort vs value

Tasks:
{task_list}

Format your response as:
TASK: [task name]
PRIORITY: [High/Medium/Low]
REASON: [brief explanation]

Separate each task's analysis with ---

Return analysis for ALL tasks."""

    try:
        response = model.generate_content(prompt)
        return parse_priority_response(response.text, tasks)
    except Exception as e:
        return {"error": str(e)}

def parse_priority_response(text: str, original_tasks: list) -> dict:
    """Parse AI response into structured priorities"""
    result = {
        "tasks": [],
        "reasoning": ""
    }

    current_task = None
    current_priority = None
    current_reason = None

    for line in text.split('\n'):
        line = line.strip()

        if line.startswith('TASK:'):
            if current_task and current_priority:
                result["tasks"].append({
                    "name": current_task,
                    "priority": current_priority,
                    "reason": current_reason or ""
                })
            current_task = line[5:].strip()
            current_priority = None
            current_reason = None
        elif line.startswith('PRIORITY:'):
            current_priority = line[9:].strip()
        elif line.startswith('REASON:'):
            current_reason = line[7:].strip()
        elif line == '---':
            if current_task and current_priority:
                result["tasks"].append({
                    "name": current_task,
                    "priority": current_priority,
                    "reason": current_reason or ""
                })
            current_task = None
            current_priority = None
            current_reason = None

    # Add last task
    if current_task and current_priority:
        result["tasks"].append({
            "name": current_task,
            "priority": current_priority,
            "reason": current_reason or ""
        })

    # If parsing failed, create default structure
    if not result["tasks"] and original_tasks:
        result["tasks"] = [{"name": t, "priority": "Medium", "reason": "Default priority"} for t in original_tasks]
        result["reasoning"] = text

    return result

def display_task(task: dict, index: int):
    """Display a single prioritized task"""
    priority = task.get("priority", "Medium")
    color_class = f"{priority.lower()}-priority"
    color = PRIORITY_COLORS.get(priority, "#8B5CF6")

    with st.container():
        st.markdown(f'<div class="task-card {color_class}">', unsafe_allow_html=True)

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{index}. {task['name']}**")
            if task.get("reason"):
                st.caption(f"💡 {task['reason']}")
        with col2:
            st.markdown(f"<span style='color:{color};font-weight:bold;'>{priority}</span>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<p class="main-header">✅ Todo Prioritizer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered task analysis and prioritization</p>', unsafe_allow_html=True)
    st.divider()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        api_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get your API key from Google AI Studio"
        )

        st.markdown("---")
        st.markdown("""
        **How AI prioritizes:**

        **High Priority:**
        - Urgent deadlines
        - Blocking other tasks
        - High business impact

        **Medium Priority:**
        - Important but not urgent
        - Can be scheduled

        **Low Priority:**
        - Nice to have
        - Can be delegated
        """)

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 Enter Your Tasks")

        tasks_input = st.text_area(
            "Tasks (one per line)",
            placeholder="""Example:
Finish project report
Call dentist
Buy groceries
Study for exam
Clean the house""",
            height=250
        )

        prioritize_btn = st.button("🎯 Prioritize Tasks", type="primary", use_container_width=True)

    # Results
    if prioritize_btn and tasks_input:
        tasks = parse_tasks_input(tasks_input)

        if not tasks:
            st.warning("Please enter at least one task")
        else:
            api_key = get_gemini_api_key(api_key_input)

            if not api_key:
                st.error("⚠️ Please enter your Gemini API key in the sidebar!")
            else:
                with st.spinner("Analyzing and prioritizing..."):
                    try:
                        setup_gemini(api_key)
                        model = genai.GenerativeModel('gemini-2.0-flash-exp')
                        result = prioritize_tasks(tasks, model)

                        if "error" in result:
                            st.error(result["error"])
                        else:
                            st.success(f"✅ Analyzed {len(result['tasks'])} tasks")

                            # Sort by priority
                            priority_order = {"High": 0, "Medium": 1, "Low": 2}
                            sorted_tasks = sorted(
                                result["tasks"],
                                key=lambda x: priority_order.get(x.get("priority", "Medium"), 1)
                            )

                            # Display by priority group
                            for priority in ["High", "Medium", "Low"]:
                                priority_tasks = [t for t in sorted_tasks if t.get("priority") == priority]
                                if priority_tasks:
                                    st.markdown(f"### {priority} Priority ({len(priority_tasks)})")
                                    for i, task in enumerate(priority_tasks, 1):
                                        display_task(task, i)

                            # Show summary
                            high_count = len([t for t in sorted_tasks if t.get("priority") == "High"])
                            medium_count = len([t for t in sorted_tasks if t.get("priority") == "Medium"])
                            low_count = len([t for t in sorted_tasks if t.get("priority") == "Low"])

                            st.divider()
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("High", high_count)
                            with col2:
                                st.metric("Medium", medium_count)
                            with col3:
                                st.metric("Low", low_count)

                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    # Tips section
    st.divider()
    st.subheader("💡 Tips for Best Results")

    tips = st.columns(3)
    with tips[0]:
        st.info("**Be Specific**\n\nInclude deadlines and context for better prioritization")
    with tips[1]:
        st.info("**List All Tasks**\n\nInclude everything you need to do for accurate analysis")
    with tips[2]:
        st.info("**Add Context**\n\nNote dependencies or blockers when relevant")

if __name__ == "__main__":
    main()
