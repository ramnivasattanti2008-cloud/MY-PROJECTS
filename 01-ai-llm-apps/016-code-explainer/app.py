import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Code Explainer AI", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .code-box { background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Code Explainer AI")
st.caption("Paste any code and get a line-by-line explanation")

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password",
                           value=os.environ.get("GEMINI_API_KEY", ""))
    st.caption("Get your key at [Google AI Studio](https://aistudio.google.com/)")

    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key")

# Main content
code_input = st.text_area(
    "📋 Paste your code here:",
    height=300,
    placeholder="def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
)

language = st.selectbox("💬 Programming Language",
                        ["auto", "Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript", "Ruby", "PHP"])

if st.button("🚀 Explain Code", type="primary", disabled=not api_key):
    if not code_input.strip():
        st.error("❌ Please paste some code to explain")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            prompt = f"""Explain this {language} code line by line in a clear, beginner-friendly way.
For each significant line or block, provide:
- What the code does
- Why it's needed

Code:
```{language}
{code_input}
```"""

            with st.spinner("🧠 Analyzing code..."):
                response = model.generate_content(prompt)

            st.success("✅ Analysis Complete!")
            st.markdown("### 📖 Explanation")
            st.markdown(response.text)

            # Show code in styled box
            st.markdown("### 📄 Original Code")
            st.markdown(f"""
            <div class="code-box">
            <pre><code>{code_input}</code></pre>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()
st.caption("💡 Tip: Include context like variable names and comments for better explanations!")
