# Iris Classifier

A beginner-friendly machine learning project that classifies iris flowers into three species based on their physical measurements.

## Overview

This project demonstrates the classic Iris classification problem using the **K-Nearest Neighbors (KNN)** algorithm. It's one of the most famous datasets in machine learning history!

## ML Concepts Covered

- **K-Nearest Neighbors (KNN)**: Instance-based learning algorithm
- **Feature Scaling**: Standardizing input features
- **Decision Boundaries**: Visualizing classifier behavior
- **Multi-class Classification**: Handling 3+ classes

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
- Load the classic Iris dataset (150 samples)
- Train a K-Nearest Neighbors classifier
- Generate decision boundary visualizations
- Save model files for the web app

### 3. Run the Web App

```bash
streamlit run app.py
```

## Project Structure

```
iris-classifier/
├── app.py                   # Streamlit web application
├── train.py                # Model training script
├── model.pkl               # Trained KNN classifier (generated)
├── scaler.pkl              # Fitted StandardScaler (generated)
├── class_info.pkl          # Class names and feature info (generated)
├── decision_boundaries.png # Visualization (generated)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## The Iris Dataset

| Species | Sepal Length | Sepal Width | Petal Length | Petal Width |
|---------|-------------|-------------|--------------|-------------|
| Setosa  | 5.0 cm      | 3.4 cm      | 1.5 cm       | 0.2 cm      |
| Versicolor | 5.9 cm   | 2.8 cm      | 4.3 cm       | 1.3 cm      |
| Virginica | 6.6 cm    | 3.0 cm      | 5.6 cm       | 2.1 cm      |

## How KNN Works

1. **Store training data**: Keep all training examples in memory
2. **Calculate distance**: Measure distance from new input to all training points
3. **Find neighbors**: Select the K closest training examples
4. **Vote**: The majority class among neighbors becomes the prediction

```
New flower → Find 5 nearest → Count votes → Predict species
```

## Example Usage

Input measurements:
- Sepal: 6.0 cm x 3.0 cm
- Petal: 4.5 cm x 1.5 cm

Output: **Versicolor** (78% confidence)

## Visualizations

The training script generates decision boundary plots showing:
- How the classifier separates the three species
- Which features provide the best separation (petals > sepals)

## Further Improvements

- Add dimensionality reduction (PCA, t-SNE) for visualization
- Try different K values and compare accuracy
- Add cross-validation for more robust evaluation
- Implement other classifiers (SVM, Decision Tree)
