import streamlit as st
import os
import google.genai as genai
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="AI Article Summarizer", page_icon="📰", layout="centered")
st.markdown("""
<style>
.stApp{background:#0e0e1a}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:#1a1a2e;color:#e0e0e0;border:1px solid #333;border-radius:8px}
.stButton>button{background:linear-gradient(135deg,#e17055,#fdcb6e);color:#fff;border:none;border-radius:8px;padding:.5rem 1.5rem;font-weight:700;font-size:1rem}
h1,h2,h3{color:#ffeaa7!important}
</style>
""", unsafe_allow_html=True)

st.title("📰 AI Article Summarizer")
st.markdown("*Paste a URL or text — get a clear, structured summary*")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Set `GEMINI_API_KEY` environment variable to use this app.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

input_mode = st.radio("📥 Input Type", ["🔗 URL", "📝 Paste Text"], horizontal=True)

article_text = ""
if input_mode == "🔗 URL":
    url = st.text_input("🔗 Article URL", placeholder="https://example.com/article")
    if url:
        with st.spinner("Fetching article..."):
            try:
                headers = {"User-Agent": "Mozilla/5.0 (compatible; ArticleBot/1.0)"}
                resp = requests.get(url, timeout=15, headers=headers)
                soup = BeautifulSoup(resp.text, "html.parser")
                for tag in soup(["script", "style", "nav", "footer", "header"]):
                    tag.decompose()
                article_text = " ".join(soup.stripped_strings)
                article_text = article_text[:8000]
                st.success(f"✅ Fetched {len(article_text)} characters")
            except Exception as e:
                st.error(f"Failed to fetch: {e}")
else:
    article_text = st.text_area("📝 Paste article text:", height=200, placeholder="Paste article text here...")

length = st.select_slider("📏 Summary Length", ["Short (3 bullets)", "Medium (5 bullets)", "Long (8 bullets)"], value="Medium (5 bullets)")
include = st.multiselect("Include", ["Key Takeaways", "Main Arguments", "Supporting Evidence", "TL;DR"], default=["Key Takeaways", "Main Arguments"])

if st.button("🧠 Summarize") and article_text:
    with st.spinner("Summarizing..."):
        prompt = f"""Summarize the following article. Include: {', '.join(include)}.

Target length: {length}

Article:
\"\"\"{article_text}\"\"\"

Format the output with clear markdown headers and bullet points."""
        try:
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

st.caption("🔑 Uses Google Gemini — set `GEMINI_API_KEY` environment variable.")
