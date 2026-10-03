import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Weight Tracker", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .metric-card { background-color: #1e2530; padding: 20px; border-radius: 10px; text-align: center; }
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: #1e2530; color: white; border: 1px solid #3d4654;
    }
    .stDateInput > div > div > input { background-color: #1e2530; color: white; }
</style>
""", unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect('weight.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, weight REAL, date TEXT, notes TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, height REAL, goal_weight REAL)''')
    conn.commit()
    c.execute('SELECT COUNT(*) FROM settings')
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO settings (height, goal_weight) VALUES (170, 70)')
    conn.commit()
    conn.close()

def get_entries():
    conn = sqlite3.connect('weight.db')
    df = pd.read_sql('SELECT * FROM entries ORDER BY date DESC', conn)
    conn.close()
    return df

def add_entry(weight, date, notes):
    conn = sqlite3.connect('weight.db')
    c = conn.cursor()
    c.execute('INSERT INTO entries (weight, date, notes) VALUES (?, ?, ?)',
              (weight, date, notes))
    conn.commit()
    conn.close()

def delete_entry(entry_id):
    conn = sqlite3.connect('weight.db')
    c = conn.cursor()
    c.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()

def get_settings():
    conn = sqlite3.connect('weight.db')
    df = pd.read_sql('SELECT * FROM settings LIMIT 1', conn)
    conn.close()
    return df.iloc[0] if not df.empty else {'height': 170, 'goal_weight': 70}

def update_settings(height, goal_weight):
    conn = sqlite3.connect('weight.db')
    c = conn.cursor()
    c.execute('UPDATE settings SET height = ?, goal_weight = ?', (height, goal_weight))
    conn.commit()
    conn.close()

def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "#60a5fa"
    elif bmi < 25:
        return "Normal", "#4ade80"
    elif bmi < 30:
        return "Overweight", "#fbbf24"
    else:
        return "Obese", "#f87171"

init_db()

st.title("⚖️ Weight Tracker")
st.markdown("---")

entries = get_entries()
settings = get_settings()

# Calculate stats
current_weight = entries.iloc[0]['weight'] if not entries.empty else 0
start_weight = entries.iloc[-1]['weight'] if not entries.empty else 0
weight_change = current_weight - start_weight if entries.shape[0] > 1 else 0
bmi = calculate_bmi(current_weight, settings['height']) if current_weight > 0 else 0
bmi_cat, bmi_color = get_bmi_category(bmi)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric-card'><h3>Current</h3><h2 style='color:#60a5fa'>{current_weight:.1f} kg</h2></div>", unsafe_allow_html=True)
with col2:
    color = "#4ade80" if weight_change < 0 else "#f87171"
    st.markdown(f"<div class='metric-card'><h3>Change</h3><h2 style='color:{color}'>{weight_change:+.1f} kg</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h3>BMI</h3><h2 style='color:{bmi_color}'>{bmi:.1f}</h2><small>{bmi_cat}</small></div>", unsafe_allow_html=True)
with col4:
    diff = current_weight - settings['goal_weight'] if current_weight > 0 else 0
    st.markdown(f"<div class='metric-card'><h3>To Goal</h3><h2 style='color:#fbbf24'>{diff:+.1f} kg</h2></div>", unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📝 Log Weight", "📋 History", "📊 Charts", "⚙️ Settings"])

with tab1:
    st.header("Log Today's Weight")
    with st.form("weight_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=70.0, step=0.1)
            date = st.date_input("Date", value=datetime.now())
        with col2:
            notes = st.text_input("Notes (optional)")
        if st.form_submit_button("Log Weight", use_container_width=True):
            add_entry(weight, date.isoformat(), notes)
            st.success("Weight logged!")

with tab2:
    st.header("Weight History")
    if not entries.empty:
        for _, row in entries.iterrows():
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.markdown(f"### {row['weight']} kg")
            with col2:
                st.markdown(f"**{row['date']}**")
                if row['notes']:
                    st.caption(row['notes'])
            with col3:
                if st.button("🗑️", key=f"del_{row['id']}"):
                    delete_entry(row['id'])
                    st.rerun()
            st.markdown("---")
    else:
        st.info("No weight entries yet. Start tracking!")

with tab3:
    st.header("Progress Charts")
    if not entries.empty:
        entries_sorted = entries.sort_values('date')

        # Main weight chart
        fig = px.line(entries_sorted, x='date', y='weight', title="Weight Over Time",
                     markers=True)
        fig.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117', font_color='white')
        fig.update_traces(line_color='#60a5fa', marker_color='#60a5fa')

        # Add goal line if set
        goal = settings['goal_weight']
        fig.add_hline(y=goal, line_dash="dash", line_color="#4ade80", annotation_text="Goal")
        fig.add_annotation(x=entries_sorted['date'].iloc[-1], y=goal, text=f"Goal: {goal}kg",
                          showarrow=False, font_color="#4ade80")

        st.plotly_chart(fig, use_container_width=True)

        # BMI chart
        entries_sorted['bmi'] = entries_sorted['weight'].apply(
            lambda w: calculate_bmi(w, settings['height']))

        fig2 = px.line(entries_sorted, x='date', y='bmi', title="BMI Over Time", markers=True)
        fig2.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117', font_color='white')
        fig2.update_traces(line_color='#fbbf24', marker_color='#fbbf24')
        st.plotly_chart(fig2, use_container_width=True)

        # Weekly average
        entries_sorted['date'] = pd.to_datetime(entries_sorted['date'])
        entries_sorted['week'] = entries_sorted['date'].dt.isocalendar().week
        weekly = entries_sorted.groupby('week')['weight'].mean().reset_index()

        fig3 = px.bar(weekly, x='week', y='weight', title="Weekly Average Weight")
        fig3.update_layout(plot_bgcolor='#1e2530', paper_bgcolor='#0e1117', font_color='white')
        fig3.update_traces(marker_color='#a78bfa')
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Log some weights to see charts!")

with tab4:
    st.header("Settings")
    with st.form("settings_form"):
        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0,
                                     value=float(settings['height']), step=1.0)
        with col2:
            goal = st.number_input("Goal Weight (kg)", min_value=30.0, max_value=200.0,
                                  value=float(settings['goal_weight']), step=0.5)
        if st.form_submit_button("Update Settings", use_container_width=True):
            update_settings(height, goal)
            st.success("Settings updated!")

    # BMI Scale
    st.markdown("### BMI Scale")
    bmi_data = pd.DataFrame({
        'Category': ['Underweight', 'Normal', 'Overweight', 'Obese'],
        'Min': [0, 18.5, 25, 30],
        'Max': [18.5, 25, 30, 50],
        'Color': ['#60a5fa', '#4ade80', '#fbbf24', '#f87171']
    })
    for _, row in bmi_data.iterrows():
        st.markdown(f"- **{row['Category']}**: {row['Min']} - {row['Max']}")
