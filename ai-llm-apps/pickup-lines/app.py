import streamlit as st
import google.generativeai as genai
import os
import random

st.set_page_config(page_title="AI Pickup Lines", page_icon="💬", layout="centered")

# Dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .title { text-align: center; color: #f0f6fc; font-size: 2.5rem; margin-bottom: 0.5rem; }
    .subtitle { text-align: center; color: #8b949e; font-size: 1.1rem; margin-bottom: 2rem; }
    .line-card { background: linear-gradient(135deg, #1a1f2e 0%, #161b22 100%); border-radius: 16px; padding: 25px; margin: 15px 0; border: 2px solid #f778ba; box-shadow: 0 8px 32px rgba(247, 120, 186, 0.2); }
    .line-text { color: #f0f6fc; font-size: 1.3rem; text-align: center; font-style: italic; margin-bottom: 15px; }
    .explanation { background-color: #1c2128; padding: 15px; border-radius: 10px; border-left: 4px solid #a371f7; color: #8b949e; }
    .situation-tag { background-color: #a371f7; color: white; padding: 5px 15px; border-radius: 20px; display: inline-block; margin: 5px; }
    .rating { color: #ffd700; font-size: 1.2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">💬 AI Pickup Line Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Get charming, witty, and hilariously smooth lines</p>', unsafe_allow_html=True)

# Pre-built lines for demo mode
demo_lines = [
    {
        "line": "Are you a Wi-Fi signal? Because I'm feeling a connection.",
        "context": "tech/online",
        "explanation": "A classic tech-based pun that's endearing and light-hearted."
    },
    {
        "line": "Do you have a map? I just got lost in your eyes.",
        "context": "general",
        "explanation": "The timeless classic - works in most casual situations."
    },
    {
        "line": "If beauty were time, you'd be an eternity.",
        "context": "romantic",
        "explanation": "A poetic twist on the 'time is precious' concept."
    },
    {
        "line": "Are you French? Because Eiffel for you.",
        "context": "romantic/travel",
        "explanation": "A punny wordplay combining French culture with romance."
    },
    {
        "line": "I'm not a photographer, but I can definitely picture us together.",
        "context": "creative",
        "explanation": "Self-aware humor that shows confidence without being pushy."
    }
]

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Customize")

    situation = st.selectbox("🎯 Situation", [
        "Casual/Bar", "Online/Dating App", "Workplace", "Party/Event",
        "Coffee Shop", "Travel/Adventure", "Art/Museum", "Music Concert", "Sports Event", "Any"
    ])

    style = st.selectbox("🎭 Style", [
        "Witty & Clever", "Cheesy & Fun", "Smooth & Romantic", "Geeky/Nerdy", "Dark Humor", "Self-Deprecating"
    ])

    num_lines = st.slider("📊 Number of Lines", 3, 10, 5)

    include_explanations = st.checkbox("💡 Include Explanations", value=True)
    include_ratings = st.checkbox("⭐ Rate Effectiveness", value=True)

    st.markdown("---")
    st.caption("Powered by Google Gemini")

# Main content
st.subheader("🎨 Tell us about your target")
target_desc = st.text_area(
    "Target Description",
    placeholder="e.g., Bookworm who loves coffee, fitness enthusiast, indie music fan...",
    height=80
)

# Style descriptions
style_emojis = {
    "Witty & Clever": "🧠",
    "Cheesy & Fun": "🧀",
    "Smooth & Romantic": "💋",
    "Geeky/Nerdy": "🤓",
    "Dark Humor": "🌑",
    "Self-Deprecating": "😅"
}

st.info(f"**Selected Style:** {style_emojis.get(style, '✨')} {style}")

# Generate button
if st.button("💘 Generate Pickup Lines", use_container_width=True, type="primary"):
    with st.spinner("🧠 Thinking of something smooth..."):
        try:
            api_key = os.environ.get("GEMINI_API_KEY", "")
            if api_key:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")

                prompt = f"""Generate {num_lines} creative, original pickup lines.

Situation: {situation}
Style: {style}
Target description: {target_desc if target_desc else 'A general, attractive person'}

"""
                if include_explanations:
                    prompt += "Include an explanation for why each line works.\n"
                if include_ratings:
                    prompt += "Rate each line's effectiveness from 1-5 stars.\n"

                prompt += """
Format each line as:
---
LINE [number]
[the pickup line itself, in quotes]
"""
                if include_explanations:
                    prompt += "Why it works: [brief explanation]\n"
                if include_ratings:
                    prompt += "Rating: ⭐⭐⭐⭐⭐ [X/5]\n"
                prompt += "---\n"

                response = model.generate_content(prompt)
                lines = response.text
            else:
                # Demo mode - show pre-built lines
                selected = random.sample(demo_lines, min(num_lines, len(demo_lines)))
                lines = "\n---\n".join([
                    f"LINE {i+1}\n\"{l['line']}\"\nSituation: {l['context']}\nWhy it works: {l['explanation']}\nRating: ⭐⭐⭐ {'⭐' * random.randint(0, 2)}"
                    for i, l in enumerate(selected)
                ])
                lines = "⚠️ **Demo Mode** - Set `GEMINI_API_KEY` for custom lines.\n---\n" + lines

            # Display lines
            parts = lines.split("---")
            for part in parts:
                if part.strip() and "LINE" in part:
                    st.markdown(f'<div class="line-card"><div class="line-text">"{part.strip().split("LINE")[1].strip()}"</div></div>', unsafe_allow_html=True)

            # Also show raw for full content
            st.markdown(lines)

        except Exception as e:
            st.error(f"Error generating lines: {str(e)}")

# Fun stats section
st.markdown("---")
st.subheader("📊 Fun Statistics")

stats_col1, stats_col2, stats_col3 = st.columns(3)

with stats_col1:
    st.metric("Lines Generated", "1,247", "🎉")

with stats_col2:
    success_rate = random.randint(45, 75)
    st.metric("Success Rate", f"{success_rate}%", "💕")

with stats_col3:
    st.metric("Happy Users", "892", "+42 this week")

# Tips section
st.markdown("---")
st.subheader("💡 Pro Tips for Success")

tips_html = """
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;">
    <div style="background-color: #1c2128; padding: 15px; border-radius: 10px; text-align: center;">
        <strong>🎯 Read the Room</strong><br>
        <small>Context matters! Match your line to the situation.</small>
    </div>
    <div style="background-color: #1c2128; padding: 15px; border-radius: 10px; text-align: center;">
        <strong>😏 Confidence is Key</strong><br>
        <small>Delivery beats content every time.</small>
    </div>
    <div style="background-color: #1c2128; padding: 15px; border-radius: 10px; text-align: center;">
        <strong>😂 Don't Take It Too Seriously</strong><br>
        <small>Be ready to laugh it off if needed.</small>
    </div>
</div>
"""
st.markdown(tips_html, unsafe_allow_html=True)

# Disclaimer
st.markdown("---")
st.caption("⚠️ Use responsibly and always respect boundaries. Success not guaranteed! 😄")
