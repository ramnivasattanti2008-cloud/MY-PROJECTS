# Git Commit Writer 📝

An AI-powered tool that generates professional, descriptive git commit messages from your diff output using Google's Gemini API.

## Features

- Generate conventional commit messages
- Multiple commit types (feat, fix, docs, style, refactor, test, chore)
- Optional scope and ticket number integration
- Detailed commit body generation
- One-click copy functionality
- Clean, developer-friendly interface

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/)

3. Run the app:
   ```bash
   streamlit run app.py
   ```

4. Enter your API key in the sidebar

## Usage

1. Make your changes in your codebase
2. Stage your changes: `git add <files>` or `git add .`
3. Get the diff: `git diff --staged` (for staged) or `git diff` (for unstaged)
4. Paste the diff output
5. Optionally add scope and ticket number
6. Click "Generate Commit Message"
7. Copy and use!

## Commit Types

- **feat** - New feature
- **fix** - Bug fix
- **docs** - Documentation changes
- **style** - Code style changes (formatting, semicolons, etc.)
- **refactor** - Code refactoring
- **test** - Adding or updating tests
- **chore** - Maintenance tasks

## Example Output

```
feat(auth): add password reset functionality

- Add reset password endpoint
- Implement email verification
- Add rate limiting for security
- Include expiration token handling

Closes #123
```

## Environment Variables

- `GEMINI_API_KEY` - Your Gemini API key (optional, can also enter in UI)
