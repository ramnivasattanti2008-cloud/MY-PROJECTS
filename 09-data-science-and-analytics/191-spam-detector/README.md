# Spam Detector

A beginner-friendly machine learning project that detects spam messages using Naive Bayes classification.

## Overview

This project demonstrates how to build a spam detector using the **Naive Bayes algorithm**, a popular choice for text classification tasks.

## ML Concepts Covered

- **Bag of Words (BoW)**: Converting text to numerical features
- **Naive Bayes Classifier**: A probabilistic classifier based on Bayes' theorem
- **Text Preprocessing**: Tokenization and feature extraction
- **Model Evaluation**: Accuracy, precision, recall, F1-score

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the Model

```bash
python train.py
```

This will:
- Download the SMS Spam Collection dataset
- Train a Naive Bayes classifier
- Save the model as `model.pkl` and `vectorizer.pkl`

### 3. Run the Web App

```bash
streamlit run app.py
```

## Project Structure

```
spam-detector/
├── app.py           # Streamlit web application
├── train.py         # Model training script
├── model.pkl        # Trained classifier (generated)
├── vectorizer.pkl   # Fitted CountVectorizer (generated)
├── spam_data.csv    # Dataset (downloaded)
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## How It Works

### Bag of Words

The text is converted into numerical features using CountVectorizer:

1. **Tokenization**: Split text into individual words
2. **Counting**: Count occurrences of each word
3. **Vectorization**: Convert to a sparse matrix

### Naive Bayes Classification

The Multinomial Naive Bayes algorithm calculates:

$$P(spam|words) = \frac{P(words|spam) \cdot P(spam)}{P(words)}$$

For each word in the message, it computes the probability of being spam or ham, then picks the higher probability.

## Example Usage

- Input: "Congratulations! You've won a free prize!"
- Output: **Spam** (98.5% confidence)

- Input: "Hey, are we meeting for lunch today?"
- Output: **Ham** (99.2% confidence)

## Screenshots

The Streamlit app provides:
- Text input area for messages
- One-click spam detection
- Confidence scores
- Visual probability breakdown

## Further Improvements

- Add more features (word n-grams, character patterns)
- Try other classifiers (SVM, Random Forest)
- Add spam keywords highlighting
- Implement real-time email integration
