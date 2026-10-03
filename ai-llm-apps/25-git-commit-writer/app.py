import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Git Commit Writer", page_icon="📝", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .commit-box { background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

st.title("📝 Git Commit Writer AI")
st.caption("Paste your git diff, get professional commit messages instantly")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password",
                           value=os.environ.get("GEMINI_API_KEY", ""))
    st.caption("Get your key at [Google AI Studio](https://aistudio.google.com/)")

    st.divider()
    st.subheader("📋 Commit Style")
    commit_type = st.selectbox("Commit Type", ["All Types (Auto-detect)", "feat", "fix", "docs", "style", "refactor", "test", "chore"])
    include_body = st.checkbox("Include Commit Body", value=True)
    conventional = st.checkbox("Conventional Commits Format", value=True)

    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key")

# Main content
st.markdown("### 📄 Paste Your Git Diff")
st.caption("Copy the output of `git diff` or `git diff --staged`")

diff_input = st.text_area(
    "Git Diff Output",
    height=350,
    placeholder="""diff --git a/src/app.py b/src/app.py
index 1234567..89abcdef 100644
--- a/src/app.py
+++ b/src/app.py
@@ -10,6 +10,7 @@ def main():
     print('Hello')
+    print('World')"""
)

col1, col2 = st.columns(2)
with col1:
    scope = st.text_input("Scope (optional)", placeholder="auth, api, ui")
with col2:
    ticket = st.text_input("Ticket/Issue # (optional)", placeholder="JIRA-123")

if st.button("✨ Generate Commit Message", type="primary", disabled=not api_key):
    if not diff_input.strip():
        st.error("❌ Please paste your git diff")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            type_instruction = f"Use commit type: {commit_type}" if commit_type != "All Types (Auto-detect)" else "Detect the most appropriate commit type"
            conventional_instruction = "Use Conventional Commits format (type(scope): description)" if conventional else "Use standard commit message format"

            prompt = f"""Analyze this git diff and generate a professional commit message.

{type_instruction}
{conventional_instruction}
{f'- Scope: {scope}' if scope else ''}
{f'- Related ticket: {ticket}' if ticket else ''}
{f'- Include detailed commit body explaining the why' if include_body else '- Keep it concise'}

Diff:
```
{diff_input}
```

Rules:
- First line: max 72 characters, imperative mood ("Add feature" not "Added feature")
- Use conventional commits format: type(scope): description
- Body: explain what changed and why (if enabled)
- Mention any breaking changes if present
- Be specific, not generic ("Fixed bug" vs "Fix null pointer in auth handler")"""

            with st.spinner("🎨 Writing commit message..."):
                response = model.generate_content(prompt)

            st.success("✅ Commit Message Generated!")

            # Display
            st.markdown("### 📝 Your Commit Message")

            commit_text = response.text.strip()

            # Extract just the commit message if full response
            st.markdown(f"""
            <div class="commit-box">
            <pre>{commit_text}</pre>
            </div>
            """, unsafe_allow_html=True)

            # Copy buttons
            st.code(commit_text, language="bash")

            # One-line version
            first_line = commit_text.split('\n')[0]
            st.info(f"**Quick copy:** `{first_line}`")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.divider()
st.caption("💡 Tip: For best results, stage specific files with `git add` and use `git diff --staged`")
