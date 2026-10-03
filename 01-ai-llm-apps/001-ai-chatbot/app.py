"""
AI Chatbot - Simple conversational AI with chat history
Uses Google Gemini API for natural language responses
"""

import streamlit as st
import os
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .chat-message {padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;}
    .user-msg {background-color: #262730; color: #ffffff;}
    .bot-msg {background-color: #1a2332; color: #e0e0e0;}
    .stTextInput > div > div > input {background-color: #262730; color: white;}
</style>
""", unsafe_allow_html=True)

def get_api_key():
    """Get Gemini API key from secrets or environment"""
    try:
        return st.secrets["GEMINI_API_KEY"]
    except:
        return os.environ.get("GEMINI_API_KEY", "")

def init_gemini(api_key):
    """Initialize Gemini with API key"""
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def get_response(model, user_input, history):
    """Get response from Gemini"""
    try:
        # Build conversation context
        chat = model.start_chat(history=history)
        response = chat.send_message(user_input)
        return response.text, chat.history
    except Exception as e:
        return f"Error: {str(e)}", history

def main():
    st.title("💬 AI Chatbot")
    st.caption("Powered by Google Gemini")

    # Sidebar for API key
    with st.sidebar:
        st.header("⚙️ Settings")
        api_key = get_api_key()

        if not api_key:
            st.warning("Please enter your Gemini API key")
            api_key = st.text_input("Gemini API Key", type="password", help="Get your API key from Google AI Studio")
            if api_key:
                st.session_state.api_key = api_key
                st.rerun()
        else:
            st.success("API Key loaded")

        st.markdown("---")
        st.markdown("### How to use")
        st.markdown("1. Enter your message")
        st.markdown("2. Press Enter or click Send")
        st.markdown("3. Chat history persists in session")

        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.history = []
            st.rerun()

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "history" not in st.session_state:
        st.session_state.history = []
    if "api_key" not in st.session_state and api_key:
        st.session_state.api_key = api_key

    # Check API key
    if not st.session_state.get("api_key"):
        st.error("Please enter your Gemini API key in the sidebar to continue.")
        return

    # Initialize Gemini
    if not init_gemini(st.session_state.api_key):
        st.error("Failed to initialize Gemini. Please check your API key.")
        return

    model = genai.GenerativeModel('gemini-1.5-flash')

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if user_input := st.chat_input("Type your message here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response, history = get_response(
                    model,
                    user_input,
                    st.session_state.history
                )
                st.markdown(response)
                st.session_state.history = history

        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
