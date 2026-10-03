# Product Review Summarizer ⭐

An AI-powered tool that analyzes multiple product reviews to extract common themes, sentiment, and actionable insights using Google's Gemini API.

## Features

- Analyze sentiment across multiple reviews
- Extract key themes (positive and negative)
- Generate pros and cons lists
- Identify target customer segments
- Include representative quote examples
- Quick and detailed analysis modes

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

1. Paste product reviews (one per line or separated by blank lines)
2. Optionally enter the product name
3. Choose analysis depth (quick or detailed)
4. Click "Analyze Reviews" for instant insights

## Input Format

Each review should be on a separate line:
```
Great product! Works perfectly.
The quality is poor and it broke.
Love it! Would recommend.
```

## Output Includes

- Overall sentiment score
- Key praise points
- Common complaints
- Top pros and cons
- Target customer profile
- Notable review quotes

## Environment Variables

- `GEMINI_API_KEY` - Your Gemini API key (optional, can also enter in UI)
