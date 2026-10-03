# Sentiment Analyzer

A beginner-friendly machine learning project that analyzes the sentiment (positive, negative, or neutral) of any text using TextBlob.

## Overview

This project demonstrates simple sentiment analysis using **TextBlob**, a Python library built on top of NLTK. It provides polarity and subjectivity scores for any given text.

## ML Concepts Covered

- **Sentiment Analysis**: Determining emotional tone in text
- **Polarity Score**: Measuring positive vs. negative sentiment
- **Subjectivity Score**: Measuring opinion vs. fact
- **Natural Language Processing (NLP)**: Tokenization and word-level analysis

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download NLTK Data (required by TextBlob)

```bash
python -m textblob.download_corpora
```

### 3. Run the Web App

```bash
streamlit run app.py
```

## Project Structure

```
sentiment-simple/
├── app.py              # Streamlit web application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## How It Works

### TextBlob Sentiment Analysis

TextBlob uses a pre-trained sentiment analyzer that returns:

- **Polarity**: -1 (very negative) to +1 (very positive)
- **Subjectivity**: 0 (very objective) to 1 (very subjective)

### Example Scores

| Text | Polarity | Subjectivity |
|------|----------|--------------|
| "I love this product!" | +0.75 | 0.80 |
| "This is terrible." | -0.80 | 0.90 |
| "The meeting is at 3pm." | 0.00 | 0.00 |
| "I think it's okay, maybe." | +0.10 | 0.50 |

## Features

- **Real-time analysis**: See results as you type
- **Visual sentiment meter**: See where your text falls on the scale
- **Word-level analysis**: See which words contribute most to sentiment
- **Subjectivity indicator**: Understand if text is fact or opinion
- **Example texts**: Try pre-written examples

## How TextBlob Works

1. **Tokenization**: Split text into words and sentences
2. **Word sentiment lookup**: Each word has a pre-assigned polarity
3. **Aggregation**: Average all word sentiments for overall score
4. **Classification**: Label as positive, negative, or neutral

## Example Usage

Input: "This movie was absolutely fantastic! I loved every minute of it."

Output:
- **Sentiment**: Positive 😊
- **Polarity**: +0.72
- **Subjectivity**: 0.85 (highly subjective)

## Further Improvements

- Use custom-trained models for domain-specific sentiment
- Add aspect-based sentiment (analyze different parts separately)
- Implement multi-language support
- Create sentiment trends over time
- Add emotion detection (joy, anger, sadness, etc.)
