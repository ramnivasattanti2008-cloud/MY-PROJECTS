import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="AI Dungeon", page_icon="🗡️", layout="centered")

# Dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .title { text-align: center; color: #f0f6fc; font-size: 2.5rem; margin-bottom: 0.5rem; }
    .subtitle { text-align: center; color: #8b949e; font-size: 1.1rem; margin-bottom: 2rem; }
    .story-box { background-color: #161b22; border-radius: 16px; padding: 20px; border: 1px solid #30363d; margin: 15px 0; max-height: 400px; overflow-y: auto; }
    .narrative { color: #c9d1d9; line-height: 1.8; font-size: 1rem; }
    .choice-btn { background-color: #238636; color: white; padding: 12px 20px; border-radius: 8px; border: none; margin: 5px; cursor: pointer; width: 100%; }
    .choice-btn:hover { background-color: #2ea043; }
    .input-area { background-color: #1c2128; border-radius: 12px; padding: 15px; border: 2px solid #30363d; }
    .health-bar { background-color: #3fb950; height: 20px; border-radius: 10px; transition: width 0.3s; }
    .stat-box { background-color: #1c2128; padding: 10px; border-radius: 8px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "story" not in st.session_state:
    st.session_state.story = []
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "player_stats" not in st.session_state:
    st.session_state.player_stats = {"health": 100, "gold": 50, "level": 1}

st.markdown('<h1 class="title">🗡️ AI Dungeon</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your choices shape the story</p>', unsafe_allow_html=True)

# Sidebar - Game Settings
with st.sidebar:
    st.header("⚔️ Adventure Settings")

    genre = st.selectbox("🎭 Genre", [
        "Fantasy Quest", "Space Opera", "Mystery", "Horror",
        "Comedy Adventure", "Romance", "Post-Apocalyptic"
    ])

    difficulty = st.selectbox("💀 Difficulty", ["Easy", "Normal", "Hard", "Permadeath"])

    st.markdown("---")
    st.subheader("📊 Your Stats")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("❤️ Health", st.session_state.player_stats["health"])
    with col2:
        st.metric("💰 Gold", st.session_state.player_stats["gold"])

    st.metric("⭐ Level", st.session_state.player_stats["level"])

    if st.button("🔄 New Game"):
        st.session_state.story = []
        st.session_state.game_started = False
        st.session_state.player_stats = {"health": 100, "gold": 50, "level": 1}
        st.rerun()

    st.markdown("---")
    st.caption("Powered by Google Gemini")

# Character creation
if not st.session_state.game_started:
    st.subheader("🧙 Create Your Hero")

    col1, col2 = st.columns(2)
    with col1:
        character_name = st.text_input("🏷️ Character Name", placeholder="Enter your name...")
        character_class = st.selectbox("⚔️ Class", [
            "Warrior", "Mage", "Rogue", "Ranger", "Paladin", "Bard"
        ])

    with col2:
        backstory = st.text_area("📜 Backstory Hint", placeholder="A hint about your past...", height=80)

    class_descriptions = {
        "Warrior": "💪 Strong and fearless, master of combat",
        "Mage": "🔮 Wielder of arcane powers and ancient knowledge",
        "Rogue": "🗡️ Swift and cunning, a master of stealth",
        "Ranger": "🏹 Nature's guardian with deadly aim",
        "Paladin": "🛡️ Holy champion of justice and light",
        "Bard": "🎵 Charismatic storyteller with magical music"
    }

    st.info(f"**{character_class}**: {class_descriptions.get(character_class, '')}")

    if st.button("⚔️ Begin Adventure", use_container_width=True, type="primary"):
        if not character_name:
            st.warning("Please name your hero!")
        else:
            with st.spinner("📖 Writing your epic..."):
                try:
                    api_key = os.environ.get("GEMINI_API_KEY", "")
                    if api_key:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("gemini-1.5-flash")

                        prompt = f"""Begin an interactive text adventure story for a player.

Character: {character_name}
Class: {character_class}
Genre: {genre}
Difficulty: {difficulty}
Backstory hint: {backstory if backstory else 'A mysterious past'}

Write an engaging opening scene (2-3 paragraphs) that:
1. Sets the scene and atmosphere
2. Introduces the character's situation
3. Presents 3 clear choices for the player

Format:
---
NARRATIVE:
[Your story opening here...]

CHOICES:
1. [First choice with brief description]
2. [Second choice with brief description]
3. [Third choice with brief description]
---
"""
                        response = model.generate_content(prompt)
                        opening = response.text
                    else:
                        opening = """⚠️ **Demo Mode** - Set `GEMINI_API_KEY` for real AI generation.

---
NARRATIVE:
The morning mist rolls across the ancient forest as you awaken. You are **{name}**, a {char_class} whose journey has only begun. The path ahead splits into three directions, each shrouded in mystery and possibility.

The {genre} world awaits your decisions. Every choice will shape your destiny.

CHOICES:
1. **Venture into the dark forest** - Ancient secrets lie within...
2. **Follow the merchant's road** - Safety and civilization await...
3. **Investigate the mysterious ruins** - Treasure and danger go hand in hand...
---
""".format(name=character_name, char_class=character_class, genre=genre)

                    st.session_state.story = [{"role": "narrator", "content": opening}]
                    st.session_state.game_started = True
                    st.rerun()

                except Exception as e:
                    st.error(f"Error starting game: {str(e)}")

else:
    # Display story
    st.subheader("📖 Story")

    for entry in st.session_state.story:
        if entry["role"] == "narrator":
            st.markdown(f'<div class="story-box"><div class="narrative">{entry["content"]}</div></div>', unsafe_allow_html=True)

    # Input for next action
    st.markdown("---")
    st.subheader("🎯 Your Action")

    custom_action = st.text_input(
        "What do you do?",
        placeholder="Describe your action or choose from suggestions...",
        key="action_input"
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        submit_action = st.button("✨ Perform Action", use_container_width=True, type="primary")
    with col2:
        if st.button("🔄 Continue Story", use_container_width=True):
            custom_action = "Continue the story naturally"
            submit_action = True

    if submit_action and custom_action:
        with st.spinner("⚔️ Resolving action..."):
            try:
                api_key = os.environ.get("GEMINI_API_KEY", "")
                story_context = "\n\n".join([f"[{i+1}] {s['content']}" for i, s in enumerate(st.session_state.story[-3:])])

                if api_key:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")

                    prompt = f"""Continue this interactive text adventure story.

Character: {st.session_state.get('character_name', 'Hero')}
Class: {st.session_state.get('character_class', 'Adventurer')}
Genre: {genre}
Difficulty: {difficulty}

Recent story context:
{story_context}

Player's action: {custom_action}

Continue the narrative (2-3 paragraphs) based on the player's action, then offer 3 new choices.

Consider: Does this action succeed? What are the consequences? How does the world react?

Format:
---
NARRATIVE:
[Continue the story...]

CHOICES:
1. [Choice 1]
2. [Choice 2]
3. [Choice 3]
---

After the --- section, on a single line, provide:
STATS: health=X gold=X level=X (only if they changed)
"""
                    response = model.generate_content(prompt)
                    continuation = response.text
                else:
                    continuation = f"""
NARRATIVE:
You {custom_action.lower()}. The world responds to your action...

The path ahead reveals new possibilities. Your courage is being tested.

CHOICES:
1. **Press forward** - The adventure continues...
2. **Rest and regroup** - Recover your strength...
3. **Search the area** - Look for clues and treasure...
---

STATS: health=100 gold=50 level=1
"""

                # Parse stats if present
                if "STATS:" in continuation:
                    parts = continuation.split("STATS:")
                    narrative_part = parts[0]
                    stats_part = parts[1].split("---")[0].strip()
                    continuation = narrative_part

                    for stat in stats_part.split():
                        if "health=" in stat:
                            st.session_state.player_stats["health"] = int(stat.split("=")[1])
                        elif "gold=" in stat:
                            st.session_state.player_stats["gold"] = int(stat.split("=")[1])
                        elif "level=" in stat:
                            st.session_state.player_stats["level"] = int(stat.split("=")[1])

                st.session_state.story.append({"role": "player", "content": f"**You:** {custom_action}"})
                st.session_state.story.append({"role": "narrator", "content": continuation})
                st.rerun()

            except Exception as e:
                st.error(f"Error continuing story: {str(e)}")

    # Game over check
    if st.session_state.player_stats["health"] <= 0:
        st.error("💀 GAME OVER - Your adventure has ended!")
        if st.button("🔄 Start New Adventure"):
            st.session_state.story = []
            st.session_state.game_started = False
            st.rerun()
