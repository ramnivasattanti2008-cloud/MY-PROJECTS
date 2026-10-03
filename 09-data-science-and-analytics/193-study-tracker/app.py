import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime, timedelta

st.set_page_config(page_title="Study Tracker", page_icon="📚", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .metric-card { background-color: #1e2530; padding: 20px; border-radius: 10px; text-align: center; }
    h1, h2, h3 { color: #ffffff !important; }
    .stSelectbox > div > div > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: #1e2530; color: white; border: 1px solid #3d4654;
    }
    .stDateInput > div > div > input { background-color: #1e2530; color: white; }
</style>
""", unsafe_allow_html=True)

SUBJECTS = ["Mathematics", "Physics", "Chemistry", "Biology", "Computer Science",
            "History", "Geography", "Economics", "Literature", "Languages", "Other"]

def init_db():
    conn = sqlite3.connect('study.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, hours REAL,
                  date TEXT, notes TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS goals
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, weekly_hours REAL)''')
    conn.commit()
    # Initialize default goal
    c.execute('SELECT COUNT(*) FROM goals')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO goals (weekly_hours) VALUES (20)')
    conn.commit()
    conn.close()

def get_sessions():
    conn = sqlite3.connect('study.db')
    df = pd.read_sql('SELECT * FROM sessions ORDER BY date DESC', conn)
    conn.close()
    return df

def add_session(subject, hours, date, notes):
    conn = sqlite3.connect('study.db')
    c = conn.cursor()
    c.execute('INSERT INTO sessions (subject, hours, date, notes) VALUES (?, ?, ?, ?)',
              (subject, hours, date, notes))
    conn.commit()
    conn.close()

def delete_session(session_id):
    conn = sqlite3.connect('study.db')
    c = conn.cursor()
    c.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
    conn.commit()
    conn.close()

def get_goal():
    conn = sqlite3.connect('study.db')
    df = pd.read_sql('SELECT * FROM goals LIMIT 1', conn)
    conn.close()
    return df.iloc[0]['weekly_hours'] if not df.empty else 20

def update_goal(weekly_hours):
    conn = sqlite3.connect('study.db')
    c = conn.cursor()
    c.execute('UPDATE goals SET weekly_hours = ?', (weekly_hours,))
    conn.commit()
    conn.close()

init_db()

st.title("📚 Study Tracker")
st.markdown("---")

sessions = get_sessions()
current_goal = get_goal()

# Calculate stats
today = datetime.now()
week_start = today - timedelta(days=today.weekday())
week_sessions = sessions[sessions['date'] >= week_start.date().isoformat()] if not sessions.empty else pd.DataFrame()
week_hours = week_sessions['hours'].sum() if not week_sessions.empty else 0
total_hours = sessions['hours'].sum() if not sessions.empty else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric-card'><h3>Total Hours</h3><h2 style='color:#60a5fa'>{total_hours:.1f}h</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h3>This Week</h3><h2 style='color:#4ade80'>{week_hours:.1f}h</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3>Goal</h3><h2 style='color:#fbbf24'>{current_goal}h/week</h2></div>", unsafe_allow_html=True)
with col4:
    remaining = max(0, current_goal - week_hours)
    st.markdown(f"<div class='metric-card'><h3>Remaining</h3><h2 style='color:#f87171'>{remaining:.1f}h</h2></div>", unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["➕ Log Session", "📋 Sessions", "📊 Progress", "⚙️ Settings"])

with tab1:
    st.header("Log Study Session")
    with st.form("session_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            subject = st.selectbox("Subject", SUBJECTS)
            hours = st.number_input("Hours Studied", min_value=0.5, max_value=24.0, value=1.0, step=0.5)
        with col2:
            date = st.date_input("Date", value=datetime.now())
            notes = st.text_input("Notes (optional)")
        if st.form_submit_button("Log Session", use_container_width=True):
            add_session(subject, hours, date.isoformat(), notes)
            st.success("Session logged!")

with tab2:
    st.header("Study Sessions")
    if not sessions.empty:
        sessions['date'] = pd.to_datetime(sessions['date'])
        for _, row in sessions.head(20).iterrows():
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.markdown(f"### {row['hours']}h")
            with col2:
                st.markdown(f"**{row['subject']}** - {row['date'].strftime('%Y-%m-%d')}")
                if row['notes']:
                    st.caption(row['notes'])
            with col3:
                if st.button("🗑️", key=f"del_{row['id']}"):
                    delete_session(row['id'])
                    st.rerun()
            st.markdown("---")
    else:
        st.info("No study sessions logged yet. Start tracking!")

with tab3:
    st.header("Study Progress")
    if not sessions.empty:
        sessions['date'] = pd.to_datetime(sessions['date'])

        col1, col2 = st.columns(2)
        with col1:
            # Hours by subject
            subject_totals = sessions.groupby('subject')['hours'].sum().reset_index()
            subject_totals = subject_totals.sort_values('hours', ascending=True)
            fig = px.bar(subject_totals, y='subject', x='hours', orientation='h',
                        title="Hours by Subject", color='hours', color_continuous_scale='Viridis')
            fig.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117', font_color='white')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Daily hours
            sessions['day'] = sessions['date'].dt.date
            daily = sessions.groupby('day')['hours'].sum().reset_index()
            fig2 = px.line(daily, x='day', y='hours', title="Daily Study Hours", markers=True)
            fig2.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117', font_color='white')
            fig2.update_traces(line_color='#60a5fa', marker_color='#60a5fa')
            st.plotly_chart(fig2, use_container_width=True)

        # Weekly comparison
        sessions['week'] = sessions['date'].dt.isocalendar().week
        sessions['year'] = sessions['date'].dt.year
        weekly = sessions.groupby(['year', 'week'])['hours'].sum().reset_index()
        weekly['label'] = weekly.apply(lambda x: f"Y{x['year']}W{x['week']}", axis=1)

        fig3 = px.bar(weekly, x='label', y='hours', title="Weekly Study Hours")
        fig3.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117', font_color='white')
        fig3.update_traces(marker_color='#4ade80')
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Log some study sessions to see progress!")

with tab4:
    st.header("Settings")
    with st.form("goal_form"):
        weekly_goal = st.number_input("Weekly Study Goal (hours)", min_value=1, max_value=168, value=int(current_goal))
        if st.form_submit_button("Update Goal", use_container_width=True):
            update_goal(weekly_goal)
            st.success("Goal updated!")
