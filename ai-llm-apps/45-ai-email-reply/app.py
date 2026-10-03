"""
AI Email Reply - Get professional email reply suggestions
"""
import streamlit as st
import google.generativeai as genai
import os

# Configure page
st.set_page_config(page_title="AI Email Reply", page_icon="📧", layout="wide")

# Dark theme styles
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
    .email-card { background: #0f3460; padding: 20px; border-radius: 12px; margin: 12px 0; border-left: 4px solid #27ae60; }
    .email-option { color: #ecf0f1; line-height: 1.7; }
    .label { color: #e74c3c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📧 AI Email Reply")
st.caption("Get professional email response suggestions in one click")

# Initialize Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY not found in environment variables")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Input section
st.subheader("📨 Paste the received email")
email_input = st.text_area("Email content", height=200,
    placeholder="""Hi,

Thanks for reaching out. I wanted to follow up on our conversation about the project timeline. Could we schedule a call this week to discuss the next steps?

Best regards,
[Name]""")

col1, col2 = st.columns(2)

with col1:
    reply_tone = st.selectbox("🎯 Reply Tone",
        ["Professional & Formal", "Friendly & Casual", "Brief & Direct", "Enthusiastic & Positive"])

with col2:
    reply_length = st.selectbox("📏 Length",
        ["Short (<50 words)", "Medium (50-100 words)", "Detailed (>100 words)"])

additional_context = st.text_input("📎 Additional context (optional)",
    placeholder="e.g., Confirming Thursday 3pm meeting, Include attachment link")

if st.button("✉️ Generate Reply Options", type="primary"):
    if not email_input.strip():
        st.warning("Please paste the email you received")
    else:
        with st.spinner("Generating reply options..."):
            context_instruction = f"Also include: {additional_context}" if additional_context else "Focus on the main request in the email"

            prompt = f"""Generate 3 different professional email reply options for the following email:

---
{email_input}
---

Parameters:
- Tone: {reply_tone}
- Length: {reply_length}
- {context_instruction}

Requirements for each option:
1. **Option 1: Concise** - Quick acknowledgment, minimal detail
2. **Option 2: Balanced** - Moderate detail, professional tone
3. **Option 3: Comprehensive** - Full response with all relevant information

Format each option clearly with:
- Clear subject line (if applicable)
- Greeting
- Body
- Professional closing

Label each option clearly."""

            try:
                response = model.generate_content(prompt)
                st.success("Reply options generated!")

                st.markdown("---")
                st.subheader("💬 Choose Your Reply")

                replies = response.text
                sections = replies.split("**Option")

                for i, section in enumerate(sections):
                    if section.strip():
                        if i > 0:
                            st.markdown(f"### Option {section.split('**')[0].strip()}")

                        content = section.split('**')[-1] if '**' in section else section
                        st.markdown(f'<div class="email-card"><div class="email-option">{content.strip()}</div></div>', unsafe_allow_html=True)

                st.session_state.replies = replies

            except Exception as e:
                st.error(f"Error generating replies: {str(e)}")

# Quick templates
st.markdown("---")
st.markdown("### 📝 Quick Reply Templates")
templates = {
    "Acknowledgment": "Thank you for your email. I've received it and will get back to you shortly.",
    "Meeting Request": "Thanks for reaching out. I'd be happy to discuss this further. Could you share your availability this week?",
    "Follow Up": "I wanted to follow up on my previous email. Please let me know if you need any additional information.",
    "Decline": "Thank you for thinking of me. Unfortunately, I'm unable to commit to this at the moment, but I appreciate the opportunity."
}

col1, col2 = st.columns(2)
for i, (template_name, template_text) in enumerate(templates.items()):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"**{template_name}**")
        st.caption(template_text)
