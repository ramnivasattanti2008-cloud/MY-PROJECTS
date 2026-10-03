"""
Spam Detector Training Script
Trains a Naive Bayes classifier to detect spam messages.
Uses the SMS Spam Collection dataset from UCI ML Repository.
"""

import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def load_data():
    """
    Load the SMS Spam Collection dataset.
    This is a well-known dataset containing 5,574 SMS messages,
    each labeled as 'ham' (not spam) or 'spam'.
    """
    # Download dataset if not exists
    data_path = Path(__file__).parent / "spam_data.csv"

    if not data_path.exists():
        print("Downloading SMS Spam Collection dataset...")
        # Using a copy of the dataset from a reliable source
        url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"

        try:
            df = pd.read_csv(url, sep='\t', header=None, names=['label', 'message'])
            df.to_csv(data_path, index=False)
            print(f"Dataset saved to {data_path}")
        except Exception as e:
            print(f"Could not download: {e}")
            # Fallback: Create a small sample dataset
            print("Creating sample dataset for demonstration...")
            df = create_sample_data()
            df.to_csv(data_path, index=False)

    return pd.read_csv(data_path)


def create_sample_data():
    """
    Creates a small sample dataset for demonstration purposes.
    In production, you would use the real UCI dataset.
    """
    messages = [
        ("ham", "Hey, are we still meeting for lunch today?"),
        ("ham", "Thanks for calling. I'll call you back later."),
        ("spam", "Congratulations! You've won a free iPhone! Click here to claim."),
        ("ham", "Can you send me the report when you get a chance?"),
        ("spam", "URGENT: Your account has been compromised. Verify now!"),
        ("ham", "I'll be home by 6pm."),
        ("spam", "FREE MONEY! Click here to win $1,000,000!"),
        ("ham", "The meeting is scheduled for 2pm tomorrow."),
        ("spam", "You have been selected for a prize! Call now!"),
        ("ham", "Thanks for your help with the project."),
        ("spam", "CONGRATULATIONS! You are the 1000th visitor!"),
        ("ham", "Let me know if you need anything else."),
        ("spam", "Your loan is approved! Call now to finalize."),
        ("ham", "I'll see you at the party tonight."),
        ("spam", "WARNING: Your computer may be infected!"),
        ("ham", "The report looks good. Good job!"),
        ("spam", "Make money fast! Visit our website!"),
        ("ham", "Can we reschedule our call to Friday?"),
        ("spam", "Act now! Limited time offer!"),
        ("ham", "I've sent you the files you requested."),
        ("spam", "Click here for free stuff!"),
        ("ham", "Happy birthday! Hope you have a great day!"),
        ("spam", "You've won! Claim your prize immediately!"),
        ("ham", "The weather looks nice today."),
        ("spam", "Your message is waiting. Call now!"),
        ("ham", "I'll be there in 10 minutes."),
        ("spam", "Congratulations! Your number was selected!"),
        ("ham", "Can you pick up some milk on your way home?"),
        ("spam", "Low interest loan available. Apply today!"),
        ("ham", "See you tomorrow morning."),
        ("spam", "FREE gift card! Complete survey now!"),
        ("ham", "I'll send you the document shortly."),
        ("spam", "Your account will be suspended. Verify now!"),
        ("ham", "Thanks for letting me know."),
        ("spam", "Congratulations! You've been pre-approved!"),
        ("ham", "The train arrives at 5:30pm."),
        ("spam", "Get rich quick! No experience needed!"),
        ("ham", "I'll call you after the meeting."),
        ("spam", "URGENT! Claim your prize before it expires!"),
        ("ham", "Please review the attached document."),
        ("spam", "You have a new message. Click here."),
        ("ham", "I'm running a bit late."),
        ("spam", "Double your money in 24 hours!"),
        ("ham", "Let's schedule a meeting for next week."),
        ("spam", "Exclusive offer just for you!"),
        ("ham", "I'll be there right after lunch."),
        ("spam", "Your gift is waiting! Redeem now!"),
        ("ham", "Can you send me the updated spreadsheet?"),
        ("spam", "Act now! This offer won't last!"),
        ("ham", "Thank you for your email."),
        ("spam", "Congratulations! You are a winner!"),
    ]

    return pd.DataFrame(messages, columns=['label', 'message'])


def train_model():
    """
    Main training pipeline:
    1. Load and preprocess data
    2. Split into train/test sets
    3. Create features using Bag of Words (CountVectorizer)
    4. Train a Naive Bayes classifier
    5. Evaluate and save the model
    """
    print("=" * 50)
    print("SPAM DETECTOR - Training Pipeline")
    print("=" * 50)

    # Load data
    print("\n[1/5] Loading data...")
    df = load_data()
    print(f"   Loaded {len(df)} messages")
    print(f"   Spam: {sum(df['label'] == 'spam')}, Ham: {sum(df['label'] == 'ham')}")

    # Prepare features and labels
    print("\n[2/5] Preparing features...")
    X = df['message']
    y = df['label'].map({'ham': 0, 'spam': 1})  # Convert to binary

    # Split data (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")

    # Create Bag of Words features
    # This converts text to numerical features based on word counts
    print("\n[3/5] Creating features (Bag of Words)...")
    vectorizer = CountVectorizer(
        stop_words='english',  # Remove common words like 'the', 'is'
        max_features=1000      # Keep top 1000 words
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    print(f"   Vocabulary size: {len(vectorizer.vocabulary_)}")

    # Train Naive Bayes classifier
    # MultinomialNB works well for text classification
    print("\n[4/5] Training Naive Bayes classifier...")
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)
    print("   Training complete!")

    # Evaluate
    print("\n[5/5] Evaluating model...")
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n   Accuracy: {accuracy:.2%}")
    print("\n   Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Ham', 'Spam']))

    print("\n   Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"   TN: {cm[0][0]:4d} | FP: {cm[0][1]:4d}")
    print(f"   FN: {cm[1][0]:4d} | TP: {cm[1][1]:4d}")

    # Save model and vectorizer
    print("\n[Saving model...]")
    models_dir = Path(__file__).parent
    with open(models_dir / "vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open(models_dir / "model.pkl", "wb") as f:
        pickle.dump(model, f)

    print(f"   Saved vectorizer.pkl and model.pkl")
    print("\n" + "=" * 50)
    print("Training complete! Run app.py to use the model.")
    print("=" * 50)

    return model, vectorizer


if __name__ == "__main__":
    train_model()
