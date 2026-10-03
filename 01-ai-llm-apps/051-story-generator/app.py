import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Story Generator", page_icon="📖", layout="centered")

# Dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .title { text-align: center; color: #f0f6fc; font-size: 2.5rem; margin-bottom: 0.5rem; }
    .subtitle { text-align: center; color: #8b949e; font-size: 1.1rem; margin-bottom: 2rem; }
    .story-box { background-color: #161b22; border-radius: 12px; padding: 20px; border: 1px solid #30363d; margin-top: 20px; }
    .story-text { color: #c9d1d9; line-height: 1.8; font-size: 1.05rem; }
    .char-box { background-color: #1c2128; border-radius: 8px; padding: 15px; margin: 10px 0; border-left: 3px solid #58a6ff; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">📖 AI Story Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Craft magical tales with AI magic</p>', unsafe_allow_html=True)

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Story Settings")
    genre = st.selectbox("✨ Genre", [
        "Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Adventure", "Comedy", "Drama"
    ])
    tone = st.selectbox("🎭 Tone", ["Dark", "Light", "Humorous", "Suspenseful", "Heartwarming"])
    story_length = st.slider("📏 Length", 300, 700, 500, step=50)

    st.markdown("---")
    st.caption("Powered by Google Gemini")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    starting_prompt = st.text_area(
        "✍️ Story Starter",
        placeholder="Once upon a time in a land far away...",
        height=120
    )

with col2:
    main_character = st.text_input("👤 Main Character", placeholder="Enter character name or description")
    setting = st.text_input("🏰 Setting", placeholder="Where does the story take place?")

# Generate button
if st.button("🚀 Generate Story", use_container_width=True, type="primary"):
    if not starting_prompt:
        st.warning("Please provide a story starter prompt!")
    else:
        with st.spinner("✨ Weaving your tale..."):
            try:
                api_key = os.environ.get("GEMINI_API_KEY", "")
                if api_key:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")

                    prompt = f"""Write a creative short story ({story_length} words) in the {genre} genre with a {tone} tone.

Story starter: {starting_prompt}
Main character: {main_character if main_character else 'A compelling protagonist of your creation'}
Setting: {setting if setting else 'A fitting world of your imagination'}

Structure your response exactly like this:
---
TITLE: [Create an engaging title]

CHARACTERS:
- [Character 1 name]: [Brief description and motivation]
- [Character 2 name]: [Brief description and motivation]
- [Character 3 name]: [Brief description if needed]

PLOT POINTS:
1. [Opening - introduce the world and main character]
2. [Rising action - conflict or challenge emerges]
3. [Climax - the pivotal moment]
4. [Falling action - consequences unfold]
5. [Resolution - satisfying conclusion]

THE STORY:
[Write the full {story_length}-word story here, flowing naturally from the starter prompt]
---"""
                    response = model.generate_content(prompt)
                    story = response.text
                else:
                    story = """⚠️ **Demo Mode** - Set `GEMINI_API_KEY` environment variable for real AI generation.

**For now, here's a story template structure:**

📖 **Your Story Preview:**

🎬 **Opening Hook:** {starting_prompt}

👥 **Suggested Characters:**
- A brave hero with a secret past
- A mysterious guide
- An unexpected ally

🎯 **Story Arc:**
1. Introduction - Meet the protagonist
2. The call to adventure
3. Challenges and growth
4. The climactic confrontation
5. A satisfying resolution

*Configure Gemini API key to generate the full story!*""".format(starting_prompt=starting_prompt)

                # Parse and display
                if "TITLE:" in story:
                    parts = story.split("---")
                    for part in parts:
                        if part.strip():
                            st.markdown(f'<div class="story-box"><div class="story-text">{part.strip()}</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="story-box"><div class="story-text">{story}</div></div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error generating story: {str(e)}")

# Footer tips
st.markdown("---")
st.markdown("💡 **Tips:** Be specific with your starter prompt for better results! Try including a conflict or question to spark the narrative.")
