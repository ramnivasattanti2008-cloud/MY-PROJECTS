import streamlit as st
import os
import google.generativeai as genai
import random

st.set_page_config(page_title="Domain Generator", page_icon="🚀")
st.write("""
<style>
.stApp{background:#0d1117;color:#e6edf3}
.stTextInput>div>div>input{background:#161b22;border:1px solid #30363d;color:#e6edf3;border-radius:8px}
.stButton>button{background:#da3633;color:#fff;border:none;border-radius:8px;padding:0.6rem 2rem;font-weight:600}
.stButton>button:hover{background:#f85149}
.domain-card{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:1.2rem;margin:0.5rem 0}
.tag{background:#1f6feb;padding:0.2rem 0.6rem;border-radius:12px;font-size:0.8rem;color:#fff;display:inline-block;margin:0.2rem}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Domain Name Generator")
st.caption("Discover creative startup domain names with availability hints")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    st.caption("Get key at [aistudio.google.com](https://aistudio.google.com)")
    if api_key:
        genai.configure(api_key=api_key)
    st.divider()
    domain_suffix = st.selectbox("TLD Preference", [".com", ".io", ".ai", ".co", ".app", ".dev"])
    style = st.multiselect("Style", ["Modern", "Catchy", "Descriptive", "Invented", "Playful"], default=["Modern"])

st.divider()

industry = st.text_input("Industry", placeholder="e.g., Fintech, HealthTech, EdTech, E-commerce...")
business_idea = st.text_area("Business Idea / Description", placeholder="Describe your startup in a few sentences...", height=100)
keywords = st.text_input("Key Words (optional)", placeholder="e.g., fast, secure, smart, easy...")
num_suggestions = st.slider("Number of suggestions", 5, 20, 10)

generate = st.button("Generate Domain Ideas", use_container_width=True)

if generate and api_key and industry and business_idea:
    with st.spinner("Brainstorming domain names..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"""Generate {num_suggestions} creative domain name suggestions for a {industry} startup.

Business Description: {business_idea}
Keywords: {keywords or: "innovative, modern"}
Preferred TLD: {domain_suffix}
Styles: {", ".join(style)}

For each domain, provide:
1. The domain name (with TLD)
2. Brief explanation of the name's meaning/strategy
3. Availability hint (High/Medium/Low - estimated)

Format as a list, one per line."""
            response = model.generate_content(prompt)
            st.session_state["domains"] = response.text
            st.session_state["suffix"] = domain_suffix
        except Exception as e:
            st.error(f"Error: {e}")

if "domains" in st.session_state:
    st.divider()
    st.subheader("Suggested Domains")
    st.caption(f"Check availability at your registrar or use WHOIS lookup for {st.session_state['suffix']}")

    for line in st.session_state["domains"].split("\n"):
        if line.strip() and (line[0].isdigit() or "-" in line[:5] or "•" in line or "✓" in line):
            with st.container():
                st.markdown(f"<div class='domain-card'>{line}</div>", unsafe_allow_html=True)

    st.info("Note: Availability hints are estimates. Always verify with your domain registrar.")

st.divider()
st.caption("Tip: Combine AI suggestions with your own brainstorming for the best results.")
