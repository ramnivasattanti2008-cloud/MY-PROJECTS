# Study Buddy

Your AI-powered study assistant for learning any topic.

## Features

- **Topic Explanations** - Learn concepts in simple terms
- **Quiz Generation** - Test your knowledge with AI-generated questions
- **Flashcard Creation** - Quick review cards for memorization
- **Multiple Topics** - Any subject from science to history to programming

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Gemini API Key:**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create an API key
   - Set as environment variable:
     ```bash
     export GEMINI_API_KEY="your-api-key"
     ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Study Modes

### 📖 Explain Topic
Get a clear, beginner-friendly explanation of any concept with:
- Simple definitions
- Key concepts
- Real-world examples
- Common misconceptions

### ❓ Take Quiz
Test your knowledge with:
- Multiple choice questions
- Mix of factual and conceptual questions
- Configurable number of questions

### 🃏 Flashcards
Create quick review cards:
- Term/definition pairs
- Perfect for memorization
- Configurable number of cards

## Usage Tips

1. Be specific with your topic (e.g., "Photosynthesis" not "Biology")
2. Adjust difficulty by how you phrase questions
3. Use quizzes to identify knowledge gaps
4. Create flashcards for any topic you want to memorize

## Project Structure

```
04-study-buddy/
├── app.py           # Main Streamlit application
├── requirements.txt # Python dependencies
└── README.md        # This file
```
