"""
Digit Recognizer Training Script
Trains a classifier to recognize handwritten digits (0-9).
Uses the MNIST-style digit dataset from scikit-learn.
"""

import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def load_data():
    """
    Load the digit dataset.
    This is a simplified version of MNIST with 1,797 samples
    of 8x8 pixel digit images.
    """
    digits = datasets.load_digits()
    return digits


def train_model():
    """
    Main training pipeline:
    1. Load digit dataset
    2. Visualize sample images
    3. Split into train/test sets
    4. Scale features (pixel values)
    5. Train SVM classifier
    6. Evaluate and save the model
    """
    print("=" * 50)
    print("DIGIT RECOGNIZER - Training Pipeline")
    print("=" * 50)

    # Load data
    print("\n[1/5] Loading digit dataset...")
    digits = load_data()
    X = digits.data
    y = digits.target
    images = digits.images

    print(f"   Images: {len(X)}")
    print(f"   Image size: {int(np.sqrt(X.shape[1]))}x{int(np.sqrt(X.shape[1]))} pixels")
    print(f"   Classes: {list(range(10))}")

    # Visualize samples
    print("\n[2/5] Creating sample visualization...")
    visualize_samples(images, y)

    # Split data
    print("\n[3/5] Splitting data...")
    X_train, X_test, y_train, y_test, images_train, images_test = train_test_split(
        X, y, images, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")

    # Scale features
    print("\n[4/5] Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("   Pixel values standardized")

    # Train SVM classifier
    # SVM with RBF kernel works well for digit recognition
    print("\n[5/5] Training SVM classifier...")
    print("   (This may take a minute...)")
    model = SVC(kernel='rbf', gamma='scale', probability=True, random_state=42)
    model.fit(X_train_scaled, y_train)
    print("   Training complete!")

    # Evaluate
    print("\n[Evaluating model...]")
    train_accuracy = model.score(X_train_scaled, y_train)
    test_accuracy = model.score(X_test_scaled, y_test)

    print(f"\n   Training Accuracy: {train_accuracy:.2%}")
    print(f"   Test Accuracy: {test_accuracy:.2%}")

    # Show per-class accuracy
    from sklearn.metrics import classification_report
    y_pred = model.predict(X_test_scaled)
    print("\n   Per-class Performance:")
    print(classification_report(y_test, y_pred, digits=2))

    # Visualize predictions
    print("\n[Creating prediction visualization...]")
    visualize_predictions(images_test, y_test, y_pred, model, scaler)

    # Save model and scaler
    print("\n[Saving model...]")
    models_dir = Path(__file__).parent
    with open(models_dir / "model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(models_dir / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print(f"   Saved model.pkl and scaler.pkl")
    print("\n" + "=" * 50)
    print("Training complete! Run app.py to use the model.")
    print("=" * 50)

    return model, scaler


def visualize_samples(images, labels):
    """Visualize sample digits from each class."""
    fig, axes = plt.subplots(2, 5, figsize=(12, 5))

    # Get one sample of each digit
    for digit in range(10):
        row = digit // 5
        col = digit % 5
        idx = np.where(labels == digit)[0][0]

        axes[row, col].imshow(images[idx], cmap='gray')
        axes[row, col].set_title(f'Digit: {digit}', fontsize=14)
        axes[row, col].axis('off')

    plt.suptitle('Sample Digits from Dataset', fontsize=16)
    fig.patch.set_facecolor('#0e1117')
    plt.tight_layout()

    output_path = Path(__file__).parent / "sample_digits.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0e1117')
    plt.close()
    print(f"   Saved sample_digits.png")


def visualize_predictions(images, true_labels, pred_labels, model, scaler):
    """Visualize some predictions with confidence scores."""
    # Select random samples
    np.random.seed(42)
    n_samples = 16
    indices = np.random.choice(len(images), n_samples, replace=False)

    fig, axes = plt.subplots(4, 4, figsize=(10, 10))

    for i, idx in enumerate(indices):
        row = i // 4
        col = i % 4
        ax = axes[row, col]

        # Get image and predict
        img = images[idx].reshape(1, -1)
        img_scaled = scaler.transform(img)
        pred = model.predict(img_scaled)[0]
        proba = model.predict_proba(img_scaled)[0]
        confidence = proba[pred] * 100

        # Display image
        ax.imshow(images[idx], cmap='gray')

        # Color code: green if correct, red if wrong
        color = '#00ff00' if pred == true_labels[idx] else '#ff0000'
        ax.set_title(f'Pred: {pred} ({confidence:.0f}%)', color=color, fontsize=12)
        ax.axis('off')

    plt.suptitle('Model Predictions (Green=Correct, Red=Wrong)', fontsize=14)
    fig.patch.set_facecolor('#0e1117')
    plt.tight_layout()

    output_path = Path(__file__).parent / "predictions.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0e1117')
    plt.close()
    print(f"   Saved predictions.png")


if __name__ == "__main__":
    train_model()
