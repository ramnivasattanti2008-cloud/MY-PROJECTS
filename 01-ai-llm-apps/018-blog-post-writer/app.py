import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Blog Post Writer", page_icon="✍️", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .blog-section { background-color: #161b22; padding: 20px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #58a6ff; }
</style>
""", unsafe_allow_html=True)

st.title("✍️ Blog Post Writer AI")
st.caption("Generate professional blog post outlines with structure and content ideas")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password",
                           value=os.environ.get("GEMINI_API_KEY", ""))
    st.caption("Get your key at [Google AI Studio](https://aistudio.google.com/)")

    st.divider()
    st.subheader("📝 Output Options")
    include_intro = st.checkbox("Include Introduction", value=True)
    include_conclusion = st.checkbox("Include Conclusion", value=True)
    target_length = st.selectbox("Target Length", ["Short (500 words)", "Medium (1000 words)", "Long (2000 words)"])
    tone = st.selectbox("Writing Tone", ["Professional", "Casual", "Friendly", "Authoritative", "Conversational"])

    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key")

# Main content
st.markdown("### 🎯 Enter Your Blog Topic")
topic = st.text_input(
    "Topic",
    placeholder="Example: The Future of Remote Work in 2025"
)

col1, col2 = st.columns(2)
with col1:
    target_audience = st.text_input("Target Audience", placeholder="Tech professionals, small business owners")
with col2:
    keywords = st.text_input("SEO Keywords (comma-separated)", placeholder="remote work, productivity, work-life balance")

blog_style = st.selectbox("Blog Style", ["How-to/Tutorial", "Listicle", "Opinion/Editorial", "News/Announcement", "Comparison"])

if st.button("🚀 Generate Outline", type="primary", disabled=not api_key):
    if not topic.strip():
        st.error("❌ Please enter a blog topic")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""Create a detailed blog post outline for: {topic}

Requirements:
- Style: {blog_style}
- Tone: {tone}
- Length: {target_length}
{f'- Target audience: {target_audience}' if target_audience else ''}
{f'- Include SEO keywords: {keywords}' if keywords else ''}

Format the output as:
1. **Title** (SEO-optimized)
2. **Meta Description** (155 characters max)
3. **Introduction** (hook + what readers will learn)
4. **Main Sections** (H2 headings with 2-3 sub-points each)
5. **Conclusion** (summary + call-to-action)
6. **Suggested Featured Image Description**

Keep it actionable and engaging."""

            with st.spinner("✍️ Creating your outline..."):
                response = model.generate_content(prompt)

            st.success("✅ Outline Generated!")
            st.markdown("### 📋 Your Blog Post Outline")
            st.markdown(f"""
            <div class="blog-section">
            {response.text.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

            # Also show as markdown
            st.markdown("---")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()
st.caption("💡 Tip: Be specific with your topic for better, more targeted outlines!")
