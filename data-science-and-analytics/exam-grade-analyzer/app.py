"""
Exam Grade Analyzer
A Streamlit application for analyzing student exam results
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from io import StringIO

# Page configuration
st.set_page_config(
    page_title="Exam Grade Analyzer",
    page_icon="📚",
    layout="wide"
)

# Dark theme styling
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .css-1d391kg { padding: 2rem; }
    h1, h2, h3 { color: #ffffff; }
    .upload-box { border: 2px dashed #00d4aa; border-radius: 10px; padding: 2rem; text-align: center; }
    .metric-card { background-color: #1e2530; padding: 1.5rem; border-radius: 10px; text-align: center; }
</style>
""", unsafe_allow_html=True)

def calculate_grade_percentage(marks, total_marks=100):
    """Calculate percentage from marks"""
    return (marks / total_marks) * 100

def assign_grade(percentage):
    """Assign letter grade based on percentage"""
    if percentage >= 90:
        return 'A+'
    elif percentage >= 80:
        return 'A'
    elif percentage >= 70:
        return 'B+'
    elif percentage >= 60:
        return 'B'
    elif percentage >= 50:
        return 'C'
    elif percentage >= 40:
        return 'D'
    else:
        return 'F'

def assign_grade_color(grade):
    """Get color for grade"""
    colors = {
        'A+': '#00d4aa',
        'A': '#26de81',
        'B+': '#fed330',
        'B': '#fd9644',
        'C': '#f7b731',
        'D': '#eb3b5a',
        'F': '#fc5c65'
    }
    return colors.get(grade, '#ffffff')

def main():
    st.title("📚 Exam Grade Analyzer")
    st.markdown("### Upload exam results CSV and get comprehensive analysis")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Analysis",
        ["Upload Data", "Overview", "Subject Analysis", "Student Rankings", "Visualizations"]
    )

    # Check if data is loaded
    if 'df' not in st.session_state:
        st.session_state.df = None

    # File upload section
    with st.expander("📁 Upload Exam Data", expanded=True):
        uploaded_file = st.file_uploader(
            "Choose a CSV file with exam results",
            type=['csv'],
            help="CSV should have columns: student_name, roll_no, and subject marks"
        )

        if uploaded_file is not None:
            try:
                # Read the CSV
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                st.success(f"Loaded data for {len(df)} students")

                # Show preview
                with st.expander("Preview Data"):
                    st.dataframe(df.head(10), use_container_width=True)
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

    # If no data, show sample data option
    if st.session_state.df is None:
        col1, col2 = st.columns(2)
        with col1:
            st.info("👆 Please upload a CSV file to analyze exam results")

        with col2:
            if st.button("📋 Load Sample Data"):
                df = generate_sample_data()
                st.session_state.df = df
                st.success("Sample data loaded! You can now analyze it.")

    # If data exists, show analysis pages
    if st.session_state.df is not None:
        df = st.session_state.df

        # Preprocess data
        df = preprocess_data(df)

        if page == "Upload Data":
            show_upload_info()
        elif page == "Overview":
            show_overview(df)
        elif page == "Subject Analysis":
            show_subject_analysis(df)
        elif page == "Student Rankings":
            show_student_rankings(df)
        elif page == "Visualizations":
            show_visualizations(df)

def generate_sample_data():
    """Generate sample exam data"""
    np.random.seed(42)
    n_students = 50

    students = [f"Student_{i+1}" for i in range(n_students)]
    rolls = [f"2024{str(i+1).zfill(3)}" for i in range(n_students)]

    # Generate marks for 6 subjects
    subjects = {
        'Mathematics': np.random.randint(35, 98, n_students),
        'Physics': np.random.randint(40, 95, n_students),
        'Chemistry': np.random.randint(38, 96, n_students),
        'English': np.random.randint(50, 95, n_students),
        'Computer Science': np.random.randint(45, 100, n_students),
        'Biology': np.random.randint(42, 94, n_students)
    }

    data = {
        'student_name': students,
        'roll_no': rolls
    }
    data.update(subjects)

    return pd.DataFrame(data)

def preprocess_data(df):
    """Preprocess the exam data"""
    df = df.copy()

    # Get subject columns (exclude student_name and roll_no)
    subject_cols = [col for col in df.columns if col not in ['student_name', 'roll_no', 'percentage', 'grade', 'total']]

    # Calculate total marks
    df['total'] = df[subject_cols].sum(axis=1)

    # Calculate percentage
    df['percentage'] = df['total'] / len(subject_cols)

    # Assign grades
    df['grade'] = df['percentage'].apply(assign_grade)

    return df

def show_upload_info():
    """Show information about expected data format"""
    st.header("📋 Data Format Guide")

    st.markdown("""
    ### Expected CSV Format

    Your CSV file should contain the following columns:

    | Column | Description |
    |--------|-------------|
    | `student_name` | Name of the student |
    | `roll_no` | Roll number / ID |
    | Subject columns | One column per subject with marks (e.g., Mathematics, Physics) |

    ### Example:

    ```csv
    student_name,roll_no,Mathematics,Physics,Chemistry,English
    John Doe,2024001,85,78,92,88
    Jane Smith,2024002,91,85,78,95
    ```

    ### Tips:
    - Subject columns should contain numeric marks
    - Missing values will be treated as 0
    - Marks can be on any scale (auto-normalized for analysis)
    """)

    # Show sample data format
    st.subheader("Sample Data Preview")
    sample_df = generate_sample_data()
    st.dataframe(sample_df.head(), use_container_width=True)

def show_overview(df):
    """Display overview statistics"""
    st.header("📊 Exam Overview")

    # Get subject columns
    subject_cols = [col for col in df.columns if col not in ['student_name', 'roll_no', 'percentage', 'grade', 'total']]
    n_subjects = len(subject_cols)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_students = len(df)
        st.metric("Total Students", total_students)

    with col2:
        avg_percentage = df['percentage'].mean()
        st.metric("Average Score", f"{avg_percentage:.1f}%")

    with col3:
        pass_count = len(df[df['percentage'] >= 40])
        pass_rate = (pass_count / total_students) * 100
        st.metric("Pass Rate", f"{pass_rate:.1f}%")

    with col4:
        highest_score = df['percentage'].max()
        st.metric("Highest Score", f"{highest_score:.1f}%")

    st.divider()

    # Grade distribution
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Grade Distribution")
        grade_counts = df['grade'].value_counts().sort_index()

        fig = px.bar(
            x=grade_counts.index,
            y=grade_counts.values,
            color=grade_counts.values,
            color_continuous_scale='RdYlGn',
            text=grade_counts.values
        )
        fig.update_layout(template='plotly_dark', height=400)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Score Distribution")
        fig = px.histogram(
            df,
            x='percentage',
            nbins=10,
            color_discrete_sequence=['#00d4aa']
        )
        fig.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Additional stats
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        fail_count = len(df[df['percentage'] < 40])
        st.metric("Failed Students", fail_count)

    with col2:
        distinction = len(df[df['percentage'] >= 75])
        st.metric("Distinction (75%+)", distinction)

    with col3:
        first_class = len(df[(df['percentage'] >= 60) & (df['percentage'] < 75)])
        st.metric("First Class (60-75%)", first_class)

    with col4:
        std_dev = df['percentage'].std()
        st.metric("Std Deviation", f"{std_dev:.2f}")

def show_subject_analysis(df):
    """Analyze performance by subject"""
    st.header("📖 Subject-wise Analysis")

    # Get subject columns
    subject_cols = [col for col in df.columns if col not in ['student_name', 'roll_no', 'percentage', 'grade', 'total']]

    # Subject statistics
    subject_stats = []
    for subject in subject_cols:
        stats = {
            'Subject': subject,
            'Average': df[subject].mean(),
            'Highest': df[subject].max(),
            'Lowest': df[subject].min(),
            'Std Dev': df[subject].std(),
            'Pass %': (df[subject] >= 40).sum() / len(df) * 100
        }
        subject_stats.append(stats)

    stats_df = pd.DataFrame(subject_stats)
    st.dataframe(
        stats_df.style.background_gradient(subset=['Average'], cmap='Greens'),
        use_container_width=True
    )

    st.divider()

    # Subject comparison chart
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Average Score by Subject")
        fig = px.bar(
            x=stats_df['Subject'],
            y=stats_df['Average'],
            color=stats_df['Average'],
            color_continuous_scale='Viridis',
            text=stats_df['Average'].round(1)
        )
        fig.update_layout(template='plotly_dark', height=400)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Pass Percentage by Subject")
        fig = px.bar(
            x=stats_df['Subject'],
            y=stats_df['Pass %'],
            color=stats_df['Pass %'],
            color_continuous_scale='RdYlGn',
            text=stats_df['Pass %'].round(1)
        )
        fig.update_layout(template='plotly_dark', height=400)
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    # Box plot for subject distribution
    st.subheader("Subject Score Distribution")
    fig = px.box(
        df[subject_cols].melt(),
        x='variable',
        y='value',
        color='variable',
        labels={'variable': 'Subject', 'value': 'Marks'}
    )
    fig.update_layout(template='plotly_dark', height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def show_student_rankings(df):
    """Display student rankings"""
    st.header("🏆 Student Rankings")

    # Sort by percentage
    ranked_df = df.sort_values('percentage', ascending=False).reset_index(drop=True)
    ranked_df.index = ranked_df.index + 1
    ranked_df.index.name = 'Rank'

    # Display top performers
    st.subheader("Top 10 Performers")
    display_cols = ['student_name', 'roll_no', 'total', 'percentage', 'grade']
    st.dataframe(
        ranked_df[display_cols].head(10).style.background_gradient(subset=['percentage'], cmap='Greens'),
        use_container_width=True
    )

    st.divider()

    # Search for student
    col1, col2 = st.columns([2, 1])

    with col1:
        search_name = st.text_input("Search Student by Name")

    with col2:
        search_roll = st.text_input("Search by Roll No")

    if search_name:
        results = df[df['student_name'].str.contains(search_name, case=False)]
        if len(results) > 0:
            st.subheader(f"Search Results for '{search_name}'")
            st.dataframe(results[display_cols], use_container_width=True)
        else:
            st.warning("No students found")

    if search_roll:
        results = df[df['roll_no'].astype(str).str.contains(search_roll, case=False)]
        if len(results) > 0:
            st.subheader(f"Search Results for Roll No '{search_roll}'")
            st.dataframe(results[display_cols], use_container_width=True)
        else:
            st.warning("No students found")

    st.divider()

    # Bottom performers
    st.subheader("Students Needing Attention (Below 40%)")
    low_performers = df[df['percentage'] < 40][display_cols]
    if len(low_performers) > 0:
        st.dataframe(
            low_performers.style.background_gradient(subset=['percentage'], cmap='Reds'),
            use_container_width=True
        )
    else:
        st.success("All students passed!")

    # Subject-wise weak students
    st.subheader("Students with Lowest Marks per Subject")
    subject_cols = [col for col in df.columns if col not in ['student_name', 'roll_no', 'percentage', 'grade', 'total']]

    for subject in subject_cols:
        lowest = df.nsmallest(3, subject)[['student_name', subject]]
        if len(lowest) > 0 and lowest[subject].min() < 40:
            st.markdown(f"**{subject}**: {lowest.iloc[0]['student_name']} ({lowest.iloc[0][subject]})")

def show_visualizations(df):
    """Display various visualizations"""
    st.header("📊 Visual Analytics")

    subject_cols = [col for col in df.columns if col not in ['student_name', 'roll_no', 'percentage', 'grade', 'total']]

    # Student performance overview
    st.subheader("Individual Student Performance")

    # Student selector
    student = st.selectbox("Select Student", df['student_name'].unique())
    student_data = df[df['student_name'] == student].iloc[0]

    # Radar chart for student
    subjects = subject_cols
    marks = [student_data[sub] for sub in subjects]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=marks + [marks[0]],
        theta=subjects + [subjects[0]],
        fill='toself',
        name=student,
        line_color='#00d4aa'
    ))

    # Add average line
    avg_marks = [df[sub].mean() for sub in subjects]
    fig.add_trace(go.Scatterpolar(
        r=avg_marks + [avg_marks[0]],
        theta=subjects + [subjects[0]],
        fill='toself',
        name='Class Average',
        line_color='#ff6b6b'
    ))

    fig.update_layout(
        polar=dict(bgcolor='#1e2530'),
        showlegend=True,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # Heatmap
    st.subheader("Performance Heatmap")
    heatmap_data = df[subject_cols].T
    heatmap_data.columns = df['student_name'].values[:20]  # Limit to first 20 for readability

    fig = px.imshow(
        heatmap_data,
        labels=dict(x="Student", y="Subject", color="Marks"),
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Scatter plot: Total vs Average
    st.subheader("Performance Distribution")
    fig = px.scatter(
        df,
        x='total',
        y='percentage',
        color='grade',
        hover_data=['student_name'],
        labels={'total': 'Total Marks', 'percentage': 'Percentage'}
    )
    fig.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Subject correlation
    st.subheader("Subject Correlation")
    corr_matrix = df[subject_cols].corr()

    fig = px.imshow(
        corr_matrix,
        labels=dict(color="Correlation"),
        x=subject_cols,
        y=subject_cols,
        color_continuous_scale='RdBu'
    )
    fig.update_layout(template='plotly_dark', height=500)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
