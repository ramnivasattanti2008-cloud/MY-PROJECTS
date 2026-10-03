"""
AI Outliner - Generate structured outlines for essays, articles, and blog posts
"""
import streamlit as st
import google.generativeai as genai
import os

# Configure page
st.set_page_config(page_title="AI Outliner", page_icon="📝", layout="wide")

# Dark theme styles
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
    .outline-box { background: #0f3460; padding: 20px; border-radius: 12px; border-left: 4px solid #e94560; margin: 10px 0; }
    .section-header { color: #e94560; font-weight: bold; font-size: 1.2em; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📝 AI Outliner")
st.caption("Transform your ideas into structured, compelling content")

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
    topic = st.text_input("📌 Enter your topic or title", placeholder="e.g., The Future of AI in Education")

with col2:
    content_type = st.selectbox("📄 Content Type", ["Essay", "Article", "Blog Post", "Research Paper", "Report"])

if st.button("✨ Generate Outline", type="primary"):
    if not topic:
        st.warning("Please enter a topic")
    else:
        with st.spinner("Creating your outline..."):
            prompt = f"""Create a detailed, well-structured outline for a {content_type} on the topic: "{topic}"

Requirements:
- Include an engaging introduction hook
- 4-6 main sections with subsections
- Each section should have 2-4 sub-points
- Include a conclusion with key takeaways
- Use clear hierarchical structure

Format the outline with proper indentation and numbering.
Keep it practical and easy to follow."""

            try:
                response = model.generate_content(prompt)
                st.success("Outline generated successfully!")

                st.markdown("---")
                st.subheader("📋 Your Outline")

                # Display formatted outline
                outline = response.text
                lines = outline.split('\n')

                for line in lines:
                    if line.strip():
                        if line.strip().startswith(('#', 'Introduction', 'Conclusion', 'Section', 'Part')):
                            st.markdown(f"**{line.strip()}**")
                        elif line.strip().startswith(('•', '-', '*')):
                            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{line.strip()}")
                        else:
                            st.markdown(line.strip())

                # Copy button
                st.session_state.outline = outline

            except Exception as e:
                st.error(f"Error generating outline: {str(e)}")

# Tips section
st.markdown("---")
st.markdown("### 💡 Tips for Great Outlines")
tips = """
- **Be specific** - Narrow down your topic for focused content
- **Structure matters** - Logical flow keeps readers engaged
- **Add depth** - Include sub-points that add value
"""
st.info(tips)
