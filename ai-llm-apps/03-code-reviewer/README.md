# Code Reviewer

AI-powered code review tool that analyzes your code and provides feedback.

## Features

- Multi-language support (Python, JavaScript, Java, C++, and more)
- Structured review with severity levels
- Security and performance checks
- Best practices recommendations
- Clean code display with syntax highlighting

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Gemini API Key:**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Get your free API key
   - Set as environment variable:
     ```bash
     export GEMINI_API_KEY="your-api-key"
     ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Usage

1. Select the programming language
2. Paste your code in the text area
3. Click "Review Code"
4. View detailed feedback organized by severity:
   - 🔴 HIGH - Critical issues to fix
   - 🟡 MEDIUM - Important improvements
   - 🟢 LOW - Nice-to-have optimizations

## Review Categories

- **Code Quality** - Structure, organization, maintainability
- **Security** - Vulnerabilities, injection risks, authentication
- **Performance** - Efficiency, memory usage, algorithmic complexity
- **Best Practices** - Language idioms, patterns, conventions
- **Readability** - Naming, comments, formatting

## Project Structure

```
03-code-reviewer/
├── app.py           # Main Streamlit application
├── requirements.txt # Python dependencies
└── README.md        # This file
```
