import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(page_title="Code Documenter", page_icon="📄")
st.write("""
<style>
.stApp{background:#0d1117;color:#e6edf3}
.stTextArea>div>div>textarea{background:#161b22;border:1px solid #30363d;color:#e6edf3;border-radius:8px;font-family:'Courier New',monospace}
.stButton>button{background:#f0883e;color:#fff;border:none;border-radius:8px;padding:0.6rem 2rem;font-weight:600}
.stButton>button:hover{background:#f49b56}
.code-block{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:1rem;font-family:'Courier New',monospace;overflow-x:auto}
</style>
""", unsafe_allow_html=True)

st.title("📄 Code Documenter")
st.caption("Generate comprehensive documentation for your code instantly")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    st.caption("Get key at [aistudio.google.com](https://aistudio.google.com)")
    if api_key:
        genai.configure(api_key=api_key)
    st.divider()
    doc_style = st.selectbox("Doc Style", ["Google", "JSDoc", "NumPy", "Sphinx", "Simple"])
    include_examples = st.checkbox("Include Examples", value=True)
    explain_complex = st.checkbox("Explain Complex Logic", value=True)

st.divider()

language = st.selectbox("Language", ["Python", "JavaScript", "TypeScript", "Java", "Go", "Rust", "C++", "Ruby", "Other"])
code = st.text_area("Paste Your Code", placeholder="Paste your code here...", height=300, key="code_input")

generate = st.button("Generate Documentation", use_container_width=True)

if generate and api_key and code:
    with st.spinner("Documenting your code..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""Generate comprehensive documentation for this {language} code using {doc_style} style.

Requirements:
- {"Include usage examples" if include_examples else "Omit examples"}
- {"Explain complex logic in comments" if explain_complex else ""}

Code:
```{language.lower()}
{code}
```

Provide:
1. **File/Module Description** - What does this do?
2. **Function/Class Documentation** - Each with:
   - Description
   - Parameters (name, type, description)
   - Returns (type, description)
   - Raises (exceptions)
   - Notes/Warnings
3. **Usage Examples** - Minimal and advanced
4. **Complexity Notes** - Explain any non-obvious logic"""
            response = model.generate_content(prompt)
            st.session_state["docs"] = response.text
        except Exception as e:
            st.error(f"Error: {e}")

if "docs" in st.session_state:
    st.divider()
    st.markdown(st.session_state["docs"])
    st.download_button("Download Documentation", st.session_state["docs"], "documentation.md", mime="text/markdown")
