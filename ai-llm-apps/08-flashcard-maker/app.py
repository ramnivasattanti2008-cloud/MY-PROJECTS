"""
Flashcard Maker - Create Q&A flashcards from topics/notes
Uses Gemini AI to generate study cards
"""

import streamlit as st
import os
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Flashcard Maker",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; color: #F59E0B; }
    .sub-header { font-size: 1.2rem; color: #FBBF24; }
    .flashcard { background-color: #1E1E2E; padding: 20px; border-radius: 12px; margin: 10px 0; }
    .question { color: #F59E0B; font-weight: bold; font-size: 1.1rem; }
    .answer { color: #10B981; font-size: 1rem; margin-top: 10px; }
    .stTextArea > div > div > textarea { background-color: #1E1E2E; }
</style>
""", unsafe_allow_html=True)

def get_gemini_api_key(api_key_input: str = None) -> str:
    """Get Gemini API key from various sources"""
    if hasattr(st, 'secrets') and 'GEMINI_API_KEY' in st.secrets:
        return st.secrets['GEMINI_API_KEY']
    if os.environ.get('GEMINI_API_KEY'):
        return os.environ.get('GEMINI_API_KEY')
    if api_key_input:
        return api_key_input
    return None

def setup_gemini(api_key: str):
    """Configure Gemini with API key"""
    if api_key:
        genai.configure(api_key=api_key)

def generate_flashcards(topic: str, num_cards: int, model) -> list:
    """Generate flashcards from topic using Gemini"""
    prompt = f"""Create {num_cards} flashcards for studying: {topic}

Format each flashcard as:
Q: [Question]
A: [Answer]

Make questions clear and specific. Answers should be concise but complete.
Cover key concepts, definitions, examples, and important facts.
Return ONLY the flashcards in the exact format shown above, numbered 1-{num_cards}."""

    try:
        response = model.generate_content(prompt)
        return parse_flashcards(response.text)
    except Exception as e:
        return [{"question": "Error", "answer": str(e)}]

def parse_flashcards(text: str) -> list:
    """Parse flashcards from Gemini response"""
    flashcards = []
    lines = text.strip().split('\n')
    current_q = None
    current_a = None

    for line in lines:
        line = line.strip()
        if line.startswith('Q:') or line.startswith('Q1'):
            if current_q and current_a:
                flashcards.append({"question": current_q, "answer": current_a})
            current_q = line[2:].strip() if line.startswith('Q:') else line[3:].strip()
            current_a = None
        elif line.startswith('A:'):
            current_a = line[2:].strip()

    if current_q and current_a:
        flashcards.append({"question": current_q, "answer": current_a})

    return flashcards

def create_txt_content(flashcards: list) -> str:
    """Create downloadable text content"""
    content = "=" * 50 + "\n"
    content += "FLASHCARDS\n"
    content += "=" * 50 + "\n\n"

    for i, card in enumerate(flashcards, 1):
        content += f"Card {i}:\n"
        content += f"Q: {card['question']}\n"
        content += f"A: {card['answer']}\n"
        content += "-" * 30 + "\n\n"

    return content

def main():
    # Header
    st.markdown('<p class="main-header">📚 Flashcard Maker</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Generate study flashcards from any topic</p>', unsafe_allow_html=True)
    st.divider()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        api_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get your API key from Google AI Studio"
        )

        st.markdown("---")
        st.markdown("""
        **How to get an API key:**
        1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Create a new API key
        3. Paste it here
        """)

        st.markdown("---")
        st.markdown("**Tips:**")
        st.markdown("""
        - Be specific with topics
        - Include key terms
        - Add context for better cards
        """)

    # Main content
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📝 Enter Topic or Notes")

        topic = st.text_area(
            "Topic / Notes",
            placeholder="Example: Python list comprehensions\n\nInclude any notes, concepts, or topics you want flashcards on...",
            height=200
        )

        num_cards = st.slider("Number of flashcards", 3, 15, 5)

        generate_btn = st.button("🎴 Generate Flashcards", type="primary", use_container_width=True)

    # Flashcard display
    if generate_btn and topic:
        api_key = get_gemini_api_key(api_key_input)

        if not api_key:
            st.error("⚠️ Please enter your Gemini API key in the sidebar!")
        else:
            with st.spinner("Generating flashcards..."):
                try:
                    setup_gemini(api_key)
                    model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    flashcards = generate_flashcards(topic, num_cards, model)

                    if flashcards:
                        st.success(f"✅ Created {len(flashcards)} flashcards!")

                        # Display flashcards
                        for i, card in enumerate(flashcards, 1):
                            with st.container():
                                st.markdown(f"### 📇 Card {i}")
                                st.markdown(f'<div class="flashcard">', unsafe_allow_html=True)
                                st.markdown(f'<p class="question">❓ {card["question"]}</p>', unsafe_allow_html=True)
                                st.markdown(f'<p class="answer">💡 {card["answer"]}</p>', unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)

                        # Download button
                        txt_content = create_txt_content(flashcards)
                        st.download_button(
                            label="📥 Download as Text",
                            data=txt_content,
                            file_name="flashcards.txt",
                            mime="text/plain",
                            type="primary"
                        )
                    else:
                        st.warning("No flashcards generated. Try a different topic.")

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Template section
    st.divider()
    st.subheader("💡 Suggested Topics")

    suggestions = [
        ("Python", "Python list comprehensions and map/filter functions"),
        ("History", "World War II causes and key events"),
        ("Biology", "Cell structure and organelles"),
        ("Math", "Quadratic equations and factoring"),
    ]

    cols = st.columns(4)
    for i, (cat, suggestion) in enumerate(suggestions):
        with cols[i]:
            st.info(f"**{cat}**\n\n{suggestion}")

if __name__ == "__main__":
    main()
