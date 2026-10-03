# Digit Recognizer

A beginner-friendly machine learning project that recognizes handwritten digits (0-9) using Support Vector Machines.

## Overview

This project demonstrates digit recognition using the classic **MNIST-style digit dataset**. It's a great introduction to image classification and computer vision fundamentals.

## ML Concepts Covered

- **Image Classification**: Recognizing patterns in pixel data
- **Support Vector Machine (SVM)**: A powerful classifier with RBF kernel
- **Feature Scaling**: Normalizing pixel values
- **Probability Estimation**: Getting confidence scores

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
- Load the digit dataset (1,797 samples, 8x8 pixels each)
- Train an SVM classifier
- Create visualizations
- Save model files for the web app

### 3. Run the Web App

```bash
streamlit run app.py
```

## Project Structure

```
digit-recognizer/
├── app.py              # Streamlit web application
├── train.py            # Model training script
├── model.pkl           # Trained SVM classifier (generated)
├── scaler.pkl          # Fitted StandardScaler (generated)
├── sample_digits.png   # Sample digit visualization (generated)
├── predictions.png     # Prediction examples (generated)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## The Digit Dataset

The dataset contains 8x8 grayscale images of handwritten digits:
- **1,797 total samples**
- **10 classes** (digits 0-9)
- **64 features** (8x8 = 64 pixel values)
- Each pixel value: 0-16 (normalized intensity)

## How SVM Works

The **Support Vector Machine** with RBF kernel works by:

1. **Mapping**: Projects data into higher-dimensional space
2. **Finding boundaries**: Identifies optimal separating hyperplane
3. **Support vectors**: Uses critical data points near boundaries
4. **Classification**: New points are classified based on which side they fall

## How It Works in This App

1. Upload an image of a handwritten digit
2. Image is preprocessed (resized to 8x8, normalized)
3. SVM predicts the digit class
4. Probability scores show confidence for each digit

## Example Usage

Upload an image of the digit "7":
- Output: **7** (94.2% confidence)

## Visualizations

The training script generates:
- **Sample digits**: One example of each digit 0-9
- **Prediction grid**: Shows model predictions with confidence

## Further Improvements

- Use the full MNIST dataset (70,000 images, 28x28 pixels)
- Add data augmentation (rotation, scaling)
- Try convolutional neural networks (CNN)
- Implement real-time webcam recognition
