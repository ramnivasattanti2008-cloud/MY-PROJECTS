import streamlit as st
import os
import google.genai as genai

st.set_page_config(page_title="AI Grammar Check", page_icon="✍️", layout="centered")
st.markdown("""
<style>
.stApp{background:#0e0e1a}
.stTextArea>div>div>textarea{background:#1a1a2e;color:#e0e0e0;border:1px solid #333;border-radius:8px}
.stButton>button{background:linear-gradient(135deg,#00b894,#0984e3);color:#fff;border:none;border-radius:8px;padding:.5rem 2rem;font-weight:700;font-size:1rem}
h1,h2,h3{color:#a8f0c6!important}
</style>
""", unsafe_allow_html=True)

st.title("✍️ AI Grammar & Style Checker")
st.markdown("*Paste your text — get grammar fixes, style improvements, and explanations*")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Set `GEMINI_API_KEY` environment variable to use this app.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

mode = st.radio("📋 Analysis Mode", ["✨ Full Check", "🔍 Grammar Only", "🎨 Style Only"], horizontal=True)
text = st.text_area("📄 Paste your text here:", height=200, placeholder="Type or paste your text...")

if st.button("🔎 Check Text") and text:
    with st.spinner("Analyzing text..."):
        if mode == "✨ Full Check":
            prompt = f"""You are a professional editor. Analyze this text:

"{text}"

Provide:
1. **Corrected Version** — the fixed text
2. **Issues Found** — list each issue with the original problem word/phrase and why it's wrong
3. **Style Suggestions** — improvements for clarity, tone, and engagement
4. **Explanation** — brief note on any key grammar rule applied"""
        elif mode == "🔍 Grammar Only":
            prompt = f"""Check this text for grammar, spelling, and punctuation errors only:

"{text}"

Provide:
1. **Corrected Version**
2. **Issues List** — each error with original → corrected + brief reason"""
        else:
            prompt = f"""Improve the style and clarity of this text without changing meaning:

"{text}"

Provide:
1. **Improved Version**
2. **Style Tips** — what changed and why"""

        try:
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
with st.expander("📚 Grammar Quick Reference"):
    st.markdown("""
| Rule | Example |
|------|---------|
| **Their/There/They're** | Their car (possessive) / There is (place) / They're going (they are) |
| **Than vs Then** | Better than / Then I realized (time) |
| **Affect vs Effect** | Affect (verb: to influence) / Effect (noun: result) |
| **Who vs Whom** | Who did this? (subject) / Whom did you call? (object) |
| **Comma splices** | Two independent clauses need `,and` or `;` or `.` |
    """)

st.caption("🔑 Uses Google Gemini — set `GEMINI_API_KEY` environment variable.")
