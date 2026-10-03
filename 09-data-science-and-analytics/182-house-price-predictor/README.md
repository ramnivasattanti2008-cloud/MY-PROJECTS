# House Price Predictor

A beginner-friendly machine learning project that predicts house prices using Linear Regression.

## Overview

This project demonstrates how to build a house price prediction model using **Linear Regression**. It generates realistic housing data and learns the relationship between house features and their prices.

## ML Concepts Covered

- **Linear Regression**: Finding the best-fit line through data
- **Feature Scaling**: Standardizing input features
- **Model Evaluation**: R² score, MAE, RMSE
- **Coefficient Interpretation**: Understanding feature impact

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
- Generate 500 sample house records
- Train a Linear Regression model
- Create visualizations
- Save model files for the web app

### 3. Run the Web App

```bash
streamlit run app.py
```

## Project Structure

```
house-price-predictor/
├── app.py                # Streamlit web application
├── train.py              # Model training script
├── model.pkl             # Trained Linear Regression model (generated)
├── scaler.pkl            # Fitted StandardScaler (generated)
├── feature_info.pkl      # Feature ranges (generated)
├── housing_data.csv      # Generated dataset (generated)
├── model_analysis.png    # Visualizations (generated)
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Features Used

| Feature | Range | Impact |
|---------|-------|--------|
| Area | 800-3200 sq ft | +$100 per sq ft |
| Bedrooms | 1-6 | +$15,000 per bedroom |
| Bathrooms | 1-4 | +$20,000 per bathroom |
| Age | 0-100 years | -$500 per year |
| Location | 1-5 (quality) | +$25,000 per level |

## How Linear Regression Works

Linear regression finds the relationship:

```
Price = β₀ + β₁×Area + β₂×Bedrooms + β₃×Bathrooms + β₄×Age + β₅×Location
```

The algorithm finds the best coefficients (β) that minimize the prediction error.

## Example Usage

Input:
- Area: 2000 sq ft
- Bedrooms: 3
- Bathrooms: 2
- Age: 10 years
- Location: 4 stars

Output: **$372,500**

## Visualizations

The training script generates:
- **Actual vs Predicted**: Shows model accuracy
- **Feature vs Price**: Individual feature relationships
- **Residual Plot**: Checks for patterns in errors

## Further Improvements

- Add more features (garage, pool, neighborhood)
- Try polynomial regression for non-linear relationships
- Use regularization (Ridge, Lasso) to prevent overfitting
- Integrate with real estate APIs for live data
