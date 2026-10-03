import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Grade Calculator & Analyzer", page_icon="📊", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #ffffff !important; }
    .grade-a { color: #4ade80; }
    .grade-b { color: #22c55e; }
    .grade-c { color: #eab308; }
    .grade-d { color: #f97316; }
    .grade-f { color: #ef4444; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Grade Calculator & Analyzer")
st.markdown("Calculate your GPA and visualize your academic performance")

# Subject definitions
SUBJECTS = ["Mathematics", "Physics", "Chemistry", "Biology", "English", "History",
            "Computer Science", "Economics", "Art", "Music", "Geography", "Psychology"]

# Credit hours for each subject
CREDITS = {"Mathematics": 4, "Physics": 4, "Chemistry": 4, "Biology": 3, "English": 3,
           "History": 3, "Computer Science": 4, "Economics": 3, "Art": 2, "Music": 2,
           "Geography": 3, "Psychology": 3}

# Grade point scale
GRADE_POINTS = {"A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
                "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "D-": 0.7, "F": 0.0}

GRADE_COLORS = {"A+": "#4ade80", "A": "#22c55e", "A-": "#86efac", "B+": "#3b82f6",
                "B": "#2563eb", "B-": "#60a5fa", "C+": "#eab308", "C": "#ca8a04",
                "C-": "#fbbf24", "D+": "#f97316", "D": "#ea580c", "D-": "#fb923c", "F": "#ef4444"}

# Initialize session state
if "grades" not in st.session_state:
    st.session_state.grades = {subj: {"marks": None, "credits": CREDITS[subj]} for subj in SUBJECTS}

# Input section
st.sidebar.header("📝 Enter Your Marks")

for subj in SUBJECTS:
    marks = st.sidebar.number_input(f"{subj} ({CREDITS[subj]} credits)",
                                   min_value=0, max_value=100, value=None, step=1,
                                   key=f"marks_{subj}")
    if marks is not None:
        st.session_state.grades[subj]["marks"] = marks

# Calculate grade from marks
def get_grade(marks):
    if marks is None: return None
    if marks >= 90: return "A+"
    elif marks >= 85: return "A"
    elif marks >= 80: return "A-"
    elif marks >= 75: return "B+"
    elif marks >= 70: return "B"
    elif marks >= 65: return "B-"
    elif marks >= 60: return "C+"
    elif marks >= 55: return "C"
    elif marks >= 50: return "C-"
    elif marks >= 45: return "D+"
    elif marks >= 40: return "D"
    elif marks >= 35: return "D-"
    else: return "F"

# Prepare data
data = []
for subj, info in st.session_state.grades.items():
    if info["marks"] is not None:
        grade = get_grade(info["marks"])
        grade_point = GRADE_POINTS[grade]
        quality_points = grade_point * info["credits"]
        data.append({
            "Subject": subj, "Marks": info["marks"], "Credits": info["credits"],
            "Grade": grade, "Grade Point": grade_point, "Quality Points": quality_points
        })

df = pd.DataFrame(data)

# Calculate GPA
if len(df) > 0:
    total_quality_points = df["Quality Points"].sum()
    total_credits = df["Credits"].sum()
    gpa = total_quality_points / total_credits if total_credits > 0 else 0
else:
    gpa = 0
    total_quality_points = 0
    total_credits = 0

# Display GPA
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("📚 Subjects Entered", len(df))
col2.metric("🎯 Total Credits", total_credits)
col3.metric("📈 GPA", f"{gpa:.2f}")
col4.metric("🏆 Total Quality Points", f"{total_quality_points:.1f}")

# GPA indicator
gpa_color = "#4ade80" if gpa >= 3.5 else "#eab308" if gpa >= 2.5 else "#ef4444"
st.markdown(f"""
<div style="background: #161b22; padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;">
    <h2 style="color: {gpa_color}; font-size: 4rem; margin: 0;">{gpa:.2f}</h2>
    <p style="color: #888; font-size: 1.2rem;">Cumulative GPA</p>
</div>
""", unsafe_allow_html=True)

# Charts
if len(df) > 0:
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📊 Subject Performance", "🎓 Grade Distribution", "📈 Progress Analysis"])

    with tab1:
        # Bar chart of marks
        fig = px.bar(df.sort_values("Marks"), x="Subject", y="Marks",
                     title="Marks by Subject",
                     color="Grade", color_discrete_map=GRADE_COLORS,
                     text="Marks")
        fig.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="Pass Line (60)")
        fig.update_layout(template="plotly_dark", height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Horizontal bar chart
        fig2 = px.bar(df.sort_values("Marks", ascending=True), x="Marks", y="Subject",
                      title="Subject Performance (Sorted)",
                      color="Marks", color_continuous_scale="RdYlGn",
                      orientation="h", text="Marks")
        fig2.update_layout(template="plotly_dark", height=600, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        # Grade distribution pie
        grade_counts = df["Grade"].value_counts().reset_index()
        grade_counts.columns = ["Grade", "Count"]

        fig = px.pie(grade_counts, values="Count", names="Grade",
                     title="Grade Distribution",
                     color="Grade", color_discrete_map=GRADE_COLORS,
                     hole=0.4)
        fig.update_layout(template="plotly_dark", height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Grade distribution bar
        fig2 = px.bar(grade_counts, x="Grade", y="Count",
                     title="Grade Count",
                     color="Grade", color_discrete_map=GRADE_COLORS,
                     text="Count")
        fig2.update_layout(template="plotly_dark", height=400, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        # Credit-weighted chart
        fig = px.scatter(df, x="Marks", y="Grade Point", size="Credits",
                       title="Marks vs Grade Points (Size = Credits)",
                       color="Subject", hover_data=["Subject", "Marks", "Credits"])
        fig.update_layout(template="plotly_dark", height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Radar chart for subjects
        fig2 = go.Figure()
        categories = df["Subject"].tolist() + [df["Subject"].tolist()[0]]
        values = df["Marks"].tolist() + [df["Marks"].tolist()[0]]

        fig2.add_trace(go.Scatterpolar(r=values, theta=categories, fill="toself",
                                        fillcolor="rgba(0, 212, 255, 0.3)",
                                        line=dict(color="#00d4ff")))
        fig2.update_layout(template="plotly_dark", height=500,
                          title="Subject Performance Radar",
                          polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
        st.plotly_chart(fig2, use_container_width=True)

# Data table
st.markdown("---")
st.subheader("📋 Complete Grade Sheet")
if len(df) > 0:
    display_df = df[["Subject", "Marks", "Credits", "Grade", "Grade Point", "Quality Points"]]
    st.dataframe(display_df, use_container_width=True)

    # Export button
    csv = display_df.to_csv(index=False)
    st.download_button("📥 Download Grade Sheet", csv, "grades.csv", "text/csv")
else:
    st.info("👈 Enter your marks in the sidebar to see your grades here!")

st.caption("Grade Scale: A+(90-100), A(85-89), A-(80-84), B+(75-79), B(70-74), B-(65-69), C+(60-64), C(55-59), C-(50-54), D+(45-49), D(40-44), D-(35-39), F(0-34)")
