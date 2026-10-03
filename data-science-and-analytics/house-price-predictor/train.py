"""
House Price Predictor Training Script
Trains a linear regression model to predict house prices.
Uses a sample dataset with features like area, bedrooms, etc.
"""

import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def generate_sample_data():
    """
    Generate a sample dataset for demonstration.
    Creates realistic housing data with:
    - Area (sq ft)
    - Bedrooms
    - Bathrooms
    - Age (years)
    - Location quality (1-5)
    """
    np.random.seed(42)
    n_samples = 500

    # Generate features
    area = np.random.normal(2000, 600, n_samples)  # Average 2000 sq ft
    bedrooms = np.random.choice([2, 3, 4, 5], n_samples, p=[0.2, 0.4, 0.3, 0.1])
    bathrooms = np.random.choice([1, 1.5, 2, 2.5, 3], n_samples, p=[0.15, 0.25, 0.35, 0.15, 0.1])
    age = np.random.exponential(15, n_samples)  # Average 15 years old
    location = np.random.choice([1, 2, 3, 4, 5], n_samples, p=[0.1, 0.2, 0.35, 0.25, 0.1])

    # Create price based on features (with some noise)
    # Price = base + area*coef + bedrooms*coef + ... + noise
    base_price = 50000
    price = (
        base_price
        + area * 100  # $100 per sq ft
        + bedrooms * 15000  # $15k per bedroom
        + bathrooms * 20000  # $20k per bathroom
        - age * 500  # $500 per year of age
        + location * 25000  # $25k per location quality point
        + np.random.normal(0, 15000, n_samples)  # Random noise
    )

    # Ensure positive prices
    price = np.maximum(price, 50000)

    # Create DataFrame
    df = pd.DataFrame({
        'area': area,
        'bedrooms': bedrooms.astype(int),
        'bathrooms': bathrooms,
        'age': age,
        'location': location.astype(int),
        'price': price
    })

    return df


def train_model():
    """
    Main training pipeline:
    1. Generate/sample housing data
    2. Split into train/test sets
    3. Scale features
    4. Train Linear Regression model
    5. Evaluate and visualize
    """
    print("=" * 50)
    print("HOUSE PRICE PREDICTOR - Training Pipeline")
    print("=" * 50)

    # Load or generate data
    print("\n[1/5] Generating sample housing data...")
    df = generate_sample_data()

    data_path = Path(__file__).parent / "housing_data.csv"
    df.to_csv(data_path, index=False)
    print(f"   Generated {len(df)} samples")
    print(f"   Saved to {data_path}")

    print("\n   Dataset Summary:")
    print(df.describe().round(2))

    # Prepare features and target
    print("\n[2/5] Preparing features...")
    X = df[['area', 'bedrooms', 'bathrooms', 'age', 'location']]
    y = df['price']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")

    # Scale features
    print("\n[3/5] Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("   Features standardized")

    # Train model
    print("\n[4/5] Training Linear Regression model...")
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    print("   Training complete!")

    # Show coefficients
    print("\n   Feature Coefficients:")
    feature_names = ['area', 'bedrooms', 'bathrooms', 'age', 'location']
    for name, coef in zip(feature_names, model.coef_):
        print(f"   {name:12s}: ${coef:+,.0f} per unit")

    # Evaluate
    print("\n[5/5] Evaluating model...")
    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)

    # Calculate MAE and RMSE
    y_pred = model.predict(X_test_scaled)
    mae = np.mean(np.abs(y_test - y_pred))
    rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))

    print(f"\n   R² Score (Train): {train_score:.4f}")
    print(f"   R² Score (Test):  {test_score:.4f}")
    print(f"   Mean Absolute Error: ${mae:,.0f}")
    print(f"   Root Mean Square Error: ${rmse:,.0f}")

    # Visualize
    print("\n[Creating visualizations...]")
    visualize_results(X, y, model, scaler, feature_names)

    # Save model and scaler
    print("\n[Saving model...]")
    models_dir = Path(__file__).parent
    with open(models_dir / "model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(models_dir / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    # Save feature info
    feature_info = {
        "feature_names": feature_names,
        "feature_ranges": {
            name: (X[name].min(), X[name].max())
            for name in feature_names
        }
    }
    with open(models_dir / "feature_info.pkl", "wb") as f:
        pickle.dump(feature_info, f)

    print(f"   Saved model.pkl, scaler.pkl, feature_info.pkl")
    print("\n" + "=" * 50)
    print("Training complete! Run app.py to use the model.")
    print("=" * 50)

    return model, scaler, feature_info


def visualize_results(X, y, model, scaler, feature_names):
    """Create visualizations of the model results."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # Plot 1: Actual vs Predicted
    ax = axes[0, 0]
    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)
    ax.scatter(y, y_pred, alpha=0.5, c='#00d4ff')
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2)
    ax.set_xlabel('Actual Price ($)')
    ax.set_ylabel('Predicted Price ($)')
    ax.set_title('Actual vs Predicted')
    ax.set_facecolor('#1e2530')
    fig.patch.set_facecolor('#0e1117')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')

    # Feature vs Price plots
    colors = ['#ff6b9d', '#4ecdc4', '#45b7d1', '#ffd93d', '#6bcb77']
    for i, (name, color) in enumerate(zip(feature_names, colors)):
        row = (i + 1) // 3
        col = (i + 1) % 3
        ax = axes[row, col]
        ax.scatter(X[name], y, alpha=0.5, c=color)
        ax.set_xlabel(name.title())
        ax.set_ylabel('Price ($)')
        ax.set_title(f'{name.title()} vs Price')
        ax.set_facecolor('#1e2530')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')

    # Residuals plot
    ax = axes[1, 2]
    residuals = y - y_pred
    ax.scatter(y_pred, residuals, alpha=0.5, c='#ff6b9d')
    ax.axhline(y=0, color='white', linestyle='--')
    ax.set_xlabel('Predicted Price ($)')
    ax.set_ylabel('Residuals ($)')
    ax.set_title('Residual Plot')
    ax.set_facecolor('#1e2530')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')

    plt.tight_layout()

    output_path = Path(__file__).parent / "model_analysis.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#0e1117')
    plt.close()
    print(f"   Saved model_analysis.png")


if __name__ == "__main__":
    train_model()
