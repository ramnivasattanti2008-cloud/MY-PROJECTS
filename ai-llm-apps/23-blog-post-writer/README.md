# Blog Post Writer ✍️

An AI-powered tool that generates professional blog post outlines with structure, content ideas, and SEO optimization using Google's Gemini API.

## Features

- Generate comprehensive blog outlines
- Multiple writing styles (How-to, Listicle, Opinion, etc.)
- Customizable tone and length
- SEO keyword integration
- Meta description generation
- Featured image suggestions

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

1. Enter your blog topic
2. Optionally specify target audience and SEO keywords
3. Choose blog style and tone
4. Click "Generate Outline" for a complete blog structure

## Output Includes

- SEO-optimized title
- Meta description (155 chars)
- Structured outline with H2/H3 headings
- Introduction hook
- Content sub-points
- Conclusion with CTA
- Featured image suggestion

## Environment Variables

- `GEMINI_API_KEY` - Your Gemini API key (optional, can also enter in UI)
