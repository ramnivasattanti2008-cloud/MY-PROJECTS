"""
Iris Classifier Training Script
Trains a classifier to predict iris flower species based on measurements.
Uses the famous Iris dataset from scikit-learn.
"""

import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


def load_data():
    """
    Load the Iris dataset.
    This is a classic dataset with 150 samples of iris flowers,
    each having 4 features: sepal length, sepal width, petal length, petal width.
    """
    iris = datasets.load_iris()
    return iris


def train_model():
    """
    Main training pipeline:
    1. Load iris dataset
    2. Split into train/test sets
    3. Scale features for better performance
    4. Train a K-Nearest Neighbors classifier
    5. Evaluate and visualize decision boundaries
    """
    print("=" * 50)
    print("IRIS CLASSIFIER - Training Pipeline")
    print("=" * 50)

    # Load data
    print("\n[1/5] Loading Iris dataset...")
    iris = load_data()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names

    print(f"   Features: {feature_names}")
    print(f"   Classes: {list(target_names)}")
    print(f"   Samples: {len(X)}")

    # Split data
    print("\n[2/5] Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")

    # Scale features
    print("\n[3/5] Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("   Features standardized (mean=0, std=1)")

    # Train KNN classifier
    # KNN is intuitive: find the K closest training examples and vote
    print("\n[4/5] Training K-Nearest Neighbors classifier (K=5)...")
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train_scaled, y_train)
    print("   Training complete!")

    # Evaluate
    print("\n[5/5] Evaluating model...")
    train_accuracy = model.score(X_train_scaled, y_train)
    test_accuracy = model.score(X_test_scaled, y_test)

    print(f"\n   Training Accuracy: {train_accuracy:.2%}")
    print(f"   Test Accuracy: {test_accuracy:.2%}")

    # Visualize decision boundaries
    print("\n[Creating visualization...]")
    visualize_decision_boundaries(X_train_scaled, X_train, y_train, feature_names, target_names)

    # Save model and scaler
    print("\n[Saving model...]")
    models_dir = Path(__file__).parent
    with open(models_dir / "model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(models_dir / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f

    # Save class information
    class_info = {
        "target_names": list(target_names),
        "feature_names": list(feature_names),
        "feature_ranges": {
            name: (X[:, i].min(), X[:, i].max())
            for i, name in enumerate(feature_names)
        }
    }
    with open(models_dir / "class_info.pkl", "wb") as f:
        pickle.dump(class_info, f)

    print(f"   Saved model.pkl, scaler.pkl, class_info.pkl")
    print("\n" + "=" * 50)
    print("Training complete! Run app.py to use the model.")
    print("=" * 50)

    return model, scaler, class_info


def visualize_decision_boundaries(X_train, X_original, y_train, feature_names, target_names):
    """
    Create visualizations showing decision boundaries.
    We'll use the two most important features for visualization.
    """
    # Use petal length and petal width (indices 2 and 3) - they provide best separation
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Decision boundary with scaled features
    ax1 = axes[0]
    # Use first two scaled features for visualization
    X_2d = X_train[:, :2]

    clf = KNeighborsClassifier(n_neighbors=5)
    clf.fit(X_2d, y_train)

    disp = DecisionBoundaryDisplay.from_estimator(
        clf, X_2d, response_method="predict",
        ax=ax1, cmap='viridis', alpha=0.4
    )

    # Plot training points
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    for i, color, target_name in zip(range(3), colors, target_names):
        idx = y_train == i
        ax1.scatter(X_2d[idx, 0], X_2d[idx, 1], c=color,
                   label=target_name, edgecolor='black', s=50)

    ax1.set_xlabel('Sepal Length (scaled)')
    ax1.set_ylabel('Sepal Width (scaled)')
    ax1.set_title('Decision Boundary (Sepal Features)')
    ax1.legend()

    # Plot 2: Petal features (better separation)
    ax2 = axes[1]
    X_2d = X_train[:, 2:4]

    clf2 = KNeighborsClassifier(n_neighbors=5)
    clf2.fit(X_2d, y_train)

    disp2 = DecisionBoundaryDisplay.from_estimator(
        clf2, X_2d, response_method="predict",
        ax=ax2, cmap='viridis', alpha=0.4
    )

    for i, color, target_name in zip(range(3), colors, target_names):
        idx = y_train == i
        ax2.scatter(X_2d[idx, 0], X_2d[idx, 1], c=color,
                   label=target_name, edgecolor='black', s=50)

    ax2.set_xlabel('Petal Length (scaled)')
    ax2.set_ylabel('Petal Width (scaled)')
    ax2.set_title('Decision Boundary (Petal Features)')
    ax2.legend()

    plt.tight_layout()

    # Save figure
    output_path = Path(__file__).parent / "decision_boundaries.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   Saved decision_boundaries.png")


if __name__ == "__main__":
    train_model()
