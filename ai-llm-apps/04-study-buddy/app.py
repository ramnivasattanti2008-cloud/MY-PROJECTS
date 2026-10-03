"""
Study Buddy - AI Study Assistant
Learn topics, generate quizzes, create flashcards
"""

import streamlit as st
import os
import google.generativeai as genai

st.set_page_config(
    page_title="Study Buddy",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .mode-card {background-color: #1a2332; padding: 1.5rem; border-radius: 0.5rem; text-align: center;}
    .flashcard {background-color: #1a2332; padding: 2rem; border-radius: 1rem; text-align: center; min-height: 200px;}
    .quiz-option {padding: 1rem; border: 1px solid #3a3a4a; border-radius: 0.5rem; margin: 0.5rem 0;}
</style>
""", unsafe_allow_html=True)

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

def explain_topic(model, topic):
    """Explain a topic in simple terms"""
    prompt = f"""Explain this topic in a clear, beginner-friendly way:

Topic: {topic}

Include:
- Simple definition
- Key concepts (3-5 bullet points)
- Real-world example
- Common misconceptions
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def generate_quiz(model, topic, num_questions=5):
    """Generate a quiz on a topic"""
    prompt = f"""Create a {num_questions}-question quiz about: {topic}

Format each question as:
Q1: [Question]
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]
Answer: [Correct letter]

Make questions mix of factual and conceptual.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def generate_flashcards(model, topic, num_cards=5):
    """Generate flashcards"""
    prompt = f"""Create {num_cards} flashcards about: {topic}

Format as:
TERM: [Term]
DEFINITION: [Definition]

---
TERM: [Next Term]
DEFINITION: [Definition]

(Continue for all cards)
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("📚 Study Buddy")
    st.caption("Your AI-Powered Learning Assistant")

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
        st.markdown("### Study Modes")
        st.markdown("📖 **Explain** - Learn concepts")
        st.markdown("❓ **Quiz** - Test knowledge")
        st.markdown("🃏 **Flashcards** - Quick review")

    if "api_key" not in st.session_state and api_key:
        st.session_state.api_key = api_key

    if not st.session_state.get("api_key"):
        st.error("Please enter your Gemini API key in the sidebar.")
        return

    if not init_gemini(st.session_state.api_key):
        st.error("Failed to initialize Gemini.")
        return

    model = genai.GenerativeModel('gemini-1.5-flash')

    # Mode selection
    mode = st.radio(
        "🎯 Choose Study Mode",
        ["📖 Explain Topic", "❓ Take Quiz", "🃏 Flashcards"],
        horizontal=True
    )

    # Topic input
    st.subheader("📝 What do you want to study?")
    topic = st.text_input(
        "Enter a topic",
        placeholder="Example: Photosynthesis, Python basics, World War II...",
        label_visibility="collapsed"
    )

    # Mode-specific options
    if mode == "❓ Take Quiz":
        num_questions = st.slider("Number of questions", 3, 10, 5)

    if mode == "🃏 Flashcards":
        num_cards = st.slider("Number of cards", 3, 10, 5)

    # Generate button
    if st.button(f"✨ {mode.split()[0]} Go!", type="primary") and topic:
        with st.spinner("Preparing your study material..."):
            if mode == "📖 Explain Topic":
                result = explain_topic(model, topic)
                st.session_state.explanation = result
                st.session_state.quiz = None
                st.session_state.flashcards = None
            elif mode == "❓ Take Quiz":
                result = generate_quiz(model, topic, num_questions)
                st.session_state.quiz = result
                st.session_state.explanation = None
                st.session_state.flashcards = None
            else:
                result = generate_flashcards(model, topic, num_cards)
                st.session_state.flashcards = result
                st.session_state.explanation = None
                st.session_state.quiz = None

    # Display results
    if st.session_state.get("explanation"):
        st.markdown("---")
        st.subheader("📖 Topic Explanation")
        st.markdown(st.session_state.explanation)

    if st.session_state.get("quiz"):
        st.markdown("---")
        st.subheader("❓ Quiz Time!")
        st.markdown(st.session_state.quiz)

    if st.session_state.get("flashcards"):
        st.markdown("---")
        st.subheader("🃏 Flashcards")

        cards_text = st.session_state.flashcards
        cards = cards_text.split("---")

        for i, card in enumerate(cards):
            if card.strip():
                with st.container():
                    st.markdown(f"**Card {i+1}**")
                    st.markdown(card.strip())
                    st.markdown("---")

if __name__ == "__main__":
    main()
