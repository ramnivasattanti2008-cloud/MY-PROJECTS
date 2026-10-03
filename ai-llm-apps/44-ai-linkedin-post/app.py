"""
AI LinkedIn Post - Write engaging LinkedIn posts with AI
"""
import streamlit as st
import google.generativeai as genai
import os

# Configure page
st.set_page_config(page_title="AI LinkedIn Post", page_icon="💼", layout="wide")

# Dark theme styles
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
    .post-box { background: #0f3460; padding: 25px; border-radius: 15px; margin: 15px 0; line-height: 1.8; }
    .hook { color: #f39c12; font-weight: bold; font-size: 1.1em; }
    .hashtag { color: #3498db; }
    .section-label { color: #2ecc71; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("💼 AI LinkedIn Post")
st.caption("Create viral-worthy LinkedIn content that engages and converts")

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY not found in environment variables")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Input section
st.subheader("📝 What do you want to share?")
topic = st.text_area("Your idea, experience, or topic", height=120,
    placeholder="e.g., I just launched my first product\nor: Tips for remote work productivity\nor: Lessons from 5 years in tech")

col1, col2 = st.columns(2)

with col1:
    tone = st.selectbox("🎨 Tone", ["Professional", "Inspirational", "Educational", "Conversational", "Storytelling"])

with col2:
    post_length = st.selectbox("📏 Length", ["Short (<150 chars)", "Medium (150-300 chars)", "Long (300-500 chars)"])

industry = st.selectbox("🏢 Industry", ["Technology", "Business", "Marketing", "Finance", "Healthcare", "Education", "General"])

if st.button("✍️ Generate Post", type="primary"):
    if not topic:
        st.warning("Please share your idea or topic")
    else:
        with st.spinner("Crafting your LinkedIn post..."):
            prompt = f"""Write an engaging LinkedIn post based on:

Topic/Idea: "{topic}"
Tone: {tone}
Length: {post_length}
Industry: {industry}

Requirements:
1. Start with a POWERFUL hook (first 2-3 lines must grab attention)
2. Use the "hook, story, value, call-to-action" structure
3. Include 4-6 relevant hashtags at the end
4. Write in first person for authenticity
5. Add 2-3 line breaks for readability
6. Make it relatable and actionable
7. End with a question or call-to-action to drive engagement

Format the response with clear labels for each section."""

            try:
                response = model.generate_content(prompt)
                st.success("Post generated!")

                st.markdown("---")
                st.subheader("📱 Your LinkedIn Post")

                post = response.text
                st.markdown(f'<div class="post-box">{post}</div>', unsafe_allow_html=True)

                # Copy button
                st.button("📋 Copy to Clipboard", key="copy_btn")

                st.session_state.generated_post = post

            except Exception as e:
                st.error(f"Error generating post: {str(e)}")

# Best practices
st.markdown("---")
st.markdown("### 🚀 LinkedIn Best Practices")
tips = """
| Element | Tip |
|---------|-----|
| **Hook** | Start with a question, number, or bold statement |
| **Timing** | Post Tuesday-Thursday, 8-10 AM or 5-6 PM |
| **Engagement** | Reply to every comment within the first hour |
| **Hashtags** | Use 3-5 relevant + 1 trending hashtag |
"""
st.table({"Tip": ["Start with hook", "Best timing", "Engage quickly", "Hashtag strategy"],
          "Details": ["Question, number, or bold statement", "Tue-Thu, 8-10 AM or 5-6 PM", "Reply to comments within 1 hour", "3-5 relevant + 1 trending"]})
