# AI Chatbot

A simple conversational AI chatbot powered by Google Gemini.

## Features

- Natural language conversations
- Chat history persistence (within session)
- Clean dark theme UI
- Configurable API key via sidebar

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Gemini API Key:**
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Create an API key
   - Set it as environment variable:
     ```bash
     export GEMINI_API_KEY="your-api-key"
     ```
   - Or enter it in the app's sidebar

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Enter your message in the chat input
2. Press Enter or click Send
3. View AI responses in the chat
4. Use sidebar to clear chat or change API key

## Project Structure

```
01-ai-chatbot/
├── app.py           # Main Streamlit application
├── requirements.txt # Python dependencies
└── README.md        # This file
```
