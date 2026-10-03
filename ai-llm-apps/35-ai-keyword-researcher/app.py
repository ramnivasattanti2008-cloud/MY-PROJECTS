import streamlit as st
import os
import google.genai as genai

st.set_page_config(page_title="AI Keyword Researcher", page_icon="🔍", layout="centered")
st.markdown("""
<style>
.stApp{background:#0e0e1a}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:#1a1a2e;color:#e0e0e0;border:1px solid #333;border-radius:8px}
.stButton>button{background:linear-gradient(135deg,#fd79a8,#e84393);color:#fff;border:none;border-radius:8px;padding:.5rem 1.5rem;font-weight:700;font-size:1rem}
h1,h2,h3{color:#fab1a0!important}
.keyword-card{background:#1e1e32;border:1px solid #333;border-radius:12px;padding:16px;margin-bottom:10px}
</style>
""", unsafe_allow_html=True)

st.title("🔍 AI Keyword Researcher")
st.markdown("*Discover SEO keywords and blog post ideas for any topic*")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Set `GEMINI_API_KEY` environment variable to use this app.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

with st.sidebar:
    st.header("🔧 Research Settings")
    topic = st.text_input("Topic / Niche", placeholder="e.g. healthy meal prep")
    content_type = st.selectbox("Content Type", ["Blog Post", "SEO Article", "YouTube Video", "Social Media", "Product Page"])
    target_audience = st.text_input("Target Audience", placeholder="e.g. busy professionals")
    num_keywords = st.slider("Number of Keywords", 5, 30, 15)
    include_questions = st.checkbox("Include Question Keywords", value=True)
    include_longtail = st.checkbox("Include Long-tail Keywords", value=True)

col1, col2 = st.columns(2)
with col1:
    st.metric("📊 Keywords", num_keywords)
with col2:
    st.metric("📝 Content Type", content_type)

st.divider()

if st.button("🚀 Generate Keywords") and topic:
    with st.spinner("Researching keywords..."):
        extras = []
        if include_questions:
            extras.append("question-based keywords (who, what, why, how)")
        if include_longtail:
            extras.append("long-tail keywords (3-5 words)")

        prompt = f"""You are an expert SEO keyword researcher. Research keywords for:
- Topic: **{topic}**
- Target Audience: **{target_audience}**
- Content Type: **{content_type}**

Generate {num_keywords} keywords. Include: {', '.join(extras)} if selected.

Return as markdown with these sections:
1. **Primary Keywords** (high volume, competitive)
2. **Secondary Keywords** (medium volume, moderate competition)
3. **Long-tail Keywords** (low volume, low competition, high intent)
4. **Question Keywords** (FAQ-style, featured snippet opportunities)
5. **Content Ideas** — 3 titles using the best keywords (SEO-friendly, click-worthy)"""

        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)

            st.divider()
            st.subheader("📈 Keyword Difficulty Tips")
            st.markdown("""
- 🔴 **High Difficulty** — Compete with DA 50+ sites, build backlinks first
- 🟡 **Medium Difficulty** — Target with quality content + internal links
- 🟢 **Low Difficulty** — Quick wins, great for new sites
- 💎 **Long-tail** — Low competition, high conversion rate
            """)
        except Exception as e:
            st.error(f"Error: {e}")

elif not topic:
    st.info("👈 Enter a topic in the sidebar to get started.")

st.divider()
st.subheader("📋 Manual Keyword Tracker")

with st.expander("➕ Add keywords to track"):
    tracked = []
    for i in range(5):
        kw = st.text_input(f"Keyword {i+1}", key=f"kw_{i}", placeholder=f"keyword {i+1}")
        if kw:
            tracked.append(kw)

    if tracked:
        st.success(f"Tracking {len(tracked)} keywords:")
        for k in tracked:
            st.markdown(f"- `{k}`")

st.caption("🔑 Uses Google Gemini — set `GEMINI_API_KEY` environment variable.")
