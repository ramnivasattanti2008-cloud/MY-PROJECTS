# Meeting Summarizer

AI-powered tool to summarize meeting notes, extract action items, and generate formal minutes.

## Features

- **Full Summary** - Complete analysis with key points, decisions, and action items
- **Decisions Only** - Focus on decisions made during the meeting
- **Meeting Minutes** - Generate formal meeting minutes document
- **Action Item Extraction** - Identify tasks with assignees

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

## Usage

1. Select your preferred output format
2. Paste meeting notes (can be rough or formatted)
3. Click "Summarize"
4. Copy the results to share with your team

## Input Formats

Works with various meeting note formats:
- Rough bullet points
- Full transcripts
- Structured notes with sections
- Chat exports

## Output Types

### Full Summary
- Executive summary
- Key points discussed
- Decisions made
- Action items with assignees
- Next steps

### Decisions Only
- List of all decisions
- Clear formatting

### Meeting Minutes
- Formal document format
- Include attendees, date, agenda
- Structured sections

## Project Structure

```
05-meeting-summarizer/
├── app.py           # Main Streamlit application
├── requirements.txt # Python dependencies
└── README.md        # This file
```
