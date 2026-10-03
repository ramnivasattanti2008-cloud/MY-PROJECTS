import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Poem Generator", page_icon="✒️", layout="centered")

# Dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .title { text-align: center; color: #f0f6fc; font-size: 2.5rem; margin-bottom: 0.5rem; }
    .subtitle { text-align: center; color: #8b949e; font-size: 1.1rem; margin-bottom: 2rem; }
    .poem-box { background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 100%); border-radius: 16px; padding: 30px; border: 2px solid #58a6ff; margin-top: 20px; box-shadow: 0 8px 32px rgba(88, 166, 255, 0.15); }
    .poem-text { color: #e6edf3; line-height: 2; font-size: 1.1rem; text-align: center; white-space: pre-wrap; font-family: 'Georgia', serif; }
    .poem-title { color: #58a6ff; font-size: 1.8rem; text-align: center; margin-bottom: 20px; font-style: italic; }
    .mood-tag { background-color: #238636; color: white; padding: 5px 15px; border-radius: 20px; display: inline-block; margin: 5px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">✒️ AI Poem Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform emotions into art</p>', unsafe_allow_html=True)

# Sidebar settings
with st.sidebar:
    st.header("🎨 Poem Settings")

    style = st.selectbox("📝 Style", [
        "Haiku", "Sonnet", "Free Verse", "Limerick", "Ode", "Ballad", "Acrostic"
    ])

    mood = st.selectbox("💭 Mood/Theme", [
        "Love", "Nature", "Melancholy", "Joy", "Mystery", "Adventure",
        "Loneliness", "Hope", "Loss", "Growth", "Dreams", "Time"
    ])

    custom_theme = st.text_input("🎯 Custom Theme", placeholder="Or enter your own...")

    st.markdown("---")
    st.caption("Powered by Google Gemini")

# Display style info
style_descriptions = {
    "Haiku": "🌸 Traditional 3-line Japanese form (5-7-5 syllables)",
    "Sonnet": "📜 14-line poem with elegant rhyme scheme",
    "Free Verse": "🌊 Unstructured, modern expression",
    "Limerick": "🤣 Playful 5-line humorous poem (AABBA)",
    "Ode": "🏛️ Celebratory poem honoring a subject",
    "Ballad": "🎵 Story poem, often with repetition",
    "Acrostic": "🔤 First letters spell a hidden message"
}

st.info(f"**{style}**: {style_descriptions.get(style, '')}")

# Main content
theme_input = custom_theme if custom_theme else mood

col1, col2 = st.columns([2, 1])
with col1:
    emotional_keywords = st.text_area(
        "💝 Emotional Keywords",
        placeholder="joy, sunset, memory, ocean waves...",
        help="Words that capture the feeling you want"
    )
with col2:
    include_title = st.checkbox("✨ Add Title", value=True)
    include_meaning = st.checkbox("📖 Include Interpretation", value=True)

# Generate button
if st.button("🎭 Generate Poem", use_container_width=True, type="primary"):
    if not theme_input:
        st.warning("Please select a mood or enter a custom theme!")
    else:
        with st.spinner("🎨 Crafting your masterpiece..."):
            try:
                api_key = os.environ.get("GEMINI_API_KEY", "")
                if api_key:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")

                    prompt = f"""Write a beautiful, original poem in the {style} format.

Theme/Mood: {theme_input}
Emotional keywords to incorporate: {emotional_keywords if emotional_keywords else 'let your creativity flow'}

"""
                    if include_title:
                        prompt += "Include a creative, evocative title.\n"
                    if include_meaning:
                        prompt += "End with a brief interpretation of the poem's deeper meaning.\n"

                    prompt += """
Format the poem beautifully with proper line breaks. Make it emotionally resonant and memorable.
"""
                    response = model.generate_content(prompt)
                    poem = response.text
                else:
                    poem = f"""⚠️ **Demo Mode** - Set `GEMINI_API_KEY` for real generation.

---

**{theme_input.title()}**

*~ A {style.lower()} in the theme of {theme_input} ~*

*Configure your Gemini API key to generate the full poem...*

---

📖 **Interpretation:**
The poem explores themes of {theme_input.lower()} through evocative imagery and careful word choice.
"""

                st.markdown(f'<div class="poem-box"><div class="poem-text">{poem}</div></div>', unsafe_allow_html=True)

                # Add mood tags
                st.markdown(f"""
                <div style="text-align: center; margin-top: 20px;">
                    <span class="mood-tag">{theme_input}</span>
                    <span class="mood-tag">{style}</span>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error generating poem: {str(e)}")

# Pre-made prompts
st.markdown("---")
st.subheader("🎯 Quick Prompts")
cols = st.columns(4)
quick_prompts = [
    ("🌅 Dawn", "Hope", "Dreams"),
    ("💔 Broken", "Loss", "Melancholy"),
    ("🔥 Passion", "Love", "Joy"),
    ("🌙 Night", "Mystery", "Loneliness")
]
for i, (emoji, mood_val, theme_val) in enumerate(quick_prompts):
    if cols[i].button(f"{emoji}\n{mood_val}"):
        st.session_state.quick_mood = theme_val
        st.rerun()
