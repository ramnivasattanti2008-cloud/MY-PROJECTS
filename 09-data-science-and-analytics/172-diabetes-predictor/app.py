"""
Diabetes Risk Predictor
A Streamlit application for predicting diabetes risk using machine learning
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="🏥",
    layout="wide"
)

# Dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .css-1d391kg { padding: 2rem; }
    h1, h2, h3 { color: #ffffff; }
    .risk-low { background-color: #1e3a1e; padding: 1rem; border-radius: 10px; border-left: 4px solid #00d4aa; }
    .risk-medium { background-color: #3a3a1e; padding: 1rem; border-radius: 10px; border-left: 4px solid #feca57; }
    .risk-high { background-color: #3a1e1e; padding: 1rem; border-radius: 10px; border-left: 4px solid #ff6b6b; }
    .info-box { background-color: #1e2530; padding: 1rem; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_data():
    """Load the Pima Indians Diabetes dataset"""
    # Using sklearn's built-in dataset or creating from known statistics
    # Pima Indians Diabetes Dataset characteristics
    data = {
        'Pregnancies': [6, 1, 8, 1, 0, 5, 3, 10, 2, 8, 4, 6, 10, 10, 0, 7, 6, 4, 1, 5, 8, 1, 5, 7, 4, 7, 1, 3, 8, 7, 9, 2, 4, 3, 0, 2, 5, 6, 5, 6],
        'Glucose': [148, 85, 183, 89, 137, 116, 78, 115, 197, 125, 110, 168, 139, 135, 68, 88, 156, 93, 129, 142, 128, 110, 136, 132, 120, 78, 180, 106, 117, 105],
        'BloodPressure': [72, 66, 64, 66, 40, 74, 50, 64, 70, 96, 92, 88, 62, 68, 62, 52, 92, 58, 86, 64, 78, 60, 76, 64, 80, 58, 90, 56, 58, 70],
        'SkinThickness': [35, 29, 29, 23, 35, 19, 32, 0, 47, 27, 0, 0, 23, 0, 0, 0, 30, 16, 15, 19, 0, 23, 31, 0, 0, 23, 31, 0, 19, 0],
        'Insulin': [155, 0, 0, 94, 168, 0, 0, 0, 543, 0, 0, 0, 0, 0, 0, 0, 175, 0, 0, 0, 84, 0, 53, 0, 0, 380, 0, 0, 71, 0],
        'BMI': [33.6, 26.6, 23.3, 28.1, 43.1, 25.6, 30.1, 35.3, 30.5, 30.1, 37.6, 38.5, 27.1, 43.3, 31.0, 24.7, 30.8, 27.9, 23.3, 24.2, 35.4, 24.0, 35.5, 35.0, 29.6, 30.1, 30.0, 24.3, 28.0, 31.2],
        'DiabetesPedigreeFunction': [0.627, 0.351, 0.672, 0.167, 2.288, 0.201, 0.248, 0.134, 0.158, 0.232, 0.191, 0.397, 0.141, 1.441, 0.382, 0.207, 0.906, 0.344, 0.231, 0.361, 0.387, 0.140, 0.155, 0.289, 0.381, 0.526, 0.398, 0.290, 0.694, 0.529],
        'Age': [50, 31, 32, 21, 33, 30, 31, 32, 53, 53, 52, 50, 32, 35, 26, 34, 30, 33, 40, 45, 47, 28, 39, 26, 31, 33, 29, 33, 30, 46],
        'Outcome': [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1]
    }
    df = pd.DataFrame(data)
    return df

@st.cache_resource
def train_model():
    """Train the diabetes prediction model"""
    df = load_data()

    # Features and target
    X = df.drop('Outcome', axis=1)
    y = df['Outcome']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train model
    model = GradientBoostingClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Evaluate
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    return model, scaler, accuracy, X.columns.tolist()

def get_risk_level(probability):
    """Determine risk level based on probability"""
    if probability < 0.3:
        return "low", "Low Risk", "Your risk of diabetes is low. Maintain a healthy lifestyle."
    elif probability < 0.6:
        return "medium", "Moderate Risk", "You have moderate risk. Consider lifestyle changes and consult a doctor."
    else:
        return "high", "High Risk", "Your risk of diabetes is high. Please consult a healthcare professional."

def get_recommendations(input_data, prediction, probability):
    """Generate health recommendations based on input"""
    recommendations = []

    glucose = input_data['Glucose']
    bmi = input_data['BMI']
    age = input_data['Age']
    bp = input_data['BloodPressure']

    if glucose > 140:
        recommendations.append("Monitor your blood sugar levels regularly")
        recommendations.append("Reduce intake of refined carbohydrates and sugars")

    if bmi > 25:
        recommendations.append("Consider weight management through diet and exercise")
        recommendations.append("Aim for at least 150 minutes of physical activity per week")

    if age > 40:
        recommendations.append("Schedule regular health check-ups")

    if bp > 80:
        recommendations.append("Monitor your blood pressure")
        recommendations.append("Reduce sodium intake")

    if len(recommendations) == 0:
        recommendations.append("Maintain your current healthy lifestyle")
        recommendations.append("Continue regular exercise and balanced diet")

    return recommendations

def main():
    st.title("🏥 Diabetes Risk Predictor")
    st.markdown("### Predict your diabetes risk using health metrics")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select",
        ["Risk Assessment", "Model Info", "Statistics"]
    )

    # Train model
    model, scaler, accuracy, feature_names = train_model()

    if page == "Risk Assessment":
        show_prediction_page(model, scaler, accuracy, feature_names)
    elif page == "Model Info":
        show_model_info(accuracy)
    elif page == "Statistics":
        show_statistics()

def show_prediction_page(model, scaler, accuracy, feature_names):
    """Main prediction page"""
    st.header("📋 Health Assessment")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Enter Your Health Metrics")

        # Input fields with sliders
        pregnancies = st.slider("Pregnancies", 0, 15, 1, help="Number of pregnancies")
        glucose = st.slider("Glucose Level (mg/dL)", 50, 200, 100, help="Plasma glucose concentration")
        blood_pressure = st.slider("Blood Pressure (mmHg)", 40, 140, 70, help="Diastolic blood pressure")
        skin_thickness = st.slider("Skin Thickness (mm)", 0, 80, 20, help="Triceps skin fold thickness")
        insulin = st.slider("Insulin Level (mu U/ml)", 0, 300, 80, help="2-Hour serum insulin")
        bmi = st.slider("BMI (kg/m²)", 15.0, 50.0, 25.0, 0.1, help="Body mass index")
        dpf = st.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.5, 0.01, help="Diabetes hereditary factor")
        age = st.slider("Age (years)", 18, 80, 30, help="Age in years")

    with col2:
        st.subheader("Risk Assessment Results")

        # Predict button
        if st.button("🔮 Predict Risk", type="primary", use_container_width=True):
            # Prepare input data
            input_data = {
                'Pregnancies': pregnancies,
                'Glucose': glucose,
                'BloodPressure': blood_pressure,
                'SkinThickness': skin_thickness,
                'Insulin': insulin,
                'BMI': bmi,
                'DiabetesPedigreeFunction': dpf,
                'Age': age
            }

            # Create DataFrame for prediction
            input_df = pd.DataFrame([input_data])

            # Scale and predict
            input_scaled = scaler.transform(input_df)
            probability = model.predict_proba(input_scaled)[0][1]
            prediction = model.predict(input_scaled)[0]

            # Get risk level
            risk_level, risk_label, risk_message = get_risk_level(probability)

            # Display result
            if risk_level == "low":
                st.markdown(f"""
                <div class="risk-low">
                    <h3>{risk_label}</h3>
                    <p>{risk_message}</p>
                    <p><strong>Risk Probability: {probability*100:.1f}%</strong></p>
                </div>
                """, unsafe_allow_html=True)
            elif risk_level == "medium":
                st.markdown(f"""
                <div class="risk-medium">
                    <h3>{risk_label}</h3>
                    <p>{risk_message}</p>
                    <p><strong>Risk Probability: {probability*100:.1f}%</strong></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="risk-high">
                    <h3>{risk_label}</h3>
                    <p>{risk_message}</p>
                    <p><strong>Risk Probability: {probability*100:.1f}%</strong></p>
                </div>
                """, unsafe_allow_html=True)

            # Risk gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': '#00d4aa' if probability < 0.3 else '#feca57' if probability < 0.6 else '#ff6b6b'},
                    'steps': [
                        {'range': [0, 30], 'color': '#00d4aa'},
                        {'range': [30, 60], 'color': '#feca57'},
                        {'range': [60, 100], 'color': '#ff6b6b'}
                    ]
                },
                title={'text': "Risk Probability %"}
            ))
            fig.update_layout(template='plotly_dark', height=250)
            st.plotly_chart(fig, use_container_width=True)

            # Recommendations
            st.divider()
            st.subheader("💡 Recommendations")
            recommendations = get_recommendations(input_data, prediction, probability)
            for rec in recommendations:
                st.write(f"• {rec}")

            # Display input summary
            with st.expander("📊 Your Input Summary"):
                summary_df = pd.DataFrame([input_data])
                st.dataframe(summary_df.T, use_container_width=True)

    # Model accuracy info
    st.divider()
    st.info(f"Model Accuracy: {accuracy*100:.1f}% (based on historical Pima Indians data)")

def show_model_info(accuracy):
    """Display model information"""
    st.header("ℹ️ Model Information")

    st.markdown("""
    ### About This Predictor

    This diabetes risk predictor uses the **Pima Indians Diabetes Dataset** to train a machine learning model.

    **Features Used:**
    - Number of pregnancies
    - Glucose concentration
    - Blood pressure
    - Skin thickness
    - Insulin level
    - BMI (Body Mass Index)
    - Diabetes Pedigree Function (hereditary factor)
    - Age
    """)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-box">
            <h4>Model Type</h4>
            <p>Gradient Boosting Classifier</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
            <h4>Training Data</h4>
            <p>Pima Indians Diabetes Dataset</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="info-box">
            <h4>Accuracy</h4>
            <p>{accuracy*100:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
            <h4>Algorithm</h4>
            <p>Scikit-learn GradientBoostingClassifier</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    ### Risk Categories

    | Risk Level | Probability | Description |
    |------------|-------------|-------------|
    | Low Risk | < 30% | Healthy lifestyle recommended |
    | Moderate Risk | 30-60% | Consider lifestyle changes |
    | High Risk | > 60% | Consult healthcare professional |

    ### Important Disclaimer

    This tool is for educational purposes only and should not replace professional medical advice.
    Always consult a healthcare provider for proper diagnosis and treatment.
    """)

def show_statistics():
    """Display dataset statistics"""
    st.header("📊 Dataset Statistics")

    df = load_data()

    # Overview stats
    col1, col2, col3 = st.columns(3)

    with col1:
        total = len(df)
        st.metric("Total Records", total)

    with col2:
        positive = df['Outcome'].sum()
        st.metric("Diabetes Positive", positive)

    with col3:
        negative = total - positive
        st.metric("Diabetes Negative", negative)

    st.divider()

    # Feature distributions
    st.subheader("Feature Distributions by Outcome")

    feature = st.selectbox("Select Feature", df.columns[:-1])

    fig = px.histogram(
        df,
        x=feature,
        color='Outcome',
        barmode='overlay',
        opacity=0.7,
        color_discrete_map={0: '#00d4aa', 1: '#ff6b6b'}
    )
    fig.update_layout(template='plotly_dark', height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Correlation heatmap
    st.subheader("Feature Correlation")
    corr_matrix = df.corr()

    fig = px.imshow(
        corr_matrix,
        labels=dict(color="Correlation"),
        color_continuous_scale='RdBu'
    )
    fig.update_layout(template='plotly_dark', height=600)
    st.plotly_chart(fig, use_container_width=True)

    # Summary statistics
    st.subheader("Summary Statistics")
    st.dataframe(df.describe(), use_container_width=True)

if __name__ == "__main__":
    main()
