"""
Code Reviewer - AI-powered code review with suggestions
Get instant feedback on your code
"""

import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(
    page_title="Code Reviewer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .review-section {background-color: #1a2332; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;}
    .issue-high {border-left: 4px solid #dc3545;}
    .issue-medium {border-left: 4px solid #ffc107;}
    .issue-low {border-left: 4px solid #28a745;}
    .stTextArea > div > div > textarea {font-family: 'Courier New', monospace;}
</style>
""", unsafe_allow_html=True)

LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#",
    "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "SQL", "Other"
]

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        return os.environ.get("GEMINI_API_KEY", "")

def init_gemini(api_key):
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def review_code(model, code, language):
    """Get AI code review"""
    prompt = f"""Review this {language} code and provide feedback.

Code:
```{language}
{code}
```

Provide a structured review with:
1. **Overall Assessment** - Brief summary of code quality
2. **Issues Found** - List any problems (bugs, security issues, performance)
3. **Suggestions** - Specific improvements
4. **Best Practices** - Recommendations

Format issues by severity: HIGH, MEDIUM, LOW
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("🔍 AI Code Reviewer")
    st.caption("Get instant feedback on your code")

    with st.sidebar:
        st.header("⚙️ Settings")
        api_key = get_api_key()

        if not api_key:
            st.warning("Enter your Gemini API key")
            api_key = st.text_input("Gemini API Key", type="password")
            if api_key:
                st.session_state.api_key = api_key
                st.rerun()
        else:
            st.success("API Key loaded")

        st.markdown("---")
        st.markdown("### Review Focus Areas")
        st.markdown("✅ Code Quality")
        st.markdown("✅ Security Issues")
        st.markdown("✅ Performance")
        st.markdown("✅ Best Practices")
        st.markdown("✅ Readability")

    if "api_key" not in st.session_state and api_key:
        st.session_state.api_key = api_key

    if not st.session_state.get("api_key"):
        st.error("Please enter your Gemini API key in the sidebar.")
        return

    if not init_gemini(st.session_state.api_key):
        st.error("Failed to initialize Gemini.")
        return

    model = genai.GenerativeModel('gemini-1.5-flash')

    # Language selection
    language = st.selectbox("📋 Programming Language", LANGUAGES, index=0)

    # Code input
    st.subheader("📝 Paste Your Code")
    code = st.text_area(
        "Enter code to review",
        placeholder="Paste your code here...",
        height=300,
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        review = st.button("🔍 Review Code", type="primary")
    with col2:
        clear = st.button("🗑️ Clear", use_container_width=True)

    if clear:
        st.session_state.review_result = ""
        st.rerun()

    if review and code:
        with st.spinner("Analyzing code..."):
            result = review_code(model, code, language)
            st.session_state.review_result = result

    # Display results
    if st.session_state.get("review_result"):
        st.markdown("---")
        st.subheader("📊 Review Results")
        st.markdown(st.session_state.review_result)

    # Quick tips
    st.markdown("---")
    with st.expander("💡 Quick Tips for Better Reviews"):
        st.markdown("""
        - **Be specific** - Paste complete functions or modules
        - **Include context** - Mention what the code should do
        - **Share imports** - Include necessary imports
        - **Mention constraints** - Python version, ES6+, etc.
        """)

if __name__ == "__main__":
    main()
