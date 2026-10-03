# Diabetes Risk Predictor 🏥

A machine learning application that predicts diabetes risk based on health metrics using the Pima Indians Diabetes Dataset.

## Features

- **Risk Assessment**: Input health metrics and get instant diabetes risk prediction
- **Visual Risk Gauge**: Interactive probability gauge showing risk level
- **Personalized Recommendations**: Health recommendations based on input
- **Model Information**: Detailed information about the ML model
- **Dataset Statistics**: Explore the training data with interactive charts

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## Input Metrics

| Metric | Range | Description |
|--------|-------|-------------|
| Pregnancies | 0-15 | Number of pregnancies |
| Glucose | 50-200 mg/dL | Plasma glucose concentration |
| Blood Pressure | 40-140 mmHg | Diastolic blood pressure |
| Skin Thickness | 0-80 mm | Triceps skin fold thickness |
| Insulin | 0-300 mu U/ml | 2-Hour serum insulin |
| BMI | 15-50 kg/m² | Body mass index |
| Diabetes Pedigree | 0-2.5 | Hereditary diabetes factor |
| Age | 18-80 years | Age in years |

## Risk Categories

| Risk Level | Probability | Color |
|------------|-------------|-------|
| Low Risk | < 30% | Green |
| Moderate Risk | 30-60% | Yellow |
| High Risk | > 60% | Red |

## Machine Learning Model

- **Algorithm**: Gradient Boosting Classifier
- **Training Data**: Pima Indians Diabetes Dataset
- **Accuracy**: ~80% (varies based on data split)

## Tech Stack

- Streamlit - Web framework
- Scikit-learn - Machine learning
- Pandas - Data manipulation
- Plotly - Interactive visualizations
- NumPy - Numerical computing

## Disclaimer

This tool is for educational purposes only and should not replace professional medical advice. Always consult a healthcare provider for proper diagnosis and treatment.

## License

MIT License
